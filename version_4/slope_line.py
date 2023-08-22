import cv2
import numpy as np

def draw_line_through_center(img, slope):
    h, w = img.shape[:2]
    cx, cy = w // 2, h // 2

    # y절편 계산
    b = cy - slope * cx

    # 두 점의 좌표를 계산
    x_start = 0
    y_start = int(slope * x_start + b)
    x_end = w
    y_end = int(slope * x_end + b)

    # 선분을 초록색으로 그리기
    cv2.line(img, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2)

# 이미지 읽기
img_path = "center_shot.png"
img = cv2.imread(img_path)

img = cv2.imread(img_path)

h, w, _ = img.shape
w = w // 2
h = h // 2
image = cv2.resize(img, (w, h))

angle = -25 # 각도 대입
slope = np.tan(angle * np.pi / 180.0)
draw_line_through_center(image, slope)

# 이미지에 기울기가 x인 선분을 그리기
draw_line_through_center(image, slope)

# 결과 이미지 출력
cv2.imshow("Result", image)
cv2.waitKey(0)
cv2.destroyAllWindows()