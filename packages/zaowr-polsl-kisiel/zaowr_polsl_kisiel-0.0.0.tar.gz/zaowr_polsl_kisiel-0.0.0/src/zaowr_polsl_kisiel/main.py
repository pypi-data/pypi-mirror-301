import numpy as np
import cv2 as cv
import glob
import json


def main() -> None:

    # termination criteriaimages
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    # objp = np.zeros((6 * 7, 3), np.float32)
    # objp[:, :2] = np.mgrid[0:7, 0:6].T.reshape(-1, 2)
    objp = np.zeros((10 * 7, 3), np.float32)
    objp[:, :2] = np.mgrid[0:10, 0:7].T.reshape(-1, 2) * 28.67

    # Arrays to store object points and image points from all the images.
    objpoints = []  # 3d point in real world space
    imgpoints = []  # 2d points in image plane.

    images = glob.glob(
        "../../../../ZAOWiR Image set - Calibration/Chessboard/Mono 1/cam4/*.png"
    )
    # images = images[0:10]

    for fname in images:
        img = cv.imread(fname)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret, corners = cv.findChessboardCorners(gray, (10, 7), None)

        # If found, add object points, image points (after refining them)
        if ret == True:
            objpoints.append(objp)

            corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners2)

            # Draw and display the corners
            # cv.drawChessboardCorners(img, (10, 7), corners2, ret)
            # cv.imshow("img", img)
            # cv.waitKey(500)

    cv.destroyAllWindows()

    ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(
        objpoints, imgpoints, gray.shape[::-1], None, None
    )

    mean_error = 0
    for i in range(len(objpoints)):
        imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
        4
        error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2) / len(imgpoints2)
        mean_error += error
        # print("Mean reprojection error: {}", mean_error / len(objpoints))

    calibration_params = {
        "corners1": corners,
        "corners2": corners2,
        "mean_error": mean_error,
        "ret": ret,
        "mtx": mtx.tolist(),
        "dist": dist.tolist(),
        "rvecs": [rvec.tolist() for rvec in rvecs],
        "tvecs": [tvec.tolist() for tvec in tvecs],
    }
    with open("./calibration_params.json", "w", encoding="utf-8") as f:
        json.dump(calibration_params, f, ensure_ascii=False, indent=4)

    # undistortion(mtx, dist, type="undistort")
    # undistortion(mtx, dist, type="remapping")


def undistortion(
    mtx,
    dist,
    savePath,
    type: str = "undistort",
    imgPath: str = "../../../../ZAOWiR Image set - Calibration/Chessboard/Mono 1/cam4/58.png",
):
    img = cv.imread(imgPath)
    cv.imshow("img", img)

    h, w = img.shape[:2]
    newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w, h), 0.3, (w, h))

    if type == "undistort":
        dst = cv.undistort(img, mtx, dist, None, newcameramtx)

        # crop the image
        x, y, w, h = roi
        dst = dst[y : y + h, x : x + w]
        # cv.imwrite("../img/undistort_calibresult.png", dst)
        cv.imwrite(savePath, dst)

    elif type == "remapping":
        mapx, mapy = cv.initUndistortRectifyMap(
            mtx, dist, None, newcameramtx, (w, h), 5
        )
        dst = cv.remap(img, mapx, mapy, cv.INTER_LINEAR)

        # crop the image
        x, y, w, h = roi
        dst = dst[y : y + h, x : x + w]
        # cv.imwrite("../img/remapping_calibresult.png", dst)

        cv.imwrite(savePath, dst)


def read_calibration():
    with open("./calibration_params.json", "r") as f:
        dump = json.load(f)

    # corners = dump["corners"]
    # corners2 = dump["corners2"]
    # mean_error = dump["mean_error"]
    # ret = dump["ret"]
    # mtx = dump["mtx"]
    # dist = dump["dist"]
    # rvecs = dump["rvecs"]
    # tvecs = dump["tvecs"]

    return dump

    # return (corners, corners2, mean_error, ret, mtx, dist, rvecs, tvecs)


if __name__ == "__main__":
    try:
        # main()
        dump = read_calibration()
        # corners = dump["corners1"]
        # corners2 = dump["corners2"]
        mean_error = dump["mean_error"]
        ret = dump["ret"]
        mtx = np.array(dump["mtx"])
        dist = np.array(dump["dist"])
        rvecs = dump["rvecs"]
        tvecs = dump["tvecs"]

        undistortion(
            mtx,
            dist,
            "../img/undistort_calibresult_2.png",
            type="undistort",
        )
        undistortion(
            mtx,
            dist,
            "../img/remapping_calibresult_2.png",
            type="remapping",
        )

    except Exception as e:
        print(e)
    finally:
        cv.destroyAllWindows()
        print("done")
