import cv2
import numpy as np
import functions

def main():

    # img variable
    result_image_path = "only_crossline.png"

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

    mask = functions.mask_red_color(image)
    _, lines, line_angle_save = functions.get_lines(mask)
    

    for line in lines:
        if c > 0:
            c -= 1
            red_line_list.append(line[0])
            x1, y1, x2, y2 = line[0]
            red_slope = (y2-y1)/(x2-x1)
            red_slopes.append(red_slope)
            red_intercept_y = y1 - ( red_slope * x1 )
            red_intercepts_y.append(red_intercept_y)
            print(f"red intercepts {red_intercept_y}")

    _ = functions.draw_dots(image,red_line_list)

    green_intercepts_y, green_slopes, cx, cy = functions.draw_line_through_center(image, line_angle_save)

    # x : (y절편2 - y절편1)/(기울기1-기울기2)
    mx.append((green_intercepts_y[0] - red_intercepts_y[1])/(red_slopes[1] - green_slopes[0] ) )
    mx.append((green_intercepts_y[1] - red_intercepts_y[0])/(red_slopes[0] - green_slopes[1] ) )

    my.append((red_slopes[1] * mx[0] + red_intercepts_y[1]))
    my.append((red_slopes[1] * mx[1] + red_intercepts_y[1]))

    #이 값들을 정수형으로 변환 및 절댓값으로 변환을 해준다.
    abs_mxy_0 = int(abs(mx[0])), int(abs(my[0]))
    abs_mxy_1 = int(abs(mx[1])), int(abs(my[1]))

    print("교점 1 :", abs_mxy_0)
    print("교점 2 :", abs_mxy_1)
    print("중점 : ", cx, cy)
    
    #중점과 교차점까지의 거리를 측정
    cal_1, cal_2 = cx - abs_mxy_0[0], cy - abs_mxy_0[1]
    cal_3, cal_4 = cx - abs_mxy_1[0], cy - abs_mxy_1[1]

    print("거리차1 : ", cal_1, cal_2)
    print("거리차2 : ", cal_3, cal_4)
    #왼쪽 선의 교점
    cv2.circle(image,(abs_mxy_0),5,(0, 255, 255),-1) 

    #오른쪽 선의 교점
    cv2.circle(image,(abs_mxy_1),5,(255, 0, 0),-1)
    
    cv2.imshow('image',image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()