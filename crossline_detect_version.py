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
        rw = rw//2;
        rh = rh//2
        result_img = cv2.resize(result_img,(rw,rh))

        # target center point
        rw = rw//2
        rh = rh//2
        
        only_cross_center = ( rw , rh ) 

        # capture img
        image = frame

        # detecting red crossline
        crossline_img, angles, (x1,x2), (y1,y2) = functions.detect_red_cross_lines(image)
        cv2.imshow('red crossline img',crossline_img)
        cv2.imshow('original img',image)


        key = cv2.waitKey(1)

        if key == ord('q'):
            break

        if key == ord('c'):

            # cam read
            ret, frame = cap.read()
            capture_image = frame
            
            # angles
            line_angle_save = []
            draw_angles = []
            slopes = []

            # 
            for angle in angles:
                if not any(int(angle) // 10 == int(existing_angle) // 10 for existing_angle in line_angle_save):
                    line_angle_save.append(angle)

            if len(line_angle_save) >= 2:
                '''
                각도 -> 기울기로 변환
                '''

                draw_angles.append(line_angle_save[0])
                draw_angles.append(line_angle_save[1])

                slopes.append(np.tan(draw_angles[0] * np.pi / 180.0))
                slopes.append(np.tan(draw_angles[1] * np.pi / 180.0))

                functions.draw_line_through_center(capture_image, slopes[0])
                functions.draw_line_through_center(capture_image, slopes[1])

                # print(f"draw angle{draw_angles[0],draw_angles[1]}")

                print(f"sloples[0]: {slopes[0]} slopes[1]: {slopes[1]}")

                h , w , _ = capture_image.shape

                dy = y2 - y1
                dx = x2 - x1
                slope = dy / dx
                print(f"slope2 : {slope}")
                
                b = y1 - slope * x1
                y_intercept = int(b) # y 절편

                functions.draw_dot(capture_image,0,y_intercept)
                # functions.draw_dot(capture_image,x2,y2)

                # capture_image = cv2.resize(capture_image,(w,h))

                # 각도 -> 기울기로 변환

                # TODO 객체의 교점 위치 2개 좌표 출력

                # TODO 카메라의 중점과 객체 교점의 위치 차 출력 해서 빼든가 해서 only_crossline 사진에서 중점과 카메라의 중점 비교

                # TODO 초록색 점 출력

                # TODO live 실시간 으로 ㄱㄱ

                # Show the image after drawing lines
                cv2.imshow("capture_image", capture_image)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()