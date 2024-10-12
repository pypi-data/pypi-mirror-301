import cv2 as cv


def remove_distortion(
    cameraMatrix: Any,
    distortionCoefficients: Any,
    imgToUndistortPath: str,
    showImgToUndistort: bool = False,
    showUndistortedImg: bool = False,
    saveUndistortedImg: bool = False,
    undistortedImgPath: str = "",
    undistortionMethod: str = "undistort",
) -> None:
    """
    Remove distortion from given image

    :param Any cameraMatrix: Camera Matrix, the focal length and optical centre matrix as shown in intrinsic parameters.
    :param Any distortionCoefficients: Distortion Coefficients: (`k₁`, `k₂`, `p₁`, `p₂`, `k₃`), which include radial (`kₙ`) and tangential (`pₙ`) distortion values.
    :param str imgToUndistortPath: Path of the image which we want to undistort.
    :param bool showImgToUndistort: Decide if you want to show the original image., defaults to False
    :param bool showUndistortedImg: Decide if you want to show the undistorted image., defaults to False
    :param bool saveUndistortedImg: Decide if you want to save the undistorted image., defaults to False
    :param str undistortedImgPath: Path where we want to save the undistorted image., defaults to ""
    :param str undistortionMethod: Choose the method used for removing distortion (`undistort` or `remapping`)., defaults to "undistort"
    :raises imgToUndistortPathNotProvided: Raises an error if the path of the image which you want to undistort was not provided or it isn't an instance of a string.
    :raises undistortedImgPathNotProvided: Raises an error if the path where the undistorted image should be saved was not provided or it isn't an instance of a string.
    """

    if (imgToUndistortPath == "") or (not isinstance(imgToUndistortPath, str)):
        raise imgToUndistortPathNotProvided(
            "Path to the undistorted image was not provided or it is not a string!\nProvide appropriate path and re-run the program."
        )

    if saveUndistortedImg and (
        (undistortedImgPath == "") or (not isinstance(undistortedImgPath, str))
    ):
        raise undistortedImgPathNotProvided(
            "Path to save the undistorted image was not provided or it is not a string!\nProvide appropriate path and re-run the program."
        )

    # "../../../../ZAOWiR Image set - Calibration/Chessboard/Mono 1/cam4/58.png"
    img = cv.imread(imgToUndistortPath)

    if showImgToUndistort:
        cv.imshow("Current Image", img)
        print("\nPress any key to continue...")
        cv.waitKey()

    h, w = img.shape[:2]
    newOptimalCameraMatrix, roi = cv.getOptimalNewCameraMatrix(
        cameraMatrix, distortionCoefficients, (w, h), 0.3, (w, h)
    )

    if undistortionMethod == "undistort":
        dst = cv.undistort(
            img, cameraMatrix, distortionCoefficients, None, newOptimalCameraMatrix
        )

        # crop the image
        x, y, w, h = roi
        dst = dst[y : y + h, x : x + w]

        if showUndistortedImg:
            cv.imshow(dst)
            print("\nPress any key to continue...")
            cv.waitKey()

        if saveUndistortedImg:
            cv.imwrite(undistortedImgPath, dst)

    elif undistortionMethod == "remapping":
        mapx, mapy = cv.initUndistortRectifyMap(
            cameraMatrix,
            distortionCoefficients,
            None,
            newOptimalCameraMatrix,
            (w, h),
            5,
        )
        dst = cv.remap(img, mapx, mapy, cv.INTER_LINEAR)

        # crop the image
        x, y, w, h = roi
        dst = dst[y : y + h, x : x + w]

        if showUndistortedImg:
            cv.imshow(dst)
            print("\nPress any key to continue...")
            cv.waitKey()

        if saveUndistortedImg:
            cv.imwrite(undistortedImgPath, dst)
