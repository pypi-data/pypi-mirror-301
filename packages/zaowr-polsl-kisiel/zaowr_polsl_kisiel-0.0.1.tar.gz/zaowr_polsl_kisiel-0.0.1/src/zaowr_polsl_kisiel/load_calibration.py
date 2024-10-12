import json

import numpy as np


def load_calibration(calibrationParamsPath: str) -> dict[str, any]:
    """
    Load the camera calibration from specified JSON file

    :param str calibrationParamsPath: Path to the JSON calibration file
    :return dict[str, Any]: Returns calibration parameters of the camera:

        `mse` - Mean Square Error,

        `rms` - The overall RMS re-projection error in floating number format,

        `cameraMatrix` - Camera Matrix, the focal length and optical centre matrix as shown in intrinsic parameters,

        `distortionCoefficients` - Distortion Coefficients: (`k₁`, `k₂`, `p₁`, `p₂`, `k₃`), which include radial (`kₙ`) and tangential (`pₙ`) distortion values,

        `rotationVectors` - Rotation Vector, the image pixel rotation angles in radians converted to vector by Rodrigues method,

        `translationVectors` - Translation Vector, the vector depicting shift in pixel values along x and y axis.

    :raises calibrationParamsPathNotProvided: Raises an error if the path was not provided or it isn't an instance of a string.
    """

    if (calibrationParamsPath == "") or (not isinstance(calibrationParamsPath, str)):
        raise calibrationParamsPathNotProvided(
            "Path to the calibration file was not provided or it is not a string!\nProvide appropriate path and re-run the program."
        )

    with open(calibrationParamsPath, "r") as f:
        jsonDump = json.load(f)

    calibrationParams = {
        "mse": jsonDump["mse"],
        "rms": jsonDump["rms"],
        "cameraMatrix": np.array(jsonDump["cameraMatrix"]),
        "distortionCoefficients": np.array(jsonDump["distortionCoefficients"]),
        "rotationVectors": jsonDump["rotationVectors"],
        "translationVectors": jsonDump["translationVectors"],
    }

    return calibrationParams
