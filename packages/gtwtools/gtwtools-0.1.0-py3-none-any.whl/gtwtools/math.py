import numpy as np
from numpy.linalg import norm

TWOPI = 2 * np.pi

def spherical_to_cartesian(ra, dec, r,degrees=True):
    """
    Convert spherical coordinates (right ascension, declination, distance) to Cartesian coordinates.

    Inputs:
        ra -> [array-like] Right ascension in degrees or radians.
        dec -> [array-like] Declination in degrees or radians.
        r -> [array-like] Distance from the origin.
        degrees -> [bool, optional, default=True] Specifies if right ascension and declination are in degrees.
        If False, angles are in radians.
    Outputs:
        xyz -> [array-like] Cartesian coordinates as an array of shape (3,) or (N, 3).
    """
    if degrees:
        ra = np.radians(ra)
        dec = np.radians(dec)

    x = r * np.cos(dec) * np.cos(ra)
    y = r * np.cos(dec) * np.sin(ra)
    z = r * np.sin(dec)

    return np.stack([x,y,z]).T

def cartesian_to_spherical(x, y, z, degrees=True):
    """
    Convert Cartesian coordinates to spherical coordinates (right ascension, declination, distance).

    Inputs:
        x -> [array-like] X coordinate.
        y -> [array-like] Y coordinate.
        z -> [array-like] Z coordinate.
        degrees -> [bool, optional, default=True] Specifies if the output right ascension and declination are in degrees.
        If False, angles are in radians.
    Outputs:
        ra_dec_r -> [array-like] Spherical coordinates as an array of shape (3,) or (N, 3).
    """
    r = np.sqrt(x ** 2 + y ** 2 + z ** 2)
    ra = np.arctan2(y, x) % TWOPI # normalize RA to [0, 2pi)
    dec = np.arcsin(z / r)

    if degrees:
        ra = np.degrees(ra)
        dec = np.degrees(dec)

    return np.stack([ra,dec,r]).T

def slant(r,los_vec,R_vec):
    """
    Calculate the slant distance of the space object w.r.t. the site.

    usage:
        >>> rho,r_vec = slant(r,los_vec,R_vec)
    Inputs:
        r -> [array_like] Distance to the central attractor
        los_vec -> [array_like] Unit vector of the Line-Of-Sight(LOS) from the site to the space object
        R_vec -> [array_like] Position vector of the site
    Outputs:
        rho -> [array_like] Slant distance of the space object w.r.t. the site
        r_vec -> [array_like] Position vector of the space object
    """
    if R_vec.ndim == 1:
        R = norm(R_vec)
        C = 2*np.dot(los_vec,R_vec)
        q = C**2 - 4*(R**2 - r**2)
        if q < 0: q = 0
        rho = (-C + np.sqrt(q))/2
        r_vec = rho*los_vec + R_vec
    else:
        R = norm(R_vec,axis=1)
        C = 2*(los_vec * R_vec).sum(axis=1)
        q = C**2 - 4*(R**2 - r**2)
        q[q < 0] = 0
        rho = (-C + np.sqrt(q))/2
        r_vec = rho[:,None]*los_vec + R_vec
    return rho,r_vec

def slerp_radec(times, radec, interp_times):
    """
    Interpolate right ascension (RA) and declination (Dec) using SLERP.

    This function also supports extrapolation.
    If the requested `interp_times` include values outside the range of the original `times`, the function will extrapolate based on the direction defined by the first or last interval of data.
    The extrapolated values assume that the motion or change in RA and Dec continues in the same manner as defined by the first or last two data points.
    Extrapolation is handled automatically without additional parameters.

    Inputs:
        times -> [array-like,float] Original time series corresponding to the measurements of RA and Dec, with shape of (N,).
        radec -> [array-like,float] Measured RA and Dec values at the times in `times` (units: degrees), with shape of (N, 2).
        interp_times -> [array-like,float] Array of time points where interpolation is desired, with shape of (M,).
    Outputs:
        radec_interp -> [array-like,float] Interpolated RA and Dec values at `interp_times` (units: degrees), with shape of (M, 2).
        The first column is RA, and the second column is Dec.
    """
    # Ensure the time series is in ascending order
    if not np.all(np.diff(times) >= 0):
        raise ValueError("times array must be in ascending order.")

    # Convert spherical coordinates to Cartesian unit vectors
    vectors = spherical_to_cartesian(radec[:,0], radec[:,1], 1)  # Shape: (N, 3)

    # Find the indices for each interpolation time
    indices = np.searchsorted(times, interp_times) - 1
    indices = np.clip(indices, 0, len(times) - 2)

    # Get the starting and ending vectors for each interval
    v0 = vectors[indices]          # Shape: (M, 3)
    v1 = vectors[indices + 1]      # Shape: (M, 3)

    # Compute the normalized interpolation parameter t in [0, 1]
    t0 = times[indices]
    t1 = times[indices + 1]
    delta_t = t1 - t0
    t = (interp_times - t0) / delta_t  # Normalize to [0, 1]
    t = t[:, np.newaxis]  # Shape: (M, 1)

    # Compute the dot product and clip to handle numerical errors
    dot_product = np.sum(v0 * v1, axis=1, keepdims=True)
    dot_product = np.clip(dot_product, -1.0, 1.0)

    # Compute the angle theta between vectors
    theta = np.arccos(dot_product)  # Shape: (M, 1)

    # Compute sin(theta)
    sin_theta = np.sin(theta)

    # Handle small angles to avoid division by zero
    small_theta = theta < 1e-8  # Threshold for small angles
    sin_theta[small_theta] = 1.0  # Prevent division by zero

    # Compute interpolation coefficients
    s0 = np.sin((1 - t) * theta) / sin_theta  # Shape: (M, 1)
    s1 = np.sin(t * theta) / sin_theta        # Shape: (M, 1)

    # For small angles, use linear interpolation coefficients
    s0[small_theta] = 1 - t[small_theta]
    s1[small_theta] = t[small_theta]

    # Perform the interpolation
    slerp_vectors = s0 * v0 + s1 * v1  # Shape: (M, 3)

    # Normalize the interpolated vectors
    slerp_vectors /= np.linalg.norm(slerp_vectors, axis=1, keepdims=True)

    # Convert back to spherical coordinates (RA and Dec)
    x, y, z = slerp_vectors.T
    radec_interp = cartesian_to_spherical(x, y, z)[:,:-1]

    return radec_interp
