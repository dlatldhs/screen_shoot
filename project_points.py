import cv2
import numpy as np

def project_points(points_3d, rvec, tvec, camera_matrix):
    points_2d, _ = cv2.projectPoints(points_3d, rvec, tvec, camera_matrix)
    return points_2d