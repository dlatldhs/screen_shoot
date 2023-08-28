import cv2
import numpy as np
import functions

def main():

    # img variable
    result_image_path = "only_crossline.png"

    # line angle save
    line_angle_save = []

    # capture img
    image = cv2.imread('dlatldhs_test_pic.png')

    mask = functions.mask_red_color(image)
    lines = functions.detect_red_lines(mask)

    img = image.copy()
    result = functions.draw_lines(img,lines)


    cv2.imshow('image',image)
    cv2.imshow('mask ',mask)
    
    cv2.imshow('result',result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()