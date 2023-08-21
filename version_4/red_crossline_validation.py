import cv2

# 이미지 파일 경로
img_path = "center_shot.png"

# 이미지 읽기
img = cv2.imread(img_path)

h , w , _ = img.shape
w= w//2
h= h//2

img = cv2.resize(img,(w,h))
cw = w//2
ch = h//2

cw = cw + 79
ch = ch + 40
# 점 그리기
cv2.circle(img, (cw, ch), 5, (0, 255, 0), -1)

# 이미지 출력
cv2.imshow("Image with green dot", img)

# 키 입력 대기
cv2.waitKey(0)

# 윈도우 닫기
cv2.destroyAllWindows()
