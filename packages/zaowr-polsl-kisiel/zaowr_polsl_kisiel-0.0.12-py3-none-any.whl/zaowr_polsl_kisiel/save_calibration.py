from json import dump as jdump
from .exceptions import CalibrationParamsPathNotProvided


def save_calibration(
    calibrationParams: dict[str, list], calibrationParamsPath: str
) -> None:
    """
    Save the provided calibration parameters to specified JSON file

    :raises CalibrationParamsPathNotProvided: Raises an error if the path was not provided or it isn't an instance of a string.
    """

    if (calibrationParamsPath == "") or (not isinstance(calibrationParamsPath, str)):
        raise CalibrationParamsPathNotProvided

    with open(calibrationParamsPath, "w", encoding="utf-8") as f:
        jdump(calibrationParams, f, ensure_ascii=False, indent=4)
