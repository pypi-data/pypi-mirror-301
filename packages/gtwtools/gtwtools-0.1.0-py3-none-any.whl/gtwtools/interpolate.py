import numpy as np
from astropy.time import Time
from scipy.interpolate import interpn
from scipy.spatial.transform import Slerp,Rotation as R

from .math import slerp_radec

def calculate_relative_times(times, interp_times):
    """
    Calculate the relative time differences of two time arrays with respect to the first time point.

    Usage:
        >>> times = ["2024-07-01T00:00:00", "2024-07-01T01:00:00"]
        >>> interp_times = ["2024-07-01T00:30:00", "2024-07-01T01:30:00"]
        >>> delta_t, delta_t_interp = calculate_relative_times(times, interp_times)
    Inputs:
        times -> [array-like] Original time array, with shape of (N,).
        interp_times -> [array-like] Time array for interpolation, with shape of (M,).
    Outputs:
        delta_t -> [array-like] Relative time differences of the original time array, with shape of (N,).
        delta_t_interp -> [array-like] Relative time differences of the time array for interpolation, with shape of (M,).
    """
    t = Time(times)  # Ignoring time zones
    t_interp = Time(interp_times)
    delta_t = (t - t[0]).value
    delta_t_interp = (t_interp - t[0]).value
    return delta_t, delta_t_interp

def interpolate_eulers(times, angles, interp_times):
    """
    Interpolate Euler angles using cubic interpolation.

    Inputs:
        times -> [array-like] Original time array, with shape of (N,).
        angles -> [array-like] Euler angles, with shape of (N, 3).
        interp_times -> [array-like] Time array for interpolation, with shape of (M,).
    Outputs:
        interp_angles -> [array-like] Interpolated Euler angles, with shape of (M, 3).
    """
    # Calculate the relative time differences
    delta_t, delta_t_interp = calculate_relative_times(times, interp_times)

    # Perform cubic interpolation in a multi-dimensional space
    interp_angles = interpn((delta_t,), angles, delta_t_interp, method='cubic')

    return interp_angles

def interpolate_quaternions(times, quaternions, interp_times):
    """
    Perform spherical linear interpolation (SLERP) on quaternions.
    SLERP describes an interpolation (with constant angular velocity) along the shortest path (a.k.a. geodesic) on the unit hypersphere between two quaternions.

    Inputs:
        times -> [array-like] Original time array, with shape of (N,).
        quaternions -> [array-like] Quaternions, with shape of (N, 4).
        interp_times -> [array-like] Time array for interpolation, with shape of (M,).
    Outputs:
        interp_quaternions -> [array-like] Interpolated Quaternions, with shape of (M, 4).
    """
    # Calculate the relative time differences
    delta_t, delta_t_interp = calculate_relative_times(times, interp_times)

    # Create a Slerp object for interpolation
    rotations = R.from_quat(quaternions)
    slerp = Slerp(delta_t, rotations)

    # Perform interpolation
    interp_rotations = slerp(delta_t_interp)

    # Retrieve interpolated quaternions
    interp_quaternions = interp_rotations.as_quat()

    return interp_quaternions

def interpolate_radec(times, radec, interp_times):
    """
    Interpolate right ascension (RA) and declination (Dec) using SLERP.

    This function also supports extrapolation.
    If the requested `interp_times` include values outside the range of the original `times`, the function will extrapolate based on the direction defined by the first or last interval of data.
    The extrapolated values assume that the motion or change in RA and Dec continues in the same manner as defined by the first or last two data points.
    Extrapolation is handled automatically without additional parameters.

    Usage:
        >>> times = ["2024-07-01T00:00:00", "2024-07-01T01:00:00","2024-07-01T02:00:00"]
        >>> interp_times = ["2024-07-01T00:30:00", "2024-07-01T01:30:00"]
        >>> radec = [[293,0.5],[290,0.8],[287,1.1]]
        >>> radec_interp = interpolate_radec(times, radec, interp_times)

    Inputs:
        times -> [array-like,str] Original time series corresponding to the measurements of RA and Dec, with shape of (N,).
        radec -> [array-like,float] Measured RA and Dec values at the times in `times` (units: degrees), with shape of (N, 2).
        interp_times -> [array-like,str] Array of time points where interpolation is desired, with shape of (M,).
    Outputs:
        radec_interp -> [array-like,float] Interpolated RA and Dec values at `interp_times` (units: degrees), with shape of (M, 2).
        The first column is RA, and the second column is Dec.
    """
    # Calculate the relative time differences
    delta_t, delta_t_interp = calculate_relative_times(times, interp_times)
    radec_interp = slerp_radec(delta_t, radec, delta_t_interp)

    return radec_interp

