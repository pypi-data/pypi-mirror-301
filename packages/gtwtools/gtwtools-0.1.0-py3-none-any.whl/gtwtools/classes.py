import os, time, glob
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler,FileSystemEvent
from concurrent.futures import ProcessPoolExecutor, as_completed

from .generate_gtw import generate_gtw_files

"""
Because Python's standard output is buffered by default. 
This means that the output is temporarily stored in a buffer and not actually written to the console or file until the buffer is full or the program ends. 
Fortunately, there are several ways to globally make all print statements output immediately.

Method 1: Run Python scripts with the -u option

The easiest way is to use the -u option when running the script, which tells the Python interpreter to run in unbuffered mode.
However, this will make the standard output and standard error output of the entire program unbuffered, 
which may have a slight impact on performance, especially in the case of large amounts of output.

Usage:
    $ python -u your_script.py
    
Method 2: Modify sys.stdout in the code

You can make all output flush immediately by setting the buffering mode of sys.stdout in the code.

Usage:
    >>> import sys
    >>> sys.stdout.reconfigure(line_buffering=True)

Method 3: Redefine the print function

You can redefine the print function at the beginning of the code to use flush=True by default.  

Usage:
    >>> import sysimport functools
    >>> print = functools.partial(print, flush=True)  
"""

# Define timeout and polling interval
TIMEOUT = 10 * 60  # 10 minutes
POLLING_INTERVAL = 5  # Check every 5 seconds
MAX_WORKERS = os.cpu_count() - 1 # Get the number of CPU cores of the system

def _find_success_file(dir):
    """
    Check if there is a file named 'success' with any extension in the given directory.

    Inputs:
        dir -> [str] The directory to search for the 'success' file.

    Returns:
        [bool] True if a 'success' file is found, otherwise False.
    """
    success_file = glob.glob(os.path.join(dir, 'success.*'))
    return len(success_file) > 0

def process_directory(ipd_dir,gtw_dir,res_dir,eph_path,att_path):
    """
    Process IPD files in the given directory.

    This function processes IPD files stored in the specified directory by
    generating corresponding GTW and ICR files using the auxiliary EPH and ATT files.
    The function checks for the existence of a success marker file (such as "success.fin")
    in the IPD directory before starting the process. If the marker file is found,
    it calls the `generate_gtw_files` function. The process is considered successful
    if the GTW files are generated without exceptions.

    Inputs:
        ipd_dir -> [str] Directory where IPD files are stored.
        gtw_dir -> [str] Directory where GTW files are stored.
        res_dir -> [str] Directory where ICR files are stored.
        eph_path -> [str] Path of the EPH files (ephemeris files used for orbital data).
        att_path -> [str] Path of the POS files (attitude/position files).
    Returns:
        ipd_success -> [bool] True if the IPD files are processed successfully, False otherwise.
    Outputs:
        GTW and ICR files in the specified directory
    """
    ipd_success = False  # Initialize the success flag as False
    start_time = time.time()  # Record the start time to enforce a timeout

    # Check if the IPD directory exists
    if os.path.exists(ipd_dir):
        print(f"Processing entry: {ipd_dir}")

        # Loop to wait for the presence of the 'success' marker file
        while True:
            # If the success marker file is found, proceed to process the IPD files
            if _find_success_file(ipd_dir):
                print(f"Found success.fin in {ipd_dir}, proceeding to process IPD files.")

                try:
                    # Attempt to generate the GTW and ICR files using the provided data
                    generate_gtw_files(ipd_dir, gtw_dir, res_dir, eph_path, att_path)
                    ipd_success = True # Set success flag to True upon successful completion
                except Exception as e:
                    # If any exception occurs, capture and log the error without halting the program
                    print(f"Error while processing {ipd_dir}: {str(e)}")
                    ipd_success = False # Set the success flag to False in case of an error
                break  # Exit the loop after processing or encountering an error

            # If the operation takes too long, terminate the process after reaching the timeout
            elif time.time() - start_time > TIMEOUT:
                print(f"Timeout while waiting for success.fin in {ipd_dir}.")
                break
            else:
                # Wait for a short interval before checking again for the success marker
                print(f"Waiting for success.fin in {ipd_dir}...")
                time.sleep(POLLING_INTERVAL)
    else:
        print(f"Directory does not exist: {ipd_dir}")
    return ipd_success

