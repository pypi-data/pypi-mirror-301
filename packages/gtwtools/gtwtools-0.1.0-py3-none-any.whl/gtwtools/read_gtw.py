import numpy as np
from astropy.time import Time
from astropy.coordinates import SkyCoord
import astropy.units as u
import re

# Convert positions
def convert_position(value):
    """
    Convert a string representation of a position to a floating-point number.
    """
    sign = -1 if value[0] == '1' else 1
    return sign * float(value[1:]) / 1e3

def parse_gtw_file(file_path):
    """
    Parse a GTW-formatted file to extract header information and data.

    The GTW-formatted file contains information about the ephemeris of the site and the angle-only data of the space objects.
    The header section includes metadata, while the data section includes time, position,
    right ascension, declination, angular precision, visual magnitude, etc.

    Usage:
        >>> header_info, data_info = parse_gtw_file('path/to/gtw_file.GTW')
    Inputs:
        file_path -> [str] Path to the GTW-formatted file.
    Outputs:
        header_info -> [dict] Dictionary containing header information.
        data_info -> [dict] Dictionary containing extracted data:
            - times: Time array of observation times.
            - radec: SkyCoord object containing right ascension and declination.
            - angular_std: Array of angular precisions.
            - positions: Array of XYZ positions of the site.
            - visual_mag: Array of visual magnitudes.
            - mag_std: Array of magnitude precisions.
    """
    # Read the file content to extract the header
    header_info = {}
    header_lines = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('C'):
                header_lines.append(line.strip())
            else:
                break  # Stop reading at the first non-header line

    # Verify the header format
    if not header_lines[0].strip().startswith('C BEGIN'):
        raise ValueError("{file_path} is not in the correct format: missing BEGIN identifier.")

    # Extract necessary information from the header
    # The format of the GTW-formatted file is as follows:
    # C BEGIN
    # C
    # C 20240829_IPDGTW/AUX/EPH/9511_P202408281011_012346_L0_GEOGC.eph
    # C 20240829_IPDGTW/AUX/POS/9511_P202408281011_012346_L0_GEOGC.pos
    # C 10808 0907  10061 9602 8 0
    # C 20240501080001 20240501080213 132
    # C
    # C
    # 10808 0907  10061 9602 8 0 41 3 20240501 080001250000 289503601 10130193 0000 000 00 0000 000 0 0124 0000 0532 00003056303924 10006497839351 10000074466185 02870168 01122504 000056 0000022557 001240 03231201 03231201 060    9511_P202408291011_012346_20240501080000_L0_GEOGC_000001.ipd
    # ...
    # ...
    # 10808 0907  10061 9602 8 0 41 3 20240501 080213250000 288565810 10142400 0000 000 00 0000 000 0 0124 0000 0532 00003899857605 10006028817986 00000113342740 03317515 01233507 000052 0000022541 001240 03231201 03231201 060    9511_P202408291011_012346_20240501080212_L0_GEOGC_000045.ipd
    # C END

    header_info['ephemeris_filepath'] = header_lines[2][2:]
    header_info['attitude_filepath'] = header_lines[3][2:]

    header_pattern = re.compile(r'\s*(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)')
    header_match = header_pattern.match(header_lines[4][2:])
    if header_match:
        time_system = int(header_match.group(5))
    else:
        raise ValueError("Invalid GTW file header format")
    header_info['time_system'] = time_system

    # Load data section using numpy
    data = np.loadtxt(file_path, comments='C', usecols=(8, 9, 10, 11, 16, 21, 22, 23, 28, 31), dtype=str)

    times, ras, decs, angular_precisions, visual_magnitudes, magnitude_precisions, positions = [], [], [], [], [], [], []

    for row in data:
        ymd, hms, ra, dec, precision, x, y, z, magnitude, magnitude_precision = row

        # Combine date and time
        isot_utc = f"{ymd[:4]}-{ymd[4:6]}-{ymd[6:8]}T{hms[:2]}:{hms[2:4]}:{hms[4:6]}.{hms[6:]}"
        times.append(isot_utc)

        # Format right ascension and declination
        ra_dms = f"{ra[:3]}d{ra[3:5]}m{ra[5:7]}.{ra[7:]}s"
        sign = '-' if dec[0] == '1' else ''
        dec_dms = f"{sign}{dec[1:3]}d{dec[3:5]}m{dec[5:7]}.{dec[7]}s"
        ras.append(ra_dms)
        decs.append(dec_dms)

        # Convert angular precision
        precision_value = float(precision[:2]) * 10**int(precision[2]) * 0.1
        angular_precisions.append(precision_value)

        # Convert visual magnitude
        sign = -1 if magnitude[0] == '1' else 1
        magnitude_value = sign * float(magnitude[1:]) * 0.01
        visual_magnitudes.append(magnitude_value)

        # Convert magnitude precision
        magnitude_precision_value = float(magnitude_precision[:2]) * 10**int(magnitude_precision[2]) * 0.01
        magnitude_precisions.append(magnitude_precision_value)

        # Convert positions
        x_position = convert_position(x)
        y_position = convert_position(y)
        z_position = convert_position(z)
        positions.append((x_position, y_position, z_position))

    t = Time(times)
    if time_system != 0:
        t = t - time_system * u.hour  # Convert local time to UTC

    # Create SkyCoord object for right ascension and declination
    coords = SkyCoord(ra=ras, dec=decs)
    radec = np.stack((coords.ra.deg, coords.dec.deg), axis=1)

    # Return the extracted data as a dictionary
    data_info = {
        'times': t.isot,
        'radec': radec,
        'angular_std': np.array(angular_precisions),
        'positions': np.array(positions)/1e3, # Convert m to km
        'visual_mag': np.array(visual_magnitudes),
        'mag_std': np.array(magnitude_precisions)
    }
    return header_info, data_info

