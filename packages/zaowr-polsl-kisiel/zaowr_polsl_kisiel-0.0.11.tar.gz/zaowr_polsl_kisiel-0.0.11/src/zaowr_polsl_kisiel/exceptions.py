class CalibrationImagesNotFound(Exception):
    """
    Couldn't find any calibration images in given path!\nProvide appropriate path and re-run the program.
    """

    def __init__(
        self,
        message="Couldn't find any calibration images in given path!\nProvide appropriate path and re-run the program.",
    ):
        self.message = message
        super().__init__(self.message)


class CalibrationParamsPathNotProvided(Exception):
    """
    Path to the calibration file was not provided or it is not a string!\nProvide appropriate path and re-run the program.
    """

    def __init__(
        self,
        message="Path to the calibration file was not provided or it is not a string!\nProvide appropriate path and re-run the program.",
    ):
        self.message = message
        super().__init__(self.message)


class ImgToUndistortPathNotProvided(Exception):
    """
    Path to the undistorted image was not provided or it is not a string!\nProvide appropriate path and re-run the program.
    """

    def __init__(
        self,
        message="Path to the undistorted image was not provided or it is not a string!\nProvide appropriate path and re-run the program.",
    ):
        self.message = message
        super().__init__(self.message)


class UndistortedImgPathNotProvided(Exception):
    """
    Path to save the undistorted image was not provided or it is not a string!\nProvide appropriate path and re-run the program.
    """

    def __init__(
        self,
        message="Path to save the undistorted image was not provided or it is not a string!\nProvide appropriate path and re-run the program.",
    ):
        self.message = message
        super().__init__(self.message)
