import cv2
import numpy as np
import math

def Capture_Event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, y)
    

def draw_bounding_box(image, points):
    x, y, w, h = cv2.boundingRect(points)

    # center locate
    # center_x = x+ w//2
    # center_y = y+ h//2

    if w > 15 and h > 15 :
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        center_x = x + w // 2
        center_y = y + h // 2
        print("Width:", w, "Height:", h)
        print("Center X:", center_x, "Center Y:", center_y)
    else:
        print("예외처리 Width:", w, "Height:", h)
        
    return image, ( center_x , center_y )

# def find_gray_corners(image):
    lower_gray = np.array([100, 100, 100], dtype=np.uint8)
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

def find_green_object(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    lower_green = np.array([30, 100, 100], dtype=np.uint8)
    upper_green = np.array([80, 255, 255], dtype=np.uint8)

    mask = cv2.inRange(hsv, lower_green, upper_green)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

# calculate_vector_from_centers
# def calculate_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance
def calculate_vector(p1, p2):
    vector_x = p2[0] - p1[0]
    vector_y = p2[1] - p1[1]
    return (vector_x, vector_y)

# create line
def draw_line_between_points(image, point1, point2, color):
    # 두 점 사이에 선 그리기
    cv2.line(image, point1, point2, color, 2)
    return image

def main():

    image_path = 'test_image_1.jpg'
    
    image = cv2.imread(image_path)

    colors = (255, 0, 0)

    # find_center_difference
    height, width, _ = image.shape

    pic_center_x = int(width / 2)
    pic_center_y = int(height/ 2)

    pic_center = (pic_center_x,pic_center_y)
    # gray_corners = find_gray_corners(image)
    green_objects = find_green_object(image)

    image_with_box = image.copy()

    # for corners in gray_corners:
    for corners in green_objects:
        image_with_box, center = draw_bounding_box(image_with_box, corners)
        print("객체 중앙 좌표")
        print(center)
        print("사진 중앙 좌표")
        print(pic_center)

        image_with_line = draw_line_between_points(image_with_box,center,pic_center,colors)

        displacement_vector = calculate_vector(center, pic_center)
        print("중앙으로 부터 (카메라)조준점의 거리차")
        print(displacement_vector)

    # cv2.imshow("result", image_with_box)

    cv2.imshow("result", image_with_line)
    cv2.waitKey(0)

if __name__ == "__main__":
    main()