def parse_gtw_file_KD(file_path):
    """
    Parse a GTW-formatted file to extract header information and data.

    The GTW-formatted file contains information about the ephemeris of the site and the angle-only data of the space objects.
    The header section includes metadata, while the data section includes time, position,
    right ascension, declination, angular precision, visual magnitude, etc.

    Usage:
        >>> header_info, data_info = parse_gtw_file('path/to/gtw_file.GTW')
    Inputs:
        file_path -> [str] Path to the GTW-formatted file.
    Outputs:
        header_info -> [dict] Dictionary containing header information.
        data_info -> [dict] Dictionary containing extracted data:
            - times: Time array of observation times.
            - radec: SkyCoord object containing right ascension and declination.
            - angular_std: Array of angular precisions.
            - positions: Array of XYZ positions of the site.
            - visual_mag: Array of visual magnitudes.
            - mag_std: Array of magnitude precisions.
    """
    # Read the file content to extract the header
    header_info = {'time_system':8}
    time_system = 8


    # Load data section using numpy
    data = np.loadtxt(file_path, comments='C', usecols=(8, 9, 10, 11, 16, 22, 23, 24, 29, 32), dtype=str)

    times, ras, decs, angular_precisions, visual_magnitudes, magnitude_precisions, positions = [], [], [], [], [], [], []

    for row in data:
        ymd, hms, ra, dec, precision, x, y, z, magnitude, magnitude_precision = row

        # Combine date and time
        isot_utc = f"{ymd[:4]}-{ymd[4:6]}-{ymd[6:8]}T{hms[:2]}:{hms[2:4]}:{hms[4:6]}.{hms[6:]}"
        times.append(isot_utc)

        # Format right ascension and declination
        ra_dms = f"{ra[:3]}d{ra[3:5]}m{ra[5:7]}.{ra[7:]}s"
        sign = '-' if dec[0] == '1' else ''
        dec_dms = f"{sign}{dec[1:3]}d{dec[3:5]}m{dec[5:7]}.{dec[7]}s"
        ras.append(ra_dms)
        decs.append(dec_dms)

        # Convert angular precision
        precision_value = float(precision[:2]) * 10**int(precision[2]) * 0.1
        angular_precisions.append(precision_value)

        # Convert visual magnitude
        sign = -1 if magnitude[0] == '1' else 1
        magnitude_value = sign * float(magnitude[1:]) * 0.01
        visual_magnitudes.append(magnitude_value)

        # Convert magnitude precision
        magnitude_precision_value = float(magnitude_precision[:2]) * 10**int(magnitude_precision[2]) * 0.01
        magnitude_precisions.append(magnitude_precision_value)

        # Convert positions
        x_position = convert_position(x)
        y_position = convert_position(y)
        z_position = convert_position(z)
        positions.append((x_position, y_position, z_position))

    t = Time(times)
    if time_system != 0:
        t = t - time_system * u.hour  # Convert local time to UTC

    # Create SkyCoord object for right ascension and declination
    coords = SkyCoord(ra=ras, dec=decs)
    radec = np.stack((coords.ra.deg, coords.dec.deg), axis=1)

    # Return the extracted data as a dictionary
    data_info = {
        'times': t.isot,
        'radec': radec,
        'angular_std': np.array(angular_precisions),
        'positions': np.array(positions)/1e3, # Convert m to km
        'visual_mag': np.array(visual_magnitudes),
        'mag_std': np.array(magnitude_precisions)
    }
    return header_info, data_info        
