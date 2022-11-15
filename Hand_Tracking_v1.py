import time
import cv2
import mediapipe as mp


mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
detect_hand_timer_init = 0
mouse_toggle_flag = False
key_toggle_flag = False
key_toggle2_flag = False
key_toggle3_flag = False
key_toggle4_flag = False
degree = 90
print(autopy.screen.scale())
# For video input:
cap = cv2.VideoCapture(1)
tipIds = [4, 8, 12, 16, 20]
with mp_hands.Hands(
        min_detection_confidence=0.8,
        min_tracking_confidence=0.8) as hands:
    while True:
        success, image = cap.read()
        image = cv2.flip(image, 1)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        image.flags.writeable = False
        results = hands.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        my_list = []
        if results.multi_hand_landmarks:
            myHand = results.multi_hand_landmarks[0]
            for idx, lm in enumerate(myHand.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                cz = float(lm.z * c)
                my_list.append([idx, cx, cy, cz])

        if len(my_list) != 0 and detect_hand_timer_init == 0:
           detect_hand_timer_init = time.time()
            
        elif len(my_list) != 0 and (time.time() - detect_hand_timer_init) > 1:
            x1, y1, z1 = my_list[9][1], my_list[9][2], my_list[9][3]
            cv2.circle(image, (x1, y1), 13, (255, 0, 255), cv2.FILLED)
            image_shape = image.shape[:2]
            data_z = 'z' + str(my_list[9][2]*10/28)
            data_f = 'f' + str(((my_list[5][1]-my_list[17][1])**2+(my_list[5][2]-my_list[17][2])**2)**0.5+40)
            cv2.line(image,(160,0),(160,640),(255,0,0),3,cv2.LINE_AA)
            cv2.line(image,(480,0),(480,640),(255,0,0),3,cv2.LINE_AA)

            if my_list[9][1] <= 160:
                if degree <= 0:
                    degree = 0
                else:
                    degree -= 1
                    data = 'b' + str(degree)
                print('right', data)

            if my_list[9][1] >= 480:
                if degree >= 180:
                    degree = 180
                else:
                    degree += 1
                    data = 'b' + str(degree)
                print('left', data)

            if my_list[6][2] - my_list[8][2] < 0 and \
                    my_list[10][2] - my_list[12][2] < 0 and my_list[14][2] - my_list[16][2] < 0 and \
                    my_list[18][2] - my_list[20][2] < 0 and not key_toggle4_flag:
                key_toggle4_flag = True
                print('close')
            elif my_list[6][2] - my_list[8][2] > 0 and \
                    my_list[10][2] - my_list[12][2] > 0 and my_list[14][2] - my_list[16][2] > 0 and \
                    my_list[18][2] - my_list[20][2] > 0 and key_toggle4_flag:
                key_toggle4_flag = False
                print('open')
                
            if len(my_list) != 0:
                fingers = []
                
        elif len(my_list) == 0:
            detect_hand_timer_init = 0
            
        cv2.imshow('MediaPipe Hands', image)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
