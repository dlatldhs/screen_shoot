import cv2
import numpy as np
import functions

def main():

    # img variable
    result_image_path = "only_crossline.png"

    # line angle save
    line_angle_save = []

    # cam read
    cap = cv2.VideoCapture(cv2.CAP_DSHOW+1)

    while True:
        
        # get frame
        ret, frame = cap.read()
        
        # target img
        result_img = cv2.imread(result_image_path)
        
        # target img resize
        rh, rw, _ = result_img.shape
        rw = rw//2;rh = rh//2
        result_img = cv2.resize(result_img,(rw,rh))

        # target center point
        rw = rw//2
        rh = rh//2

        # capture img
        image = frame
        h,w,_ = image.shape
        w = w//2;h = h//2
        cam_center = (w,h)

        # detecting red crossline
        crossline_img, angles = functions.detect_red_cross_lines(image)
        cv2.imshow('red crossline img',crossline_img)

        key = cv2.waitKey(1)

        if key == ord('q'):
            break

        if key == ord('c'):
            ret, frame = cap.read()
            capture_image = frame
            for angle in angles:
                if not any(int(angle) // 10 == int(existing_angle) // 10 for existing_angle in line_angle_save):
                    line_angle_save.append(angle)

            if len(line_angle_save) >= 2:
                draw_angle = line_angle_save[0]
                draw_angle2 = line_angle_save[1]

                print(draw_angle,draw_angle2)
                
                slope = np.tan(draw_angle * np.pi / 180.0)
                slope2 = np.tan(draw_angle2 * np.pi / 180.0)

                functions.draw_line_through_center(capture_image, slope)
                functions.draw_line_through_center(capture_image, slope2)
                    
                # Show the image after drawing lines
                cv2.imshow("capture_image", capture_image)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()