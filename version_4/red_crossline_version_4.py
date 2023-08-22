import cv2
import numpy as np
from screen_shot_lib import *

def get_center( img ):
    h, w, _ = img.shape
    print(h,w)
    w = w//2
    h = h//2
    return (w,h)

def main():
    
    # variable
    colors = (255, 0, 0)
    
    # target img
    # result_image_path = "center_shot.png"
    result_image_path = "only_crossline.png"

    # read cam
    cap = cv2.VideoCapture(2)
    
    while True:

        # frame
        ret, frame = cap.read()

        # target img
        # result_img = cv2.imread(result_image_path)
        # rh, rw, _ = result_img.shape
        # rw = rw//2
        # rh = rh//2
        # result_img = cv2.resize(result_img,(rw,rh))

        result_img = detect_green_cross_lines(frame)
        result_img = cv2.resize(result_img, (640, 480))

        result_center = get_center(result_img)

        cam = frame
        
        # cam screen
        cam_center = get_center(cam)

        x = cam_center[0]
        y = cam_center[1]
        cv2.circle(cam, (x, y),2,(0,255,0), -1)

        cv2.imshow("cam screen",cam)


        # detecting white points
        white_points = find_white_points(cam)


        # copy
        image_with_box = cam.copy()

        for corners in white_points:
            
            # image w box <- 객체에 박스 씌운 img
            # point_center 중점 좌표 ( 흰 객체 중앙 좌표 )
            image_with_box, point_center = draw_bounding_box(image_with_box, corners)
            
            # print(f"중점 좌표 {point_center}")
            # print(f"카메라의 중심 {cam_center}")
            points_distance = (cam_center[0] - point_center[0],cam_center[1] - point_center[1])

            # print("result center :", result_center)
            # print("points_distance :", points_distance)
            
            rcw = result_center[0] + ((points_distance[0]//2)//2)
            rch = result_center[1] + ((points_distance[1]//2)//2)
            
            # draw circle
            cv2.circle(result_img, (rcw,rch),5,(0,255,0),-1)

            
        cv2.imshow("result target img2", result_img)
        # quit
        key = cv2.waitKey(1) & 0xFF
        if key == 27 or key == ord('q'):
            break
    
    # wait
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()