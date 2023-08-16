import cv2
import numpy as np

def calibrate_camera(images, pattern_size):
    objp = np.zeros((np.prod(pattern_size), 3), np.float32)
    objp[:, :2] = np.indices(pattern_size).T.reshape(-1, 2)
    objpoints = []
    imgpoints = []
    for image_path in images:
        print(image_path)
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, pattern_size, None)
        print(ret,corners)
        if ret:
            objpoints.append(objp)
            imgpoints.append(corners)
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    return mtx, dist







    # objp = np.zeros((np.prod(pattern_size), 3), np.float32)
    # objp[:, :2] = np.indices(pattern_size).T.reshape(-1, 2)
    # objpoints = []
    # imgpoints = []
    # for image_path in images:
    #     image = cv2.imread(image_path) # 이미지 로드
    #     # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #     ret, corners = cv2.findChessboardCorners(image, pattern_size, None)
    #     if ret:
    #         objpoints.append(objp)
    #         imgpoints.append(corners)
    # ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, image.shape[::-1], None, None)
    # return mtx, dist




# objp = np.zeros((np.prod(pattern_size), 3), np.float32)
    # objp[:, :2] = np.indices(pattern_size).T.reshape(-1, 2)
    # objpoints = []
    # imgpoints = []
    # for image_path in images:
    #     image = cv2.imread(image_path) # 이미지 로드
    #     # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #     ret, corners = cv2.findChessboardCorners(image, pattern_size, None)
    #     if ret:
    #         objpoints.append(objp)
    #         imgpoints.append(corners)
    # ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, image.shape[::-1], None, None)
    # return mtx, dist