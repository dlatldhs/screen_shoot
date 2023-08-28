import cv2
import numpy as np

#첫번째 직선의 시작점과 끝점 : x1, y1, x2, y2
#두번째 직선의 시작점과 끝점 : x3, y3, x4, y4
def find_intersection(x1, y1, x2, y2, x3, y3, x4, y4):
    # 기울기 계산
    slope1 = (y2 - y1) / (x2 - x1)
    slope2 = (y4 - y3) / (x4 - x3)

    # y 절편 계산
    intercept1 = y1 - (slope1 * x1)
    intercept2 = y3 - (slope2 * x3)

    # 교점의 x 좌표 계산
    intersection_x = int((intercept2 - intercept1) / (slope1 - slope2))

    # 교점의 y 좌표 계산
    intersection_y = int(slope1 * intersection_x + intercept1)

    return intersection_x, intersection_y

# 이미지 생성
img = np.zeros((512, 512, 3), np.uint8)

# 두 개의 직선 생성
line_01_start = (100, 100)
line_01_end = (300 ,300)
line_02_start = (100 ,200)
line_02_end= (400 ,200)

# 라인 그리기
cv2.line(img,line_01_start,line_01_end,(0 ,0 ,255),thickness= 3)
cv2.line(img,line_02_start,line_02_end,(0 ,255 ,0),thickness= 2)

# 두 직선의 교접접 찾기 
intersection_x ,intersection_y= find_intersection(line_01_start[0], line_01_start[1],
                                                 line_01_end[0], line_01_end[1],
                                                 line_02_start[0], line_02_start[1],
                                                 line_02_end[0], line_02_start[1])

# 교접접에 동그라미 그리기 
cv2.circle(img,(intersection_x ,intersection_y ),10 ,(255 ,0 ,0),-11 )

# 이미지 보여주기 
cv2.imshow('image', img )
cv2.waitKey( )
cv2.destroyAllWindows()
