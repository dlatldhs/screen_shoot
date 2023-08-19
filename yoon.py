import cv2
import numpy as np

point_list = []

def draw_circle(image, image_with_box, center_x2, center_y2):
    COLOR = (0, 255, 0)
    RADIUS = 15 #반지름

    cv2.circle(image_with_box, (center_x2 + 3, center_y2), RADIUS, COLOR, cv2.FILLED, cv2.LINE_AA) #눈으로 봤을 때 너무 중앙에 안맞아서 일딴 +3 했음 (지워도 됨)

def Capture_Event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, y)
        point_list.append((x, y))  # 중점 좌표를 추가

def draw_bounding_box(image, points):
    x, y, w, h = cv2.boundingRect(points)
    if w > 15 and h > 15 and w < 100 and h < 100:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        center_x = x + w // 2
        center_y = y + h // 2
        point_list.append((center_x, center_y))
    
    return image

def find_gray_corners(image):
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

def main():
    
    image_path = 'screen_shoot_background_4.jpg'

    image = cv2.imread(image_path)

    h, w, _ = image.shape

    center_x2 = w // 2
    center_y2 = h // 2

    image_with_box = image.copy()
    
    draw_circle(image, image_with_box, center_x2, center_y2)


    gray_corners = find_gray_corners(image)

    for corners in gray_corners:
        image_with_box = draw_bounding_box(image_with_box, corners)
        

    top_left = point_list[3]
    bottom_left = point_list[1]
    top_right = point_list[2]
    bottom_right = point_list[0]

    cropped_image = image[top_left[1]:bottom_left[1], top_left[0]:top_right[0]]

    # cv2.imshow("cut image", cropped_image)
    saveCutImg = cv2.imwrite('cutImg.jpg', cropped_image)

    cv2.imshow("result", image_with_box)

    if saveCutImg:
        print("이미지 변수에 저장 성공")

        print(center_x2, center_y2)
    else:
        print("이미지 변수에 저장 실패")
        
    cv2.setMouseCallback('result', Capture_Event)
    cv2.waitKey(0)
    
if __name__ == "__main__":
    main()