def check_gtw_completed(gtw_dir,timeout=5):
    """
    Monitor the GTW directory and check if all files have been generated
    by continuously checking the modification time of the files in the GTW directory.

    Inputs:
        gtw_dir -> [str] Directory where GTW files are stored.
        timeout -> [int, optional, default=5] Time (in seconds) to wait before assuming no further modifications.
    """

    last_mod_time = time.time() # Initialize the last modification time

    while True:
        # Get the most recent modification time from the files in the directory
        current_mod_time = max(os.path.getmtime(os.path.join(gtw_dir, f)) for f in os.listdir(gtw_dir))
        if current_mod_time > last_mod_time:
            # Update last modification time if files are still being modified
            last_mod_time = current_mod_time
        else:
            # If no file modifications within the timeout, assume generation is complete
            if time.time() - last_mod_time >= timeout:
                print("All GTW files have been generated successfully. Stopping observer.")
                break

        time.sleep(1) # Wait before checking again

    # Create an empty success.fin file indicating that all GTW files have been generated.
    success_file_path = os.path.join(gtw_dir, 'success.fin')
    open(success_file_path, 'w').close()

def run_ipd_listfile_monitor(root_dir, eph_path, att_path, output_dir, ipd_list_file='IPD.list'):
    """
    This function monitors the 'IPD.list' file in the specified directory and processes
    the IPD files listed in this file. It first checks if a 'success.fin' file exists in the
    root directory, indicating that the IPD files have already been processed. If the
    'success.fin' file is found, it processes the IPD files in parallel using a process pool.
    If no 'success.fin' file is found, the function sets up a file system observer to monitor
    changes to the 'IPD.list' file and automatically processes new entries when the file
    is modified.

    Inputs:
        root_dir -> [str] Input base directory where the IPD.list file is stored.
        eph_path -> [str] EPH file path used for generating GTW files.
        att_path -> [str] ATT file path used for generating GTW files.
        output_dir -> [str] Output base directory where GTW and ICR files are stored.
        ipd_list_file -> [str, optional, default='IPD.list'] Filename of the IPD list file
                         to monitor, where each line contains an absolute directory of a group of IPD files.
    """
    ipd_list_path = os.path.join(root_dir, ipd_list_file)
    gtw_dir = os.path.join(output_dir, 'L2/GTW')  # Directory where GTW files will be stored
    res_dir = os.path.join(output_dir, 'L2/GTW/RES')  # Directory where ICR files will be stored

    # Check if 'success.fin' already exists in the root directory before starting the observer.
    # If it exists, it means the files have already been processed, and the function will skip
    # monitoring and proceed directly to process the files listed in 'IPD.list'.
    if _find_success_file(root_dir):
        print(f"Detected success.fin in {root_dir} at startup.\n")

        with open(ipd_list_path, 'r') as f:
            entries = [line.strip() for line in f] # Read each line in 'IPD.list' as an IPD directory path.

        # Use a process pool to parallelize the processing of IPD directories listed in 'IPD.list'.
        # Each directory entry is submitted to a separate process for parallel execution.
        with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
            # Submit tasks to the process pool to process each IPD directory.
            futures = {executor.submit(process_directory, ipd_dir, gtw_dir, res_dir, eph_path, att_path): ipd_dir for ipd_dir in entries}

            # As each task is completed, retrieve the result and check if the process was successful.
            for future in as_completed(futures):
                ipd_dir = futures[future]
                try:
                    ipd_success = future.result()  # Get the result from the completed process.
                    if ipd_success:
                        print(f"GTW files have been generated successfully for {ipd_dir}.")
                    else:
                        print(f"Processing of {ipd_dir} was not successful.")
                except Exception as exc:
                    print(f"Processing {ipd_dir} generated an exception: {exc}")
        return

    # If no 'IPD.list' file is detected, print an error and exit.
    if not os.path.exists(ipd_list_path):
        print(f"No {ipd_list_file} file detected in {root_dir} at startup, exiting immediately.")
        return

    # If 'success.fin' is not found, set up a file system observer to monitor changes to the IPD.list file.
    observer = Observer()
    event_handler = IPDFileHandler(root_dir, ipd_list_file, eph_path, att_path, output_dir, observer)
    observer.schedule(event_handler, root_dir, recursive=False)
    observer.start()

    # Manually trigger an event used for initializing any necessary actions.
    event_handler.trigger_event()

    try:
        # Keep the main loop running to allow the observer to continue monitoring the IPD.list file.
        while not getattr(event_handler, '_stop_loop', False):
            time.sleep(1)  # Keep the main thread alive by sleeping in short intervals.
    except KeyboardInterrupt:
        # If a keyboard interrupt is detected, stop the observer and clean up.
        observer.stop()
    finally:
        observer.join()  # Ensure the observer thread is properly cleaned up.

