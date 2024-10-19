import cv2
import mediapipe as mp
import pyautogui
import math


webcam = cv2.VideoCapture(0)

#khởi tạo lớp bắt bàn tay
my_hands = mp.solutions.hands.Hands()

# khởi tạo alias cho drawing_utils chứa các hàm vẽ lên hình ảnh
drawing_utils = mp.solutions.drawing_utils

# tạo biến vẽ đường thẳng
x1 = y1 = x2 = y2 =0

while True:



    ret, image = webcam.read()
    frame_height, frame_width, _ = image.shape

    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # bắt các bàn tay
    output = my_hands.process(rgb_image)

    # lấy mảng các bàn tay và vẽ từng bàn tay với các đốt tay
    hands = output.multi_hand_landmarks
    if hands:
        # trong hands là một mảng gồm các bàn tay hiển thị trên màn hình
        for hand in hands:
            # vẽ bàn tay
            drawing_utils.draw_landmarks(image, hand,  mp.solutions.hands.HAND_CONNECTIONS)
            # drawing_utils.draw_landmarks(image, hand)
            #trong một bàn tay có các cột mốc gom thành một mảng [{x, y}, {x,y}] 
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)
                # lấy ngón trỏ
                if id == 8:
                    cv2.circle(image, (x, y), 10, (0, 255, 0), 2)
                    x1 = x
                    y1 = y
                # lấy ngón lớn
                elif id == 4:
                    cv2.circle(image, (x, y), 10, (0, 255, 0), 2)
                    x2 = x
                    y2 = y

            # tính khoảng cách giữa  2 ngón
            dist = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
            
            # vẽ đường thẳng giữa 2 ngón
            cv2.line(image, (x1, y1),(x2,y2), (255,0,0), 2)

            # xử lí tăng giảm
            if dist > 70:
                pyautogui.press("volumeup")
            else:
                pyautogui.press("volumedown")

    cv2.imshow("Hand Volume", image)

    if cv2.waitKey(1) == ord("q"):
        break





webcam.release()
cv2.destroyAllWindows()