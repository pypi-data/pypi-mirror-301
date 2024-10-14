import os
import numpy as np
from datetime import datetime

def format_ra(ra):
    """
    Format right ascension (RA) in degrees to a specific string format.

    Inputs:
        ra -> [float] Right ascension in degrees.
    Outputs:
        [str] Formatted RA as a string without decimal points.
    """
    degrees = int(ra)
    arcminutes = int((ra - degrees) * 60)
    arcseconds = (ra - degrees - arcminutes / 60) * 3600

    # Round arcseconds to two decimal places
    arcseconds = round(arcseconds, 2)

    # Check if arcseconds need to be carried over
    if arcseconds >= 60.0:
        arcseconds = 0.0
        arcminutes += 1

    # If arcminutes reaches 60, carry over to degrees
    if arcminutes == 60:
        arcminutes = 0
        degrees += 1

    return f"{degrees:03}{arcminutes:02}{arcseconds:05.2f}".replace(".", "")

def format_dec(dec):
    """
    Format declination (Dec) in degrees to a specific string format.

    Inputs:
        dec -> [float] Declination in degrees.
    Outputs:
        [str] Formatted Dec as a string without decimal points.
    """
    sign = '0' if dec >= 0 else '1'
    dec = abs(dec)
    degrees = int(dec)
    arcminutes = int((dec - degrees) * 60)
    arcseconds = (dec - degrees - arcminutes / 60) * 3600

    # Round arcseconds to one decimal place
    arcseconds = round(arcseconds, 1)

    # Check if arcseconds need to be carried over
    if arcseconds >= 60.0:
        arcseconds = 0.0
        arcminutes += 1

    # If arcminutes reaches 60, carry over to degrees
    if arcminutes == 60:
        arcminutes = 0
        degrees += 1

    return f"{sign}{degrees:02}{arcminutes:02}{arcseconds:04.1f}".replace(".", "")

def format_signal(value):
    """
    Format a signal value for radar (AGC) or optical (observed magnitude).

    Inputs:
        value -> [float] Signal value in dB or magnitude.
    Outputs:
        [str] Formatted signal as a string.
    """
    sign = '0' if value >= 0 else '1'
    value = abs(value) * 10  # Quantize to 0.1
    return f"{sign}{round(value):03}" 

def format_mag(mag):
    """
    Format a magnitude value to a specific string format.

    Inputs:
        mag -> [float] Magnitude value.
    Outputs:
        [str] Formatted magnitude as a string.
    """
    sign = '0' if mag >= 0 else '1'
    mag = abs(mag) * 100
    return f"{sign}{round(mag):05}"       

def format_position(value):
    """
    Format position coordinates to a specific string format.

    Inputs:
        value -> [float] Position coordinates in appropriate unit.
    Outputs:
        [str] Formatted position as a string.
    """
    sign = '0' if value >= 0 else '1'
    value = abs(value) * 1000
    return f"{sign}{round(value):013}"

def format_pixel_xy(value):
    """
    Format pixel coordinates to a specific string format.

    Inputs:
        value -> [float] Pixel coordinates.
    Outputs:
        [str] Formatted pixel coordinate as a string.
    """
    value = abs(value) * 1000
    return f"{round(value):08}"   

def format_photometry(value):
    """
    Format a photometry value to a specific string format.

    Inputs:
        value -> [float] Photometry value.
    Outputs:
        [str] Formatted photometry value as a string.
    """
    value = abs(value) * 1000
    return f"{round(value):08}"      

def format_precision(value, scale):
    """
    Format a precision value to a specific string format based on scale.

    Inputs:
        value -> [float] Precision value.
        scale -> [float] Scale factor for the precision.
    Outputs:
        [str] Formatted precision value as a string.
    """
    value = value / scale
    exponent = 0
    while value >= 100:
        value /= 10
        exponent += 1
    return f"{round(value):02}{exponent}"    

def format_wavelength(value):
    """
    Format a wavelength value to a specific string format.

    Inputs:
        value -> [float] Wavelength value in appropriate unit.
    Outputs:
        [str] Formatted wavelength value as a string.
    """
    value = value / 0.1
    exponent = 0
    while value >= 100:
        value /= 10
        exponent += 1
    return f"{round(value):03}{exponent}"


