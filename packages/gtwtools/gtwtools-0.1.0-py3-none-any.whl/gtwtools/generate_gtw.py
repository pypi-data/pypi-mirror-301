import os
import numpy as np
from numpy.linalg import norm
from astropy.time import Time,TimeDelta
from starmatch import StarMatch

from .read_ipd import parse_ipd_file,parse_ipd_dir
from .interpolate import read_eph,read_att,interpolate_eph,interpolate_radec
from .frame_trans import DF_ECI_mat
from .math import cartesian_to_spherical,spherical_to_cartesian,slant
from .fmt_gtw import *
from .params_config import load_params

light_speed = 299792.458 # Speed of light in km/s

def generate_gtw_files(ipd_directory, GTW_dir, RES_dir, eph_path, att_path,publisher="10808", yymm='0907' ,device_id=9602, time_system=8, coord_system=0, measurement_status=0, wavelength=532):
    """
    This function processes IPD files to extract observation times and star/satellite data,
    aligns the star data with a simplified star catalog, calculates the orientation of the camera,
    and writes the results into GTW files.

    Inputs:
        ipd_directory -> [str] Directory containing IPD files.
        GTW_dir -> [str] Directory to save the generated GTW files.
        RES_dir -> [str] Directory to save the intermediate result files.
        eph_path -> [str] Path to the ephemeris file.
        att_path -> [str] Path to the attitude file.
        publisher -> [str,optional,default='10808'] Publisher identifier.
        yymm -> [str,optional,default='0907'] The activation date of the GTW format (default: '0907').
        device_id -> [int,optional,default='9602'] Device identifier (default: 9602).
        time_system -> [int,optional,default=8] Time system identifier (default: 8).
        coord_system -> [int,optional,default=0] Coordinate system identifier (default: 0).
        measurement_status -> [int,optional,default=0] Measurement status identifier (default: 0).
        wavelength -> [int,optional,default=532] Wavelength in optical data in nanometers (default: 532).
    """

    # Extract valid IPD files and observation times
    ipd_files, t_array = parse_ipd_dir(ipd_directory)
    ta_array = Time(t_array)

    # Loads configuration parameters from a YAML file.
    params = load_params('config.yaml')

    # If there are multiple camera configuration files, you can uncomment and adjust the following code according to the actual situation.
    """
    if 'GY' in ipd_files[0]:
        params = load_params('config_gy.yaml')
    elif 'JG' in ipd_files[0]:
        params = load_params('config_jg.yaml')
    else:
        raise Exception('IPD files are inconsistent with the parameter configuration file.')
    """

    # Controls whether to perform the reverse aberration correction(from the apparent position to the true position) during the light travel.
    aberration_inverse_correction = params['ABERRATION_INVERSE_CORRECTION']
    astrometry_corrections = params['ASTROMETRY_CORRECTIONS']

    # Adjust for time zone offset
    if time_system:
        tz_offset = TimeDelta(time_system * 3600, format='sec')
        t_utc = ta_array - tz_offset
    else:
        t_utc = ta_array

    # Read ephemeris and attitude data
    att_mode = 'radec' # Also 'euler,' and 'quaternion'
    times_eph, positions, velocities = read_eph(eph_path)
    times_att, att_params = read_att(att_path, att_mode)

    # Interpolate positions of platform and attitudes of camera
    platform_coords, platform_vels = interpolate_eph(times_eph, positions, velocities, t_array)
    camera_atts = interpolate_radec(times_att, att_params, t_array)

    # Calculate the camera orientation
    fp_radecs = calculate_orientation(camera_atts, att_mode)

    # Ensure the output directory exists
    if not os.path.exists(RES_dir): os.makedirs(RES_dir)
    if not os.path.exists(GTW_dir): os.makedirs(GTW_dir)

    all_sate_data = {}
    fp_calibrated = []

    # Set the file name and storage path of the intermediate result file
    res_file_name = f'{ipd_files[0].split('_')[3]}.ICR' # Internal Consistency Results
    res_file_path = os.path.join(RES_dir, res_file_name)

    # Save intermediate results
    with open(res_file_path, 'w') as res_file:

        # Process each IPD file
        for j,ipd_file in enumerate(ipd_files):
            file_path = os.path.join(ipd_directory, ipd_file)
            header, star_data, sate_data = parse_ipd_file(file_path)

            # Perform astrometric positioning
            astrometry_corrections['t'] = t_utc[j]
            # Check if 'aberration' exists in astrometry_corrections
            if 'aberration' in astrometry_corrections:
                astrometry_corrections['aberration'] = platform_vels[j]
            results = astro_positioning(star_data,sate_data,fp_radecs[j],astrometry_corrections,params)
            fp_calibrated.append(results['fp_calibrated'])

            # Write intermediate results to a file
            res_file.write(f"{ipd_file}\n")
            res_file.write(f"{results['catalog_df']}\n")
            res_file.write(f"fp_calibrated: {results['fp_calibrated']}\n")
            res_file.write(f"xy_rms: {results['xy_rms']}\n")
            res_file.write(f"radec_rms: {results['radec_rms']}\n")
            res_file.write(f"mag_rms: {results['mag_rms']}\n\n")

            # Collect results related to space objects
            for i, txh in enumerate(header['SATEOBJ_TXH']):
                if txh not in all_sate_data:
                    all_sate_data[txh] = []

                all_sate_data[txh].append({
                    'index': j,
                    'time': ta_array[j],
                    'ipd_file': ipd_file,
                    'mag': results['mag'][i],
                    'mag_std': results['mag_std'][i],
                    'ra': results['ra'][i],
                    'dec': results['dec'][i],
                    'radec_std': results['radec_std'][i],
                    'x': sate_data['x'][i],
                    'y': sate_data['y'][i],
                    'pixel_count': sate_data['pixel_count'][i],
                    'net_grayscale': sate_data['net_grayscale'][i],
                    'background_mean': sate_data['background_mean'][i],
                    'background_variance': sate_data['background_variance'][i]
                })

    # Write GTW files
    for txh, data in all_sate_data.items():
        t_start_obj = data[0]['time']
        t_end_obj = data[-1]['time']
        t_start = t_start_obj.strftime('%Y%m%d%H%M%S')
        t_end = t_end_obj.strftime('%Y%m%d%H%M%S')
        delta_t = round((t_end_obj - t_start_obj).sec)
        txh_formatted = f'{txh:06d}'
        gtw_file_name = f'{t_start}_{txh_formatted}_{device_id}.GTW'
        gtw_file_path = os.path.join(GTW_dir, gtw_file_name)
        with open(gtw_file_path, 'w') as gtw_file:
            # Write the start identifier
            gtw_file.write('C BEGIN\nC\n')
            gtw_file.write(f'C {eph_path}\n')
            gtw_file.write(f'C {att_path}\n')

            # set the header field
            head_field = f"{publisher:>5} {yymm:>4} {txh:>6} {device_id:>4} {time_system:>1} {coord_system:>1}"
            gtw_file.write(f'C {head_field}\n')

            # Write the start and end time and duration (in seconds) of the observation arc segment
            gtw_file.write(f'C {t_start} {t_end} {delta_t}\n')
            gtw_file.write('C\nC\n')
            
            # Write the data entries
            for entry in data:
                seq = entry['index']
                ra, dec = entry['ra'], entry['dec']

                if aberration_inverse_correction:
                    los_vec = spherical_to_cartesian(ra, dec, 1)  # Calculate the orientation of the target relative to the platform
                    rho, r_vec = slant(params['a'], los_vec, platform_coords[seq])  # Calculate the distance of the target relative to the platform in [km]
                    light_time = rho / light_speed # Calculate the light time in seconds
                    t_offset = TimeDelta(light_time, format='sec')
                    t_lt = ta_array[seq:seq+1] - t_offset
                    platform_coords_lt, platform_vels_lt = interpolate_eph(times_eph, positions, velocities, t_lt)
                    platform_x, platform_y, platform_z = platform_coords_lt.squeeze() * 1e3  # convert km to m
                else:
                    t_lt = entry['time']
                    platform_x, platform_y, platform_z = platform_coords[seq] * 1e3  # convert km to m

                date = t_lt.squeeze().to_datetime()
                ymd = date.strftime('%Y%m%d')
                hms = date.strftime('%H%M%S%f')
                ra_fmt = format_ra(ra)
                dec_fmt = format_dec(dec)
                data_field = f" 41 3 {ymd:>8} {hms:>12} {ra_fmt:>9} {dec_fmt:>8} 0000 000 00 0000"
                gtw_file.write(head_field + data_field)
                
                # Write the REF field
                angular_precision = format_precision(entry['radec_std'], scale=0.1)
                magnitude = format_signal(entry['mag'])
                ref_field = f" {angular_precision:>3} {measurement_status:>1} {magnitude:>4} 0000 {format_wavelength(wavelength)}"
                gtw_file.write(ref_field)

                # Write the photometry field
                photometry_field = (
                    f" {format_position(platform_x)}"
                    f" {format_position(platform_y)}"
                    f" {format_position(platform_z)}"
                    f" {format_pixel_xy(entry['x'])}"
                    f" {format_pixel_xy(entry['y'])}"
                    f" {entry['pixel_count']:>06}"
                    f" {round(entry['net_grayscale']):>010}"
                    f" {format_mag(entry['mag'])}"
                    f" {format_photometry(entry['background_mean'])}"
                    f" {format_photometry(entry['background_variance'])}"
                    f" {format_precision(entry['mag_std'], scale=0.01)}"
                    f" {entry['ipd_file']:>63}\n"
                )
                gtw_file.write(photometry_field)
            # Write the end identifier
            gtw_file.write('C END\n')    

