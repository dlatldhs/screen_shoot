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
        crossline_img, angles = functions.detect_red_cross_lines(image)
        cv2.imshow('red crossline img',crossline_img)
        cv2.imshow('original img',image)


        key = cv2.waitKey(1)

        if key == ord('q'):
            break

        if key == ord('c'):
            ret, frame = cap.read()
            line_angle_save = []
            capture_image = frame
            for angle in angles:
                if not any(int(angle) // 10 == int(existing_angle) // 10 for existing_angle in line_angle_save):
                    line_angle_save.append(angle)

            if len(line_angle_save) >= 2:
                #여기서 앵글값을 슬로프로 값을 변환하여 위에 함수에 기울기를 지정해준것
                #어차피 여기서 앵글값을 넘겨줘도 위에 함수에서 그림을 그리기 위해선 슬로프로 값을 변화하고 그려야 하기때문에
                #여기서 미리 앵글값을 슬로프값으로 변환하여 저 함수로 넘겨준것
                draw_angle = line_angle_save[0]
                draw_angle2 = line_angle_save[1]

                print(f"draw angle{draw_angle,draw_angle2}")

                h , w , _ = capture_image.shape

                h = h//2
                w = w//2

                capture_image = cv2.resize(capture_image,(w,h))

                # 각도 -> 기울기로 변환
                slope = np.tan(draw_angle * np.pi / 180.0)
                slope2 = np.tan(draw_angle2 * np.pi / 180.0)

                functions.draw_line_through_center(capture_image, slope)
                functions.draw_line_through_center(capture_image, slope2)

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