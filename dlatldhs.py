import cv2
import numpy as np
import functions
import math

def main():

    # img variable
    result_image_path = "only_crossline.png"
    target_background_image = cv2.imread(result_image_path)
    h, w, _ = target_background_image.shape
    target_h = h//2
    target_w = w//2
    target_background_image = cv2.resize(target_background_image,(target_w,target_h))
    h, w, _ = target_background_image.shape
    target_h = h//2
    target_w = w//2

    # line angle save
    line_angle_save = []
    red_line_list = []
    red_slopes = []
    red_intercepts_y = []
    mx = []
    my = []
    
    c = 2

    # capture img
    image = cv2.imread('dlatldhs_test_pic.png')
    frame_h, frame_w = image.shape[:2]
    frame_h = frame_h//2
    frame_w = frame_w//2

    mask = functions.mask_red_color(image)
    _, lines, line_angle_save = functions.get_lines(mask)
    
    # red line x y & intercept_y slope
    # red_slope : 기울기 , red_intercept_y : y 절편
    for line in lines:
        if c > 0:
            c -= 1
            red_line_list.append(line[0])
            x1, y1, x2, y2 = line[0]
            red_slope = (y2-y1)/(x2-x1)
            red_slopes.append(red_slope)
            red_intercept_y = y1 - ( red_slope * x1 )
            red_intercepts_y.append(red_intercept_y)
            # print(f"red intercepts {red_intercept_y}")

    # 점 찍어 보기
    _ = functions.draw_dots(image,red_line_list)

    # 초록색 y 절편 & 기울기 
    green_intercepts_y, green_slopes, cx, cy, angles = functions.draw_line_through_center(image, line_angle_save)
    
    # x : (y절편2 - y절편1)/(기울기1-기울기2)
    mx.append((green_intercepts_y[0] - red_intercepts_y[1])/(red_slopes[1] - green_slopes[0] ) )
    mx.append((green_intercepts_y[1] - red_intercepts_y[0])/(red_slopes[0] - green_slopes[1] ) )

    # y : (기울기1*x)+y절편1
    my.append((red_slopes[1] * mx[0] + red_intercepts_y[1]))
    my.append((red_slopes[1] * mx[1] + red_intercepts_y[1]))
    
    print("교점 1 : ", int(mx[0]), int(my[0]))
    print("교점 2 : ", int(mx[1]), int(my[1]))

    #왼쪽 선의 교점
    cv2.circle(image, (int(abs(mx[0])), int(abs(my[0]))), 5, (255, 0, 0), -1)
    
    #오른쪽 선의 교점
    cv2.circle(image, (int(abs(mx[1])), int(abs(my[1]))), 5, (255, 0, 0), -1)
    
    functions.draw_dot(image,frame_w,frame_h)

    # 교점 x 중점 y
    pita_1_x = int(mx[0])
    pita_1_y = frame_h
    pita_2_x = int(mx[1])
    pita_2_y = frame_h

    functions.draw_dot(image,pita_1_x,pita_1_y)
    functions.draw_dot(image,pita_2_x,pita_2_y)
    
    cv2.line(image,(abs(pita_1_x),abs(pita_1_y)),(frame_w,frame_h),(80,0,80), 3)
    cv2.line(image,(int(abs(mx[0])),int(abs(my[0]))),(pita_1_x,pita_1_y),(80,0,80), 3)
    cv2.line(image,(int(abs(mx[0])),int(abs(my[0]))),(frame_w,frame_h),(80,0,80), 3)

    cv2.line(image,(abs(pita_2_x),abs(pita_2_y)),(frame_w,frame_h),(80,0,80), 3)
    cv2.line(image,(int(abs(mx[1])),int(abs(my[1]))),(pita_2_x,pita_2_y),(80,0,80), 3)
    cv2.line(image,(int(abs(mx[1])),int(abs(my[1])) ),(frame_w,frame_h),(80,0,80), 3)

    rotate_image = image.copy()

    hsv = cv2.cvtColor(rotate_image, cv2.COLOR_BGR2HSV)

    # 파란색 범위 정의 (HSV)
    lower_blue = np.array([110,50,50])
    upper_blue = np.array([130,255,255])

    # HSV 이미지에서 파란색만 추출하기 위한 임계값 설정
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # mask와 원본 이미지를 비트 연산함으로써 파란색 부분만 남김
    result = cv2.bitwise_and(rotate_image,rotate_image, mask= mask)

    # 파랑색 점들이 있는 위치 찾기 (y,x 형태로 반환)
    blue_points_yx = np.where(mask != 0)
    blue_points_xy = list(zip(blue_points_yx[1], blue_points_yx[0])) # x,y 형태로 변환

    cross_first_point_xy = blue_points_xy[0]  # 첫번째 좌표 저장
    cross_last_point_xy  = blue_points_xy[-1] # 마지막 좌표 저장

    print("First point: ", cross_first_point_xy)
    print("Last  point: ", cross_last_point_xy)
    
    functions.draw_dot(result,cx,cy)
    
    (last_y, last_x) = cy-cross_first_point_xy[1] , cross_last_point_xy[0]-cx


    print(last_x,last_y)
    print(target_w,target_h)
    target_w = target_w + last_y
    target_h += last_x
    print(target_w,target_h)
    functions.draw_dot(target_background_image,target_w,target_h)

    cv2.imshow('target',target_background_image)
    cv2.imshow('result',result)
    cv2.imshow('rotate',rotate_image)
    cv2.imshow('image',image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()