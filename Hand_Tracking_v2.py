import time
import cv2
import mediapipe as mp
import serial
import math

Serial_BaudRate = 115200
Serial_Port = 'COM4'

print('Connecting to device ...')
# ser = serial.Serial(Serial_Port, Serial_BaudRate, timeout=3)fsfs
ser = serial.Serial()
ser.baudrate = Serial_BaudRate
ser.port = Serial_Port
ser.open()
print('Connect successful')

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
detect_hand_timer_init = 0

old_z_data = 0
old_f_data = 0

degree = 90
# For video input:
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
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

        if len(my_list) != 0 and (time.time() - detect_hand_timer_init) > 1:
            x1, y1, z1 = my_list[9][1], my_list[9][2], my_list[9][3]
            cv2.circle(image, (x1, y1), 13, (255, 0, 255), cv2.FILLED)
            cv2.line(image, (200, 0), (200, 640), (255, 0, 0), 3, cv2.LINE_AA)
            cv2.line(image, (440, 0), (440, 640), (255, 0, 0), 3, cv2.LINE_AA)

            f_data = int(
                math.sqrt((my_list[17][1] - my_list[5][1]) ** 2 + (my_list[17][2] - my_list[5][2]) ** 2)) * 4 + 10
            z_data = int((my_list[9][2] - 150) * 10 / 18 + 20)
            if old_f_data != f_data:
                if f_data > 160:
                    f_data = 160
                elif f_data < 40:
                    f_data = 40
                else:
                    old_f_data = f_data
                    print('f:', f_data)
                    ser.write(('f' + str(f_data)).encode('utf-8'))
                    time.sleep(0.001)

            if old_z_data != z_data:
                if z_data > 120:
                    z_data = 120
                elif z_data < 20:
                    z_data = 20
                else:
                    old_z_data = z_data
                    # print('z:', z_data)
                    ser.write(('z' + str(140 - z_data)).encode('utf-8'))
                    time.sleep(0.001)

            if my_list[9][1] <= 200:
                if degree <= 0:
                    degree = 0
                else:
                    degree -= 1
                    ser.write(('b' + str(degree)).encode('utf-8'))
                    time.sleep(0.001)
                print('right b:', degree)

            if my_list[9][1] >= 440:
                if degree >= 180:
                    degree = 180
                else:
                    degree += 1
                    ser.write(('b' + str(degree)).encode('utf-8'))
                    time.sleep(0.001)
                print('left b:', degree)

            if my_list[6][2] - my_list[8][2] < 0 and \
                    my_list[10][2] - my_list[12][2] < 0 and my_list[14][2] - my_list[16][2] < 0 and \
                    my_list[18][2] - my_list[20][2] < 0 and not key_toggle4_flag:
                key_toggle4_flag = True
                print('close')
                ser.write('c130'.encode('utf-8'))
                time.sleep(0.001)
            elif my_list[6][2] - my_list[8][2] > 0 and \
                    my_list[10][2] - my_list[12][2] > 0 and my_list[14][2] - my_list[16][2] > 0 and \
                    my_list[18][2] - my_list[20][2] > 0 and key_toggle4_flag:
                key_toggle4_flag = False
                print('open')
                ser.write('c40'.encode('utf-8'))
                time.sleep(0.001)

            if len(my_list) != 0:
                fingers = []

        elif len(my_list) == 0:
            detect_hand_timer_init = 0

        cv2.imshow('MediaPipe Hands', image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
