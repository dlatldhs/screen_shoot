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

def detect_green_cross_lines(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # 적절한 초록색의 HSV 경계 값 설정
    lower_green = np.array([50, 100, 100])
    upper_green = np.array([70, 255, 255])

    # 이진 이미지 생성
    mask = cv2.inRange(hsv, lower_green, upper_green)

    #선 검출 (HoughLinesP 변환 사용)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
    canny = cv2.Canny(thresh, 50, 100)

    lines = cv2.HoughLinesP(canny, 1, np.pi/180, 100, minLineLength=100, maxLineGap=10)

    output = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi

            # 수평선과 수직선 검출
            if 80 < abs(angle) < 100 or -10 < abs(angle) < 10:
                cv2.line(output, (x1, y1), (x2, y2), (0, 255, 0), 2)

    return output

def draw_line_through_center(img, slope):
    h, w = img.shape[:2]
    cx = w // 2
    cy = h // 2

    # y절편 계산
    b = cy - slope * cx

    # 두 점의 좌표를 계산
    x_start = 0
    y_start = int(slope * x_start + b)
    x_end = w
    y_end = int(slope * x_end + b)

    # 선분을 초록색으로 그리기
    cv2.line(img, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2)

def detect_red_cross_lines(image):
    '''
    빨간색 십자가의 형태를 감지하고 해당 선들의 각도를 계산하는 함수
    '''
    angles = []  # 새로 추가한 코드: 이 부분을 함수 시작 부분에 추가
    
    # BGR -> HSV Color Transform
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # 빨간색 범위의 최소,최대값 저장
    lower_red = np.array([0, 120, 70])
    # upper_red = np.array([10, 255, 255])
    upper_red = np.array([102, 228, 248])

    # 빨간색 부분을 추출하여 이진화된 마스크 이미지 추출
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # grayscale 변경
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 임계값 처리 -> 이진화된 이미지 생성
    _, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)

    # canny 로 엣지 검출
    canny = cv2.Canny(thresh, 50, 100)

    # Hough 변환으로 선분 검출
    lines = cv2.HoughLinesP(canny, 1, np.pi/180, 100, minLineLength=100, maxLineGap=10)

    # mask img -> bgr img
    output = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    # 검출된 선분이 있다면 ?
    if lines is not None:
        for line in lines:
            # first line
            x1, y1, x2, y2 = line[0]

            # 선의 중심에 위치한 픽셀이 빨간색 범위 내인지 확인
            mid_line_x = int((x1 + x2) / 2)
            mid_line_y = int((y1 + y2) / 2)
            pixel_value = mask[mid_line_y, mid_line_x]

            # 중심 픽셀이 빨간색 범위에 있으면, 각도와 선 그리기
            if pixel_value != 0:
                # 점1(x1,y1) 과 점2(x2,y2) 사이에 각도를 계산하는 공식
                ''' 
                y축과 x축 사이의 각도를 라디안 단위로 계산
                -π ~ π 까지
                * 180 / np.pi 를 통해 라디안 각도를 실제 각도로 변환
                '''

                angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi

                # print(f"angle {angle}") 

                # 수평선과 수직선 검출
                cv2.line(output, (x1, y1), (x2, y2), (0, 255, 0), 2)


                # dx = x2 - x1
                # dy = y2 - y1
                # slope = dy / dx

                # print(f"slope {slope}")
                
                # angle = np.arctan(slope) * 180 / np.pi
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