import cv2
import numpy as np

def draw_dot(img,x,y):
    cv2.circle(img,(x,y),5,(255,0,255),-1)

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

    angles = []

    # 적절한 초록색의 HSV 경계 값 설정
    # lower_green = np.array([50, 100, 100])
    # upper_green = np.array([70, 255, 255])
    lower_green = np.array([30, 120, 120])  # 수정된 하한값
    upper_green = np.array([80, 255, 255])  # 수정된 상한값

    # 이진 이미지 생성
    mask = cv2.inRange(hsv, lower_green, upper_green)

    #선 검출 (HoughLinesP 변환 사용)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
    canny = cv2.Canny(thresh, 50, 100)

    # lines = cv2.HoughLinesP(canny, 1, np.pi/180, 100, minLineLength=100, maxLineGap=10)
    lines = cv2.HoughLinesP(canny, 1, np.pi/180, 100, minLineLength=50, maxLineGap=150)

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
                 # 점1(x1,y1) 과 점2(x2,y2) 사이에 각도를 계산하는 공식
                ''' 
                y축과 x축 사이의 각도를 라디안 단위로 계산
                -π ~ π 까지
                * 180 / np.pi 를 통해 라디안 각도를 실제 각도로 변환
                '''
                
                angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi

                # 수평선과 수직선 검출
                # if 80 < abs(angle) < 100 or -10 < abs(angle) < 10:
                cv2.line(output, (x1, y1), (x2, y2), (255, 0, 0), 2)
                float_angle = round(angle, 2) #소수점 2자리까지
                angles.append(float_angle)  # 각도 값 저장

    return output, angles

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

    result_slope = round(slope, 2) #소수점 둘째자리까지 뽑아내기 result_slope = 기울기
    #초록색 시작, 끝점 확인하는 코드
    print("초록색 x1 : ", x_start, "초록색 y1 : ", y_start)
    print("초록색 x2 : ", x_end, "초록색 y2 : ", y_end)
    print("현재 초록색 기울기 : ", result_slope)


def detect_red_cross_lines(image):
    '''
    빨간색 십자가의 형태를 감지하고 해당 선들의 각도를 계산하는 함수
    '''
    angles = []  # 새로 추가한 코드: 이 부분을 함수 시작 부분에 추가
    x1, y1, x2, y2 = 0, 0, 0, 0  # 변수 초기화

    # BGR -> HSV Color Transform
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # 빨간색 범위의 최소,최대값 저장
    lower_red = np.array([0, 120, 70])
    # upper_red = np.array([10, 255, 255])
    # upper_red = np.array([102, 228, 248])
    upper_red = np.array([10, 255, 255])

    # 빨간색 부분을 추출하여 이진화된 마스크 이미지 추출
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # grayscale 변경
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 임계값 처리 -> 이진화된 이미지 생성
    _, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)

    # canny 로 엣지 검출
    canny = cv2.Canny(thresh, 50, 100)

    # Hough 변환으로 선분 검출
    lines = cv2.HoughLinesP(canny, 1, np.pi/180, 100, minLineLength=50, maxLineGap=100)
    # lines = cv2.HoughLinesP(canny, 1, np.pi/180, 100, minLineLength=100, maxLineGap=10)

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
                cv2.line(output, (x1, y1), (x2, y2), (255, 0, 0), 2)

                float_angle = round(angle, 2) #소수점 2자리까지
                angles.append(float_angle)  # 각도 값 저장
                output = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
                cv2.line(output, (x1, y1), (x2, y2), (255, 0, 0), 2)
                
        # cv2.imshow("mask", mask)
        # cv2.imshow("result", output)
        cv2.waitKey(0)
    return output, angles, (x1,y1) , (x2,y2)

def draw_line_between_points(image, point1, point2, color):
    # 두 점 사이에 선 그리기
    fake_image = image.copy()
    cv2.line(fake_image, point1, point2, color, 2)

    return fake_image

def calculate_vector(p1, p2):
    vector_x = p2[0] - p1[0]
    vector_y = p2[1] - p1[1]
    return (vector_x, vector_y)

def mouse_handler(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:#마우스 왼쪽 버튼
        print("x좌표 : ", x)
        print("y좌표 : ", y)

def detect_red_lines(img):

    '''
    
    made by dlatldhs

    이 함수는 선을 찾는 함수
    맨 처음 이미지를 읽은 다음 복잡한 컬러 화소를 가지고 있는 이미지를
    단순한 형태인 회색조 형태로 변환함 그리고 좀 더 처리하기 쉬운 형태인 이진화로
    영상의 어두운 부분은 완전 어둡고 밝은 부분은 더 밝게 변함
    여기서 Thresholud() 의 인자로 임계값을 설정할 수 있음 카메라 성능에 따라 적절한 임계값 필요
    canny() 함수로 흰색과 검은색의 경계선을 추출함( 윤곽선 )
    윤곽선 중 직선으로 된 선을 추출합니다.
    반환되는 값으로는 리스트로 감지된 값의 시작점과 끝점을 반환합니다.
    예시) [ (x1,y1,x2,y2) , (x1,y1,x2,y2) ...] 이런식으로 인식한 선의 좌표를 반환함
    참고 자료 : https://blog.naver.com/suresofttech/221606239357

    '''
    # image read
    image = img.copy()

    # image 회색조 변환
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 회색조 -> 이진화
    # _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    # 블러로 부드럽게 ~ 
    gauss = cv2.GaussianBlur(gray, (5,5), 0)

    # 이진화 된 사진으로 윤곽선 검출
    edges = cv2.Canny(gauss, 50, 150)

    # 직선 검출하기

    # rho : 검출할 선분의 거리 해상도(픽셀 단위) 보통 1사용
    # theta : 세타 (각도)
    # threshold : 투표(vote)를 위한 최소 공간으로 임계값과 비슷함
    # 이 값보다 큰 값만 직선으로 검출됨, 일반적으로 검출할 선분에 개수에 따라 조정됨
    # 값이 작으면 많이 검출, 값이 크면 더 적은 선분 검출

    # minLinelength : 선분의 최소길이(픽셀 단위) 이 짧은 선분은 무시됨
    # maxLineGap : 끊어진 선분 사이의 최대 허용 간격(픽셀 단위)
    # maxLineGap 보다 작은 간격이 있는 선분은 결합되어 하나의 선으로 됨

    lines = cv2.HoughLinesP(edges, rho=1, theta=1*np.pi/180,
                             threshold=50,
                             minLineLength=10,
                             maxLineGap=250)
    if lines is not None:
        for line in lines:
            # first line
            x1, y1, x2, y2 = line[0]
            # 각도만 반환
            angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi    
    
    return angle


def mask_red_color(img):
    '''
    이 함수는 이미지에서 빨간색 부분만 마스킹합니다.
    img: 원본 이미지
    '''

    # BGR -> HSV 변환
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # HSV에서 빨간색 범위를 정의합니다.
    # 아래 값들은 일반적인 빨간색에 대한 근사치이며, 실제 상황에 따라 조정이 필요할 수 있습니다.
    
    lower_red1 = np.array([0, 70, 50])
    upper_red1 = np.array([10, 255, 255])
    
    lower_red2 = np.array([170, 70, 50])
    upper_red2 = np.array([180, 255, 255])
    
    # 빨간색 범위의 마스크 생성
    mask1 = cv2.inRange(hsv, lower_red1 , upper_red1)
    mask2 = cv2.inRange(hsv ,lower_red2 ,upper_red2)
    
    mask=mask1+mask2
    
    return mask

def draw_lines(img, lines):
    '''
    이 함수는 검출된 선을 이미지 위에 그리는 함수입니다.
    img: 원본 이미지
    lines: detect_red_lines() 함수에서 반환된 선의 좌표 리스트
    '''

    # lines가 None이 아닐 때만 실행
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            print(f"시작 좌표 x:{x1}, y:{y1} | 끝 좌표 x :{x2}, y:{y2}")
            cv2.line(img, (x1,y1), (x2,y2), (80,0,80), 3)
            
    return img