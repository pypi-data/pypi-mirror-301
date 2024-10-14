import numpy as np
import re,os

def extract_and_calculate(data_raw,header,sort=False):
    """
    Extract pixel coordinates from point sources.
    The function calculates the net grayscale by subtracting the background mean multiplied by the pixel count from the grayscale sum.
    The results are then sorted in descending order based on the net grayscale values.

    Inputs:
        data_raw -> [array] Array with columns for pixel coordinates, pixel count, grayscale sum, and background values.
        header -> [dict] Dictionary containing header information such as image width and height.
    Outputs:
        result -> [dict] Dictionary containing sorted data by net grayscale:
            - x: X coordinates w.r.t the image center.
            - y: Y coordinates w.r.t the image center.
            - pixel_count: Pixel count
            - grayscale_sum: Grayscale sum
            - background_mean: Background mean
            - background_variance: Background variance
            - net_grayscale: Net grayscale values
    """
    # Shift the origin from the top left corner to the center of the image and adjust the pixel coordinates of the point sources
    x = data_raw[:, 0] - int(header['WIDTH'])/2
    y = data_raw[:, 1] - int(header['HEIGHT'])/2 # maybe int(header['HEIGHT'])/2 - data_raw[:, 1]
    
    pixel_count = data_raw[:, 2]
    grayscale_sum = data_raw[:, 5]
    background_mean = data_raw[:, 6]
    background_variance = data_raw[:, 7]
    net_grayscale = grayscale_sum - background_mean * pixel_count
    
    # Create a structured array to sort by net_grayscale
    structured_array = np.core.records.fromarrays(
        [x, y, pixel_count, grayscale_sum, net_grayscale, background_mean, background_variance],
        names='x, y, pixel_count, grayscale_sum, net_grayscale, background_mean, background_variance'
    )

    if sort:
        sorted_array = np.sort(structured_array, order='net_grayscale')[::-1]
    else:
        sorted_array = structured_array
            
    result = {
        'x': sorted_array['x'],
        'y': sorted_array['y'],
        'pixel_count': sorted_array['pixel_count'].astype(int),
        'grayscale_sum': sorted_array['grayscale_sum'].astype(int),
        'net_grayscale': sorted_array['net_grayscale'],
        'background_mean': sorted_array['background_mean'],
        'background_variance': sorted_array['background_variance']
    }
    return result

def parse_ipd_file(file_path):
    """
    Parse an IPD-formatted file to extract header information and data.
    The results are sorted in descending order based on the net grayscale values of point sources.

    Usage:
        >>> header, star_data, sate_data = parse_ipd_file('path/to/ipd_file.IPD')
    Inputs:
        file_path -> [str] Path to the IPD-formatted file.
    Outputs:
        header -> [dict] Dictionary containing header information:
            - STAROBJ_NUM: Number of star objects.
            - SATEOBJ_NUM: Number of satellite objects.
            - WIDTH: Width of the image.
            - HEIGHT: Height of the image.
            - SATEOBJ_TXH: Index of satellite object.
            - Other metadata as key-value pairs.
        star_data -> [dict] Dictionary containing processed star data:
            - x: X coordinates w.r.t the image center.
            - y: Y coordinates w.r.t the image center.
            - pixel_count: Pixel count.
            - grayscale_sum: Grayscale sum.
            - background_mean: Background mean.
            - background_variance: Background variance.
            - net_grayscale: Net grayscale values.
        sate_data -> [dict] Dictionary containing processed satellite data:
            - x: X coordinates w.r.t the image center.
            - y: Y coordinates w.r.t the image center.
            - pixel_count: Pixel count.
            - grayscale_sum: Grayscale sum.
            - background_mean: Background mean.
            - background_variance: Background variance.
            - net_grayscale: Net grayscale values.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    header,data = {},[]

    # Extract header information
    header_pattern = re.compile(r'(\w+)=\s*(.*)')
    for line in lines:
        line = line.strip()
        match = header_pattern.match(line)
        if match:
            key, value = match.groups()
            if key.startswith('SATEOBJ_TXH'):
                header.setdefault('SATEOBJ_TXH', []).append(int(value.strip()))
            else:
                header[key] = value.strip()
        else:
            data.append(line)

    # Parse data entries
    star_obj_num = int(header['STAROBJ_NUM'])
    sate_obj_num = int(header['SATEOBJ_NUM'])

    # Use numpy to load the data efficiently
    data = np.array([line.split() for line in data if line.strip() != ''], dtype=float)

    star_data_raw = data[:star_obj_num]
    sate_data_raw = data[star_obj_num:star_obj_num + sate_obj_num]

    star_data = extract_and_calculate(star_data_raw,header,sort=True)
    sate_data = extract_and_calculate(sate_data_raw,header)

    return header, star_data, sate_data

def parse_ipd_dir(ipd_directory):
    """
    Parse IPD-formatted files in a directory to extract observation times and validity status.
    The function traverses the directory, reads each IPD file, and extracts the observation times and validity status.
    It returns a list of valid files and their corresponding observation times.

    Usage:
        >>> ipd_files, t_array = parse_ipd_file_pre('path/to/ipd_directory')
    Inputs:
        ipd_directory -> [str] Path to the directory storing IPD files.
    Outputs:
        ipd_files -> [array-like] Array of valid IPD file names.
        t_array -> [array-like] Array of observation times for valid files.
    """
    t_list,valid_list = [],[]

    # Traverse the directory and process each IPD file
    ipd_files = sorted([f for f in os.listdir(ipd_directory) if os.path.splitext(f)[1].lower() == '.ipd'])

    for ipd_file in ipd_files:
        file_path = os.path.join(ipd_directory, ipd_file)

        # Open the file and read its content
        with open(file_path, 'r') as file:
            for line in file:
                if line.startswith('DATE_OBS'):
                    t_list.append(line.split('=')[1].strip())
                elif line.startswith('SATEOBJ_NUM'):
                    valid_list.append(line.split('=')[1].strip())  # If equal to 0, it is considered invalid
                    break

    valid_array = np.array(valid_list).astype(bool)
    t_array = np.array(t_list)[valid_array]
    ipd_files = np.array(ipd_files)[valid_array]
    return ipd_files, t_array
