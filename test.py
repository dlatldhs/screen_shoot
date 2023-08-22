import cv2

cap = cv2.VideoCapture(1)

while True:
    # 프레임 읽어오기
    ret, frame = cap.read()
    
    # 프레임에서 사물 인식, 객체 추적 등의 코드 추가 가능
    
    # 프레임 출력하기
    cv2.imshow('frame', frame)
    
    # 'q'를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 종료
cap.release()
cv2.destroyAllWindows()
