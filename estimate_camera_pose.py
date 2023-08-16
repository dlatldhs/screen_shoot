import cv2
import numpy as np

def estimate_camera_pose(image_points, object_points, camera_matrix, dist_coeffs):
    _, rvec, tvec = cv2.solvePnP(object_points, image_points, camera_matrix, dist_coeffs)
    return rvec, tvec