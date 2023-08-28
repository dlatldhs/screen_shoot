import cv2
import numpy as np
import functions

def main():

    # img variable
    result_image_path = "only_crossline.png"

    # line angle save
    line_angle_save = []
    red_line_list = []
    c = 2

    # capture img
    image = cv2.imread('dlatldhs_test_pic.png')

    mask = functions.mask_red_color(image)
    ed_img, lines, line_angle_save = functions.get_lines(mask)
    copy = image.copy()

    green_intercept_y = functions.draw_line_through_center(image, line_angle_save)
    
    for line in lines:
        if c > 0:
            c -= 1
            # print(type(line[0]))
            red_line_list.append(line[0])

    _ = functions.draw_dots(image,red_line_list)

    cv2.imshow('image',image)
    # print("초록 y절편 : ", green_intercept_y)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()