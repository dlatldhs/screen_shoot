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
    c = 2

    # capture img
    image = cv2.imread('dlatldhs_test_pic.png')

    mask = functions.mask_red_color(image)
    _, lines, line_angle_save = functions.get_lines(mask)
    

    for line in lines:
        if c > 0:
            c -= 1
            # print(type(line[0]))
            red_line_list.append(line[0])
            x1, y1, x2, y2 = line[0]
            print(x1,y1,x2,y2)
            red_slope = (y2-y1)/(x2-x1)
            red_slopes.append(red_slope)
            print(red_slope)
            red_intercept_y = y1 - ( red_slope * x1 )
            red_intercepts_y.append(red_intercept_y)
            print(f"red intercepts {red_intercept_y}")

    _ = functions.draw_dots(image,red_line_list)

    green_intercept_y = functions.draw_line_through_center(image, line_angle_save)
    

    cv2.imshow('image',image)
    print("초록 y절편 : ", green_intercept_y)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()