def calculate_orientation(rotation_params,mode,degrees=True):
    """
    This function calculates the orientation of the camera by converting the orientation
    vectors from the DF (Detector Frame) to the ECI (Earth-Centered Inertial) frame and then
    converting these vectors to spherical coordinates (RA and Dec).

    Inputs:
        rotation_params -> [1D/2D array-like] 3-element angles for mode 'euler', 4-element quaternions for mode 'quaternion', even directly the orientation of the camera.
        mode -> [str] Specifies the type of rotation:
            - 'euler' or like 'euler-xyz': the general euler rotation transform from DF to ECI is applied.
            - 'quaternion': each row is a (possibly non-unit norm) quaternion in form of (x, y, z, w). The quaternion is applied from DF to ECI.
            - 'radec': No calculation required, output results directly.
        degrees -> [bool,optional,default=True] If True, the angles are assumed to be in degrees.
    Outputs:
        fp_radec -> [numpy.ndarray] Array of RA and Dec representing the camera's orientation in the ECI frame.
    """
    if mode != 'radec':
        # Calculate the rotation matrices between DF and ECI frames
        DF2ECI_mat,ECI2DF_mat = DF_ECI_mat(rotation_params,mode,degrees)
        # Extract the orientation vectors in the ECI frame
        orients_ECI = DF2ECI_mat[:,:,-1]
        # Convert the orientation vectors to spherical coordinates (RA, Dec, r)
        camera_orientation = cartesian_to_spherical(orients_ECI[:,0],orients_ECI[:,1],orients_ECI[:,2])
        # Extract the RA and Dec from the spherical coordinates
        fp_radec = camera_orientation[:,:2]
    else:
        fp_radec = rotation_params

    return fp_radec

