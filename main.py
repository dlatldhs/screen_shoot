import cv2
import numpy as np
from calibrate_camera import *
from project_points import *
from estimate_camera_pose import *

# camera correction w chess-board
images = [
    # 'chess_board/img.png',
    'chess_board/1.jpg','chess_board/2.jpg','chess_board/3.jpg','chess_board/4.jpg','chess_board/5.jpg','chess_board/6.jpg','chess_board/7.jpg','chess_board/8.jpg','chess_board/9.jpg','chess_board/10.jpg',
    # 'chess_board/11.jpg','chess_board/12.jpg','chess_board/13.jpg','chess_board/14.jpg','chess_board/15.jpg','chess_board/16.jpg','chess_board/17.jpg','chess_board/18.jpg', 
    ]

# chess-board size
# pattern_size = (10,7)
pattern_size = (9,6)

camera_matrix, dist_coeffs = calibrate_camera(images, pattern_size)

# print(camera_matrix,dist_coeffs)

# # 스크린의 3D 좌표와 해당 이미지 투영 사이의 대응점 찾기

# # 카메라로 찍은 사진에서 스크린의 외각 좌표를 넣어주면 됨
# image_points = [...]

# # 스크린의 3D 좌표 목록
# object_points = [
#     (0, 0, 0), # 왼쪽 하단 모서리
#     (1, 0, 0), # 오른쪽 하단 모서리
#     (1, 1, 0), # 오른쪽 상단 모서리
#     (0, 1, 0), # 왼쪽 상단 모서리
#     (0.5, 0.5, 0), # 중앙점
# ]


# # solvePnP 함수 호출하여 카메라의 회전 및 변환 벡터 얻기
# rvec, tvec = estimate_camera_pose(image_points, object_points, camera_matrix, dist_coeffs)

# # projectPoints 함수 호출하여 3D 공간에서 점을 이미지 평면에 투영하기

# points_3d = [...] # 3D 공간에서 점의 좌표 목록
# points_2d = project_points(points_3d, rvec, tvec, camera_matrix)