class IPDFileHandler(FileSystemEventHandler):
    """
    Event handler class for monitoring changes in the IPD list file.
    """
    def __init__(self, root_dir, ipd_list_file, eph_path, att_path, output_dir, observer):
        """
        Initialize the IPDFileHandler.

        Inputs:
            root_dir -> [string] Base directory where the IPD.list file is stored.
            ipd_list_file -> [string] The filename of the IPD list file being monitored.
            eph_path -> [string] Path to the EPH file (used for generating GTW files).
            att_path -> [string] Path to the ATT file (used for generating GTW files).
            output_dir -> [string] Base output directory where the processed GTW and ICR files are stored.
            observer -> [Observer] The `Observer` instance that is watching for file changes.
        """
        self.root_dir = root_dir  # The base directory where the IPD list file is located
        self.ipd_list_path = os.path.join(root_dir, ipd_list_file)  # Full path to the IPD list file being monitored
        self.success_file_path = os.path.join(root_dir, 'success.fin')  # Path to the 'success.fin' file
        self.eph_path = eph_path  # Path to the EPH file
        self.att_path = att_path  # Path to the ATT file
        self.output_dir = output_dir  # Base output directory
        self.gtw_dir = os.path.join(output_dir, 'L2/GTW')  # Directory for storing GTW files
        self.res_dir = os.path.join(output_dir, 'L2/GTW/RES')  # Directory for storing ICR files
        self.observer = observer  # The `Observer` instance responsible for monitoring file changes
        self.processed_dirs = set()  # A set to keep track of directories that have already been processed

        # Get the initial file size of the IPD list file at startup
        self.previous_size = os.path.getsize(self.ipd_list_path)

        # Flag to indicate if there are pending entries that need processing
        self.new_entries_pending = False

        # This flag is used to stop the main loop when the processing should be terminated
        self._stop_loop = False

    def trigger_event(self):
        """
        This method simulates a file system event to manually start the processing of existing entries.
        """
        # Create a mock event object
        mock_event = FileSystemEvent('mock')
        self.on_moved(mock_event) # Trigger the 'on_moved' handler with the mock event

    def on_moved(self, event):
        """
        In this particular implementation, the function handles mock events.
        If the event is a mock event (triggered manually), it will process the IPD files at startup.

        Inputs:
            event -> [FileSystemEvent] Event object.
        """
        if event.src_path == 'mock':
            # If this is a manually triggered event, process existing entries in the IPD list
            self.process_new_entries(first_run=True)

    def on_modified(self, event):
        """
        Event handler called when the IPD list file is modified.

        This method is triggered whenever a modification event occurs for the IPD list file.
        It checks if the file size has changed since the last event to avoid processing
        unnecessary modifications (e.g., when the file is modified but not meaningfully
        changed). If the file size has changed, the method triggers the processing of new entries.

        Inputs:
            event -> [FileSystemEvent] Event object that contains details about the modification event.
        """
        # Get the current size of the IPD list file
        current_size = os.path.getsize(self.ipd_list_path)

        # Check if the event corresponds to the monitored IPD list file and if the size has changed
        if event.src_path == self.ipd_list_path and current_size != self.previous_size:
            print(f"\n{event.src_path} has been modified.\n")
            # Update the stored file size to the new size after modification
            self.previous_size = current_size
            # Process any new entries in the IPD list file
            self.process_new_entries()

    def on_created(self, event):
        """
        Event handler called when a new file is created in the root directory.

        This method is triggered when a new file is created, specifically looking for the 'success.fin'
        file in the root directory. If 'success.fin' is detected, it waits for any pending entries to be
        processed and then calls the `check_gtw_completed` function to finalize the GTW file processing.
        After all tasks are completed, it stops the file system observer and exits the monitoring loop.

        Inputs:
            event -> [FileSystemEvent] The event object that contains details about the creation event.
        """
        # If the created file is 'success.fin', begin final processing and stop the observer
        if event.src_path == self.success_file_path:
            print(f"\nDetected 'success.fin' in {self.root_dir}, waiting for pending entries to finish...")

            # Wait for any pending entries to be processed
            while self.new_entries_pending:
                time.sleep(1)

            # Finalize GTW file processing by calling the function to check completion
            check_gtw_completed(self.gtw_dir, 5)

            # Stop the observer and signal the main loop to exit
            self.observer.stop()
            self._stop_loop = True  # Set a flag to stop the main loop

    def process_new_entries(self, first_run=False):
        """
        Read the IPD list file and process new directory entries.

        This method reads the IPD list file and processes any new directory entries
        that have not been processed yet. If the method is called for the first time
        during startup, it processes all entries in the file. If it is called later,
        it only processes entries that haven't been processed before. It uses
        a process pool to handle each entry in parallel.

        Inputs:
            first_run -> [bool, optional, default=False] Indicates if this is the initial processing on startup.
                         If True, it processes all entries in the IPD list file.
        """
        # Open and read the IPD list file to get the list of entries (directories)
        with open(self.ipd_list_path, 'r') as f:
            lines = [line.strip() for line in f]

        if first_run:
            # On first run, process all entries in the file
            new_entries = lines
        else:
            # If this is not the first run, only process entries that haven't been processed yet
            new_entries = [line for line in lines if line not in self.processed_dirs]

        if new_entries:
            # If there are new entries to process, mark that there are pending entries
            self.new_entries_pending = True

            # Add each new entry to the set of processed directories to avoid reprocessing later
            for entry in new_entries:
                self.processed_dirs.add(entry)

            # Use a process pool to parallelize the processing of new entries
            with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
                # Submit each entry to the process pool for parallel processing
                futures = {executor.submit(process_directory, entry, self.gtw_dir, self.res_dir, self.eph_path, self.att_path): entry for entry in new_entries}

                # Process the result of each completed task
                for future in as_completed(futures):
                    entry = futures[future]
                    try:
                        # Get the result from the future (which is the return value of process_directory)
                        ipd_success = future.result()

                        # Check if the processing of the entry was successful
                        if ipd_success:
                            print(f"GTW files have been generated successfully for {entry}.\n")
                        else:
                            print(f"Processing of {entry} was not successful.")

                    except Exception as exc:
                        # If an exception occurs during processing, log the error
                        print(f"Processing {entry} generated an exception: {exc}")

            # Once all entries have been processed, reset the pending flag
            self.new_entries_pending = False
        else:
            print("No new entries to process.")