def format_gtw(ta_array, platform_xyz, radec, mag, target_id, GTW_dir=None, publisher="10808", yymm='0907',
               device_id=9602, time_system=8, coord_system=0, measurement_status=0, wavelength=532):
    """
    Writes ephemeris of the platform, as well as right ascension, declination, apparent magnitude of the target into a GTW-formatted file.

    Inputs:
        ta_array -> [astropy time, array-like] Array of observation times.
        platform_xyz -> [float, 2D array-like] Platform's 3D position, in kilometers.
        radec -> [float, 2D array-like] Right ascension and declination of the space object relative to the platform, in degrees.
        mag -> [float, array-like] Apparent magnitude of the space object.
        target_id -> [int] Unique identifier for the target.
        GTW_dir -> [str] Directory where the generated GTW files will be saved.
        publisher -> [str, optional, default='10808'] Identifier for the publisher of the data.
        yymm -> [str, optional, default='0907'] Date (YYMM format) of the GTW format activation.
        device_id -> [int, optional, default=9602] Identifier for the device used to collect the data.
        time_system -> [int, optional, default=8] Identifier for the time system used.
        coord_system -> [int, optional, default=0] Identifier for the coordinate system used.
        measurement_status -> [int, optional, default=0] Status identifier for the measurement.
        wavelength -> [int, optional, default=532] Wavelength (in nanometers) for the optical data (default is 532 nm).
    """

    # Ensure the output directory exists, create it if not
    if GTW_dir is None: GTW_dir = os.getcwd()
    if not os.path.exists(GTW_dir):
        os.makedirs(GTW_dir)

    # Get the number of time points in the observation array
    n = len(ta_array)

    # Extract the start and end observation times
    t_start_obj = ta_array[0]
    t_end_obj = ta_array[-1]
    t_start = t_start_obj.strftime('%Y%m%d%H%M%S')  # Format start time as 'YYYYMMDDHHMMSS'
    t_end = t_end_obj.strftime('%Y%m%d%H%M%S')  # Format end time as 'YYYYMMDDHHMMSS'

    # Calculate the duration of the observation segment in seconds
    delta_t = round((t_end_obj - t_start_obj).sec)

    # Format the target ID to be a six-digit number (e.g., '000123')
    txh_formatted = f'{target_id:06d}'

    # Construct the GTW file name using the start time, target ID, and device ID
    gtw_file_name = f'{t_start}_{txh_formatted}_{device_id}.GTW'
    gtw_file_path = os.path.join(GTW_dir, gtw_file_name)

    # File paths for auxiliary files (ephemeris and attitude)
    eph_path = 'AUX/EPH/L0_GEOGC.eph'
    att_path = 'AUX/POS/L0_GEOGC.pos'

    # Generate random values for uncertainties and other attributes (these are mock data)
    radec_std = np.random.normal(1, 0.1, n)  # uncertainties of RA/Dec
    mag_std = np.random.normal(0.1, 0.01, n)  # uncertainties of Magnitude
    x = np.random.uniform(0, 8900, n)  # X pixel coordinate
    y = np.random.uniform(0, 8900, n)  # Y pixel coordinate
    pixel_count = np.random.randint(1, 100, n)  # Pixel count for stars or space objects
    net_grayscale = np.random.uniform(500, 1e5, n)  # Total grayscale values
    background_mean = np.random.uniform(100, 500, n)  # Mean background value
    background_variance = np.random.uniform(5, 10, n)  # Background variance

    # Get the current date and time in the format 'YYYYMMDDHHMM'
    current_time = datetime.now().strftime('%Y%m%d%H%M')

    # Open the GTW file for writing
    with open(gtw_file_path, 'w') as gtw_file:
        # Write the start identifier
        gtw_file.write('C BEGIN\nC\n')
        gtw_file.write(f'C {eph_path}\n')  # Write ephemeris file path
        gtw_file.write(f'C {att_path}\n')  # Write attitude file path

        # Set and write the header fields
        head_field = f"{publisher:>5} {yymm:>4} {target_id:>6} {device_id:>4} {time_system:>1} {coord_system:>1}"
        gtw_file.write(f'C {head_field}\n')

        # Write the start and end times of the observation segment, and its duration
        gtw_file.write(f'C {t_start} {t_end} {delta_t}\n')
        gtw_file.write('C\nC\n')

        # Write the data entries for each time point
        for i in range(n):
            ra, dec = radec[i]  # Right ascension and declination
            platform_x, platform_y, platform_z = platform_xyz[i] * 1e3  # Convert platform coordinates from km to meters

            # Convert the observation time to a datetime object and format it
            date = ta_array[i].to_datetime()
            ymd = date.strftime('%Y%m%d')  # Date in 'YYYYMMDD' format
            hms = date.strftime('%H%M%S%f')  # Time in 'HHMMSSffff' format

            # Format RA and Dec for writing to the file
            ra_fmt = format_ra(ra)
            dec_fmt = format_dec(dec)

            # Create a formatted string for the data entry (this follows a specific GTW format)
            data_field = f" 41 3 {ymd:>8} {hms:>12} {ra_fmt:>9} {dec_fmt:>8} 0000 000 00 0000"
            gtw_file.write(head_field + data_field)

            # Write the REF (reference) field
            angular_precision = format_precision(radec_std[i], scale=0.1)  # Format angular precision
            magnitude = format_signal(mag[i])  # Format magnitude
            ref_field = f" {angular_precision:>3} {measurement_status:>1} {magnitude:>4} 0000 {format_wavelength(wavelength)}"
            gtw_file.write(ref_field)

            # Format observation time for the IPD file
            formatted_date_obs = datetime.strptime(ta_array[i].isot, '%Y-%m-%dT%H:%M:%S.%f').strftime('%Y%m%d%H%M%S')

            # Construct the IPD file name (used later in the photometry field)
            ipd_fn = f'9602_P{current_time}_012346_{formatted_date_obs}_L0_GEOGC_{i:05d}.ipd'

            # Write the photometry field (contains details about the target's pixel position and photometric data)
            photometry_field = (
                f" {format_position(platform_x)}"
                f" {format_position(platform_y)}"
                f" {format_position(platform_z)}"
                f" {format_pixel_xy(x[i])}"
                f" {format_pixel_xy(y[i])}"
                f" {pixel_count[i]:>06}"  # Pixel count
                f" {round(net_grayscale[i]):>010}"  # Total grayscale value
                f" {format_mag(mag[i])}"  # Magnitude
                f" {format_photometry(background_mean[i])}"  # Background mean
                f" {format_photometry(background_variance[i])}"  # Background variance
                f" {format_precision(mag_std[i], scale=0.01)}"  # Magnitude precision
                f" {ipd_fn:>63}\n"  # IPD file name
            )
            gtw_file.write(photometry_field)

        # Write the end identifier
        gtw_file.write('C END\n')