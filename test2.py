import cv2
import numpy as np
import functions

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
img_path = "yunjonghyeok.png"
image = cv2.imread(img_path)

# h, w, _ = img.shape
   # 정수 나눗셈 사용하여 반올림 처리
   # 정수 나눗셈 사용하여 반올림 처리
# image = cv2.resize(img, (w,h))

angle =61.98   # 각도 대입: 54.98°와 -26.19° 설정 예시입니다.
angle2 =-28.19   # 각도 대입: 54.98°와 -26.19° 설정 예시입니다.
slope = np.tan(angle * np.pi / 180.0)
slope2= np.tan(angle2 * np.pi /180.0)

# 이미지에 기울기가 x인 선분 그리기
draw_line_through_center(image,slope)
draw_line_through_center(image,slope2)

crossline_img, angles, (x1,y1) , (x2,y2) = functions.detect_red_cross_lines(image)
# cv2.circle(crossline_img, (x1,y1), 5, (0, 255, 0), -1)
# cv2.circle(crossline_img, (x2,y2), 5, (0, 255, 0), -1)
while True:
	cv2.imshow("Result", image)
	cv2.imshow("Result2", crossline_img)
	key = cv2.waitKey(1) 
	if key == ord('c'):   # 'c' 키를 누르면 사진 캡처 및 저장 수행합니다.
		cv2.imwrite('cap_img.png', image)
		

cv.destroyAllWindows()
