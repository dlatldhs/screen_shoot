import cv2
import numpy as np

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
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # 적절한 빨간색의 HSV 경계 값 설정
    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255, 255])

    # 이진 이미지 생성
    mask = cv2.inRange(hsv, lower_red, upper_red)

    #선 검출 (HoughLinesP 변환 사용)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
    canny = cv2.Canny(thresh, 50, 100)

    lines = cv2.HoughLinesP(canny, 1, np.pi/180, 100, minLineLength=100, maxLineGap=10)

    output = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    angle = 0
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi

            # 수평선과 수직선 검출
            
            # cv2.line(output, (x1, y1), (x2, y2), (0, 255, 255), 2)

                 # 선의 기울기 계산
            
            dx = x2 - x1
            dy = y2 - y1
            slope = dy / dx
            # print(dy, dx)
            angle = np.arctan(slope) * 180 / np.pi
            
            
            
              

    return output, angle

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
    
    cap = cv2.VideoCapture(2)

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
        crossline_img, angle = detect_red_cross_lines(image)
        cv2.imshow('red crossline img',crossline_img)


        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        if key == ord('c'):
            cv2.imwrite("yunjong.jpg", crossline_img)

        print("angle : ", angle)
        
            

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()