def interpolate_eph(times, coordinates, velocities, interp_times):
    """
    Interpolate XYZ coordinates and velocities using cubic interpolation.

    Inputs:
        times -> [array-like] Original time array, with shape of (N,).
        coordinates -> [array-like] Original XYZ coordinates, with shape of (N, 3).
        velocities -> [array-like] Original velocities, with shape of (N, 3).
        interp_times -> [array-like] Time array for interpolation, with shape of (M,).
    Outputs:
        interp_coordinates -> [array-like] Interpolated XYZ coordinates, with shape of (M, 4).
        interp_velocities -> [array-like] Interpolated velocities, with shape of (M, 4).
    """
    delta_t, delta_t_interp = calculate_relative_times(times, interp_times)
    # Perform cubic interpolation in a multi-dimensional space
    interp_coordinates = interpn((delta_t,), coordinates, delta_t_interp, method='cubic')
    interp_velocities = interpn((delta_t,), velocities, delta_t_interp, method='cubic')
    
    return interp_coordinates, interp_velocities

def read_eph(file_path):
    """
    Read an ephemeris file, extracting time, position, and velocity data.

    Usage:
        >>> file_path = 'path/to/eph_file.EPH'
        >>> times, positions, velocities = read_eph(file_path)
    Inputs:
        file_path -> [str] Path to the EPH file.
    Outputs:
        times -> [array-like] ISO times, such as ["2024-07-01T00:00:00", "2024-07-01T01:00:00"].
        positions -> [array-like] XYZ coordinates in km, with shape of (N, 3).
        velocities -> [array-like] Velocities in km/s, with shape of (N, 3).
    """
    # Use numpy to read the file, skipping the header
    data = np.loadtxt(file_path, dtype=str)

    # Extract columns
    times = data[:, 0]
    positions = data[:, 1:4].astype(float)/1e3 # Convert m to km
    velocities = data[:, 4:7].astype(float)/1e3 # Convert m/s to km/s
    
    return times, positions, velocities

def read_att(file_path,mode):
    """
    Read an attitude file and extract time, quaternion, Euler angles, or optical axis pointing (formatted as Ra and Dec) data.

    Usage:
        >>> file_path = 'path/to/att_file.ATT'
        >>> times, quaternions = read_att(file_path, 'quaternion')
        >>> times, euler_angles = read_att(file_path, 'euler')
        >>> times, radecs = read_att(file_path, 'radec')
    Inputs:
        file_path -> [str] Path to the ATT file.
        mode -> [str] The type of attitudes ('quaternion', 'euler', or 'radec').
    Outputs:
        times -> [array-like] ISO times, such as ["2024-07-01T00:00:00", "2024-07-01T01:00:00"].
        quaternions -> [array-like] Quaternions, with shape of (N, 4).
        euler_angles -> [array-like] Euler angles, with shape of (N, 3).
        radecs -> [array-like]  Right ascension and Declination, with shape of (N, 2).
    """
    # Use numpy to read the file, skipping the header
    data = np.loadtxt(file_path, dtype=str)

    # Extract columns
    times = data[:, 0]
    if mode == "quaternion":
        quaternions = data[:, 1:5].astype(float)
        return times, quaternions
    elif "euler" in mode:
        euler_angles = data[:, 1:4].astype(float)
        return times, euler_angles
    elif mode == "radec":
        radecs = data[:, -2:].astype(float)
        return times, radecs
    else:
        raise ValueError(f"{mode} must be one of 'quaternion', 'euler' or 'radec'.")