def astro_positioning(star_data,sate_data,fp_radec,astrometry_corrections,params):
    """
    The function aligns the observed star positions with a simplified star catalog and applies
    affine/similarity transformations and distortion calibration to determine the positions and
    relative photometry technique to estimate apparent magnitudes of satellites.

    Inputs:
        star_data -> [dict] Dictionary containing star data:
            - 'x': X coordinates of stars.
            - 'y': Y coordinates of stars.
            - 'net_grayscale': Grayscale values of stars.
        sate_data -> [dict] Dictionary containing satellite data:
            - 'x': X coordinates of satellites.
            - 'y': Y coordinates of satellites.
            - 'net_grayscale': Grayscale values of satellites.
        fp_radec -> [2d array] Initial orientation of camera in form of (Ra, Dec) in degrees.
        astrometry_corrections -> [dict] Dictionary specifying the types of corrections to apply.
                - 't' -> [str] Observation time in UTC, such as '2019-02-26T20:11:14.347'.
                   It specifies the time at which corrections are to be applied.
                - 'proper-motion' -> [None] If present, apply proper motion correction.
                   This term corrects for the motion of stars across the sky due to their velocities.
                - 'aberration' -> [tuple] Aberration correction parameters. Observer's velocity relative to Earth's center (vx, vy, vz) in km/s.
                   This term corrects for the apparent shift in star positions due to the motion of the observer.
                - 'parallax' -> [None] If present, apply parallax correction.
                   This term corrects for the apparent shift in star positions due to the change in observer's viewpoint as the Earth orbits the Sun.
                - 'deflection' -> [None] If present, apply light deflection correction.
                   This term corrects for the bending of light from stars due to the gravitational field of the Sun, based on general relativity.
        params -> [dict] A dictionary containing processed configuration parameters, including camera settings, star catalog data, and correction flags.
    Outputs:
        results -> [dict] Dictionary containing the calculated positions and magnitudes of satellites:
            - 'ra': Right ascension of targets in degrees.
            - 'dec': Declination of targets in degrees.
            - 'mag': Apparent Magnitudes of targets.
            - 'radec_std': Standard deviation of RA and Dec in degrees.
            - 'mag_std': Standard deviation of magnitudes.
    """
    # Retrieve camera parameters and simplified star catalog
    camera_params = params['CAMERA_PARAMS']
    simplified_catalog = params['SC_SIMPLIFIED']

    # Retrieve the mode of geometric invariants used in similarity transformation
    mode_invariants = params['MODE_INVARIANTS']

    # Retrieve the method for distortion calibration
    distortion_calibrate = params['DISTORTION_CALIBRATE']

    # Extract star data
    x = star_data['x']
    y = star_data['y']
    xy = np.stack((x, y), axis=1)
    flux = star_data['net_grayscale']

    # Extract satellite data
    x_target = sate_data['x']
    y_target = sate_data['y']
    xy_target = np.stack((x_target, y_target), axis=1)
    flux_target = sate_data['net_grayscale']

    num_target = len(flux_target)

    # Use the first 30 brightest points to compute the triangle invariants for similarity transformation
    sources = StarMatch.from_sources(xy, camera_params,flux_raw=flux,mode_invariants=mode_invariants)  # No distortion corrected
    sources.align(fp_radec,simplified_catalog,L=150,astrometry_corrections=astrometry_corrections,distortion_calibrate=distortion_calibrate)

    # Center pointing calibration
    sources.fp_calibrate()
    fp_calibrated = sources.fp_radec_calibrated

    catalog_df = sources.calibrated_results.catalog_df

    # Apply transformations to satellite data to obtain positions and magnitudes
    radec, M_affine, M_match = sources.apply(xy_target, flux_target)

    # Uncomment to show plot of distortion
    # sources.show_distortion('contourf')
    # sources.show_distortion('vector')

    # Calculate RMS errors
    xy_rms = sources.calibrated_results.xy_rms
    radec_rms = sources.calibrated_results.radec_rms
    mag_rms = sources.calibrated_results.mag_rms
    radec_rms_norm = norm(radec_rms)

    # Prepare results dictionary
    results = {
        'ra': radec[:, 0], # Right ascension of space objects in degrees
        'dec': radec[:, 1], # Declination of space objects in degrees
        'mag': M_match, # Apparent magnitude of space objects
        'xy_rms': xy_rms,  # Mean square error of pixel coordinates for star map matching
        'radec_rms': radec_rms, # Mean square error of celestial coordinates for star map matching
        'mag_rms': mag_rms, # Mean square error of magnitudes for relative photometry
        'radec_std': [radec_rms_norm] * num_target, # Mean square error of celestial coordinates for multiple space objects in the same frame
        'mag_std': [mag_rms] * num_target, # Mean square error of magnitudes for multiple space objects in the same frame
        'fp_calibrated': fp_calibrated, # Calibrated center pointing in form of [Ra,Dec] in degrees
        'catalog_df': catalog_df # Star catalog information used for star map matching
    }
    return results

