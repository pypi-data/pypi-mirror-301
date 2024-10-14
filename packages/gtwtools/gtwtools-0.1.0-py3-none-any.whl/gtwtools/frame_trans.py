import numpy as np
from scipy.spatial.transform import Rotation
def Rot(seq, angles, degrees=True):
    """
    Rotate a reference frame around a sequence of axes.
    Note: The Rot is noly suitable for a right-handed reference frame !!

    Usage:
        >>> seq = 'XY'
        >>> angles = [60,30]
        >>> rotation_matrix = Rot(seq,angles)
    Inputs:
        seq -> [str] Sequence of axes for rotation, such as 'Z' or 'XY'.
        angles -> [float,list of float] Rotation angles in [rad] or [deg]
        degrees -> [bool,optional,default=True] If True, the rotation angles are assumed to be in degrees
    Outputs:
        rotation_matrix -> [2D array of 3x3] Rotation matrix from the source reference frame to the target reference frame.
    """
    if np.isscalar(angles):
        rotation_matrix = Rotation.from_euler(seq, angles, degrees).as_matrix().T
    else:
        angles = np.array(angles)
        if len(seq) > 1:
            if angles.ndim == 1:
                rotation_matrix = Rotation.from_euler(seq, angles, degrees).as_matrix().T
            elif angles.ndim == 2:
                rotation_matrix = Rotation.from_euler(seq, angles, degrees).as_matrix().transpose(0, 2, 1)
        else:
            rotation_matrix = Rotation.from_euler(seq, angles, degrees).as_matrix().transpose(0, 2, 1)

    return rotation_matrix
def DF_ECI_mat(rotation_params, mode, degrees=True):
    """
    Compute the rotation matrix between the Device-Fixed (DF) reference frame and the Earth-Centered Inertial (ECI) reference frame.

    Usage:
        >>> rotation_params,mode = [20,30,40],'euler' # [[20,30,40],[50,60,70]], 'euler-XYZ'
        >>> rotation_params,mode = [2,3,4,5], 'quaternion' # [[2,3,4,5],[6,7,8,9]]
        >>> DF2ECI_mat,ECI2DF_mat = DF_ECI_mat(rotation_params,mode)
    Inputs:
        rotation_params -> [1D/2D array-like] 3-element angles for mode 'euler', or 4-element quaternions for mode 'quaternion'
        mode -> [str] Specifies the type of rotation:
            - 'euler' or like 'euler-XYZ': the general euler rotation transform from DF to ECI is applied
            - 'quaternion': each row is a (possibly non-unit norm) quaternion in form of (x, y, z, w). The quaternion is applied from DF to ECI.
        degrees -> [bool,optional,default=True] If True, the angles are assumed to be in degrees.
    Outputs:
        DF2ECI_mat -> [2D/3D array-like] Rotation matrix from DF to ECI with shape (3,3) or (n,3,3)
        ECI2DF_mat -> [2D/3D array-like] Rotation matrix from ECI to DF with shape (3,3) or (n,3,3)
    Note:
        The general "Euler angles" have twelve possible sequences of rotation axes, divided in two groups:
            - Proper Euler angles (ZXZ, XYX, YZY, ZYZ, XZX, YXY)
            - Tait–Bryan angles (XYZ, YZX, ZXY, XZY, ZYX, YXZ).
        where, the first group is called proper or classic Euler angles, and the second group is called Tait–Bryan angles.
        The sequence 'ZYX'(yaw, pitch, and roll) is commonly used in aerospace.
        In this program, the set {'X', 'Y', 'Z'} is for intrinsic rotations by default, and {'x', 'y', 'z'} for extrinsic rotations.
        Extrinsic and intrinsic rotations cannot be mixed in one function call.
    """
    rotation_params = np.array(rotation_params)
    if '-' in mode:
        _type,_seq = mode.split('-')
    else:
        _type,_seq = mode,'ZXZ' # Default to 'ZXZ' sequence for classic Euler rotation if no hyphen is found

    if _type == 'euler':
        DF2ECI_mat = Rot(_seq, rotation_params, degrees=degrees)
    elif _type == 'quaternion':
        DF2ECI_mat = Rotation.from_quat(rotation_params).as_matrix()
    else:
        raise ValueError(f"'{mode}' must be in ['euler','quaternion']")

    DF2ECI_mat_ndim = DF2ECI_mat.ndim
    if DF2ECI_mat_ndim == 2:
        ECI2DF_mat = DF2ECI_mat.T
    elif DF2ECI_mat_ndim == 3:
        ECI2DF_mat = DF2ECI_mat.transpose(0, 2, 1)

    return DF2ECI_mat,ECI2DF_mat