import cv2
import numpy as np

def draw_bounding_box(image, points):
    x, y, w, h = cv2.boundingRect(points)
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return image

def find_gray_corners(image):
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
    
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi

            # 수평선과 수직선 검출
            if 80 < abs(angle) < 100 or -10 < abs(angle) < 10:
                cv2.line(output, (x1, y1), (x2, y2), (0, 255, 255), 2)

    return output

def main():
    image_path = 'center_shot.png'  # 이미지 파일 경로 설정

    # 이미지 불러오기
    image = cv2.imread(image_path)
    h,w,_ = image.shape
    w = w//2
    h = h//2
    image = cv2.resize(image,(w,h))

    crossline_img = detect_red_cross_lines(image)
    cv2.imshow('red crossline',crossline_img)

    # 스티커 꼭짓점 검출
    gray_corners = find_gray_corners(image)

    # 사각형 그리기
    image_with_box = image.copy()
    for corners in gray_corners:
        image_with_box = draw_bounding_box(image_with_box, corners)
        for corner in corners:
            x, y = corner[0]
            print(f"Corner Coordinates: ({x}, {y})")

    cv2.imshow("img", image)
    cv2.imshow("result", image_with_box)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()