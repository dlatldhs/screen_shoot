import cv2
import numpy as np

def line_params(line):
    rho, theta = line[0]
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho
    x1 = int(x0 + 1000 * (-b))
    y1 = int(y0 + 1000 * a)
    x2 = int(x0 - 1000 * (-b))
    y2 = int(y0 - 1000 * a)

    slope = (y2 - y1) / (x2 - x1)
    y_intercept = y1 - slope * x1
    return slope, y_intercept

img = cv2.imread("ff.png")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 50, 150)
lines = cv2.HoughLines(edges, 1, np.pi/180, 100)

if lines is not None and len(lines) >= 2:
    line1, line2 = lines[:2]
    slope1, y_intercept1 = line_params(line1)
    slope2, y_intercept2 = line_params(line2)

    x_intersect = (y_intercept2 - y_intercept1) / (slope1 - slope2)
    y_intersect = slope1 * x_intersect + y_intercept1

    print("두 직선의 교점은 ({}, {}) 입니다.".format(x_intersect, y_intersect))

    cv2.circle(img, (int(x_intersect), int(y_intersect)), 5, (255, 0, 0), -1)
    cv2.imshow("Result", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("적어도 두 개의 직선이 필요합니다.")
