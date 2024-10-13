from typing import Any
from json import load as jload
from numpy import array as npArray


def load_calibration(calibrationParamsPath: str) -> dict[str, Any]:
    """
    Load the camera calibration from specified JSON file

    :param str calibrationParamsPath: Path to the JSON calibration file
    :return dict[str, Any]: Returns calibration parameters of the camera:

        `mse` - Mean Square Error,

        `rms` - The overall RMS re-projection error in floating number format,

        `cameraMatrix` - Camera Matrix, the focal length and optical centre matrix as shown in intrinsic parameters,

        `distortionCoefficients` - Distortion Coefficients: (k<sub>1</sub>, k<sub>2</sub>, p<sub>1</sub>, p<sub>2</sub>, k<sub>3</sub>), which include radial (k<sub>n</sub>) and tangential (p<sub>n</sub>) distortion values,

        `rotationVectors` - Rotation Vector, the image pixel rotation angles in radians converted to vector by Rodrigues method,

        `translationVectors` - Translation Vector, the vector depicting shift in pixel values along x and y axis.

    :raises calibrationParamsPathNotProvided: Raises an error if the path was not provided or it isn't an instance of a string.
    """

    if (calibrationParamsPath == "") or (not isinstance(calibrationParamsPath, str)):
        raise calibrationParamsPathNotProvided(
            "Path to the calibration file was not provided or it is not a string!\nProvide appropriate path and re-run the program."
        )

    with open(calibrationParamsPath, "r") as f:
        jsonDump = jload(f)

    calibrationParams = {
        "mse": jsonDump["mse"],
        "rms": jsonDump["rms"],
        "cameraMatrix": npArray(jsonDump["cameraMatrix"]),
        "distortionCoefficients": npArray(jsonDump["distortionCoefficients"]),
        "rotationVectors": jsonDump["rotationVectors"],
        "translationVectors": jsonDump["translationVectors"],
    }

    return calibrationParams
