import cv2
import numpy as np

def draw_line_through_center(img, slope):
    h, w = img.shape[:2]
    cx, cy = w // 2, h // 2

    # y절편 계산
    b = cy - slope * cx

    # 두 점의 좌표를 계산
    x_start = 0
    y_start = int(slope * x_start + b)
    x_end = w
    y_end = int(slope * x_end + b)

    # 선분을 초록색으로 그리기
    cv2.line(img, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2)


def draw_bounding_box(image, points):
    x, y, w, h = cv2.boundingRect(points)
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    center_x = x + w // 2
    center_y = y + h // 2
    return image, (center_x, center_y )

def find_white_points(image):
    lower_gray = np.array([200, 200, 200], dtype=np.uint8)
    upper_gray = np.array([255, 255, 255], dtype=np.uint8)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

    mask = cv2.inRange(image, lower_gray, upper_gray)
    edges = cv2.Canny(mask, 30, 150)

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    corners = []
    for contour in contours:
        epsilon = 0.1 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        if len(approx) == 4:
            corners.append(approx)
    
    return corners

def detect_red_cross_lines(image):
    angles = []  # 새로 추가한 코드: 이 부분을 함수 시작 부분에 추가
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255, 255])

    mask = cv2.inRange(hsv, lower_red, upper_red)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
    canny = cv2.Canny(thresh, 50, 100)

    lines = cv2.HoughLinesP(canny, 1, np.pi/180, 100, minLineLength=100, maxLineGap=10)

    output = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]

            # 선의 중심에 위치한 픽셀이 빨간색 범위 내인지 확인
            mid_line_x = int((x1 + x2) / 2)
            mid_line_y = int((y1 + y2) / 2)
            pixel_value = mask[mid_line_y, mid_line_x]

            # 중심 픽셀이 빨간색 범위에 있으면, 각도와 선 그리기
            if pixel_value != 0:
                angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi

                # 수평선과 수직선 검출
                cv2.line(output, (x1, y1), (x2, y2), (0, 255, 255), 2)

                # 선의 기울기 계산
                dx = x2 - x1
                dy = y2 - y1
                slope = dy / dx
                angle = np.arctan(slope) * 180 / np.pi
                float_angle = round(angle, 2) #소수점 2자리까지
                angles.append(float_angle)  # 각도 값 저장

    return output, angles

def draw_line_between_points(image, point1, point2, color):
    # 두 점 사이에 선 그리기
    fake_image = image.copy()
    cv2.line(fake_image, point1, point2, color, 2)

    return fake_image

def calculate_vector(p1, p2):
    vector_x = p2[0] - p1[0]
    vector_y = p2[1] - p1[1]
    return (vector_x, vector_y)

def main():
    # read img
    # image_path = 'center_shot.png'
    image_path = 'test_4.png'
    result_image_path = "center_shot.png"
    capture_path = "yunjong.jpg"

    save_point = []
    
    cap = cv2.VideoCapture(0)

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
        crossline_img, angles = detect_red_cross_lines(image)
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

                draw_line_through_center(result_cap_img, slope)
                draw_line_through_center(result_cap_img, slope2)
                    
                # Show the image after drawing lines
                cv2.imshow("result_cap", result_cap_img)


            

    # draw_angle = save_point[0]
    # draw_angle2 = save_point[1]

    

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()