from . import load_calibration

if __name__ == "__main__":
    try:
        calibrationParams = load_calibration(
            "../../tests/calibration_params/calibration_params.json"
        )
        print(calibrationParams["mse"])

    # except calibrationParamsPathNotProvided:
    #     print("\nError loading calibration parameters!\n")
    #     raise

    # except imgToUndistortPathNotProvided:
    #     print("\nError removing distortion from the image!\n")
    #     raise

    # except undistortedImgPathNotProvided:
    #     print("\nError saving undistorted image!\n")
    #     raise

    except Exception as e:
        print(f"\nUnknown error occurred\nError: {e}\n")
