import yaml
from starcatalogquery import StarCatalog

def load_params(config_file_path):
    """
    Loads configuration parameters from a YAML file.

    Inputs:
        config_file_path -> [str] Path to the configuration YAML file.
    Outputs:
        params -> [dict] A dictionary containing processed configuration parameters, including camera settings, star catalog data, and correction flags.
    """
    # Read the configuration file
    with open(config_file_path, 'r') as config_file:
        config = yaml.safe_load(config_file)

    # Configure camera parameters
    FOV = tuple(config['FOV'])  # Field of View (FOV) in degrees
    PIXEL_WIDTH = config['PIXEL_WIDTH']  # Pixel width in degrees
    WIDTH = config['WIDTH']  # Width of the camera resolution
    HEIGHT = config['HEIGHT']  # Height of the camera resolution
    CAMERA_PARAMS = {'fov': FOV, 'pixel_width': PIXEL_WIDTH, 'res': (HEIGHT, WIDTH)}

    # Load the star catalog file
    DIR_FROM_SIMPLIFIED = config['DIR_FROM_SIMPLIFIED']
    SC_SIMPLIFIED = StarCatalog.load(DIR_FROM_SIMPLIFIED)

    # Mode of geometric invariants
    MODE_INVARIANTS = config['MODE_INVARIANTS']

    # Method for distortion calibration
    DISTORTION_CALIBRATE = config.get('DISTORTION_CALIBRATE')

    # Switches for astrometry corrections
    astrometry_corrections = config.get('ASTROMETRY_CORRECTIONS')
    ASTROMETRY_CORRECTIONS = {key: value for key, value in astrometry_corrections.items() if value}

    # Semi-major axis of the target orbit in kilometers
    a = config['a']

    # Switch for inverse aberration correction during light travel
    ABERRATION_INVERSE_CORRECTION = config['ABERRATION_INVERSE_CORRECTION']

    # Return all parameters
    return {
        'config': config,
        'FOV': FOV,
        'PIXEL_WIDTH': PIXEL_WIDTH,
        'WIDTH': WIDTH,
        'HEIGHT': HEIGHT,
        'CAMERA_PARAMS': CAMERA_PARAMS,
        'DIR_FROM_SIMPLIFIED': DIR_FROM_SIMPLIFIED,
        'SC_SIMPLIFIED': SC_SIMPLIFIED,
        'MODE_INVARIANTS': MODE_INVARIANTS,
        'DISTORTION_CALIBRATE': DISTORTION_CALIBRATE,
        'ASTROMETRY_CORRECTIONS': ASTROMETRY_CORRECTIONS,
        'a': a,
        'ABERRATION_INVERSE_CORRECTION': ABERRATION_INVERSE_CORRECTION
    }