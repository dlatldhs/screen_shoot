import cv2
import numpy as np

import functions

def main():
    # read img
    result_image_path = "only_crosslineq.png"
    capture_path = "image.jpg"

    save_point = []
    
    cap = cv2.VideoCapture(cv2.CAP_DSHOW+1)

    while True:

        ret, frame = cap.read()

        
        result_img = cv2.imread(result_image_path)
        rh, rw, _ = result_img.shape

        rw = rw//2
        rh = rh//2
        result_img = cv2.resize(result_img,(rw,rh))

        rw = rw//2
        rh = rh//2

        image = frame
        h,w,_ = image.shape
        w = w//2
        h = h//2
        colors = (255, 0, 0)
        cam_center = (w,h)

        # detecting red crossline
        crossline_img, angles = functions.detect_red_cross_lines(image)
        cv2.imshow('red crossline img',crossline_img)




        result_cap_img = cv2.imread(capture_path)
        


        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        if key == ord('c'):
            cv2.imwrite(capture_path, crossline_img)
            for angle in angles:
                if not any(int(angle) // 10 == int(existing_angle) // 10 for existing_angle in save_point):
                    save_point.append(angle)

            if len(save_point) >= 2:
                draw_angle = save_point[0]
                draw_angle2 = save_point[1]

                slope = np.tan(draw_angle * np.pi / 180.0)
                slope2 = np.tan(draw_angle2 * np.pi / 180.0)

                functions.draw_line_through_center(result_cap_img, slope)
                functions.draw_line_through_center(result_cap_img, slope2)
                    
                # Show the image after drawing lines
                cv2.imshow("result_cap", result_cap_img)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()