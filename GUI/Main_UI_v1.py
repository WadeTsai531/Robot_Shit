import tkinter as tk
import time
import cv2
import mediapipe as mp
from PIL import Image, ImageTk
import serial
import math


class Main:
    old_f_data = 1
    old_z_data = 1
    degree = 90

    def __init__(self):
        # -------- variable --------
        self.tracking_flag = False
        self.key_toggle_flag = False

        # -------- Serial Setup --------
        Serial_BaudRate = 38400
        Serial_Port = 'COM9'
        print('Connecting to device ...')
        self.ser = serial.Serial()
        self.ser.baudrate = Serial_BaudRate
        self.ser.port = Serial_Port
        self.ser.open()
        print('Connect successful')

        # -------- UI Setup --------
        self.main_window = tk.Tk()
        self.main_window.geometry('1280x820')
        self.main_window.title('Main_GUI')
        self.main_window.configure(bg='#FFD8E9')
        self.main_window.resizable(width=False, height=False)

        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)

        self.cam = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        self.Vision()

        image_tk = ImageTk.PhotoImage(Image.open('image3.jpg'))
        self.image_label = tk.Label(self.main_window, image=image_tk, width=418, height=648)
        self.image_label.place(x=850, y=10)

        self.Start_Button = tk.Button(self.main_window, text='Start', font=('Times', 20, 'bold'), width=8,
                                      command=self.Start_mode)
        self.Start_Button.place(x=880, y=690)

        self.Close_Button = tk.Button(self.main_window, text='Close', font=('Times', 20, 'bold'), width=8,
                                      command=self.Close_mode)
        self.Close_Button.place(x=1120, y=690)

        self.main_window.mainloop()

    def Vision(self):
        ret, frame = self.cam.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_resize = cv2.resize(frame, None, fx=1.2, fy=1.2)
        frame_PIL = Image.fromarray(frame_resize)
        frame_tk = ImageTk.PhotoImage(frame_PIL)
        self.label = tk.Label(self.main_window, image=frame_tk)
        self.label.place(x=10, y=100)
        self.label.after(1, self.Re_Vision)

    def Re_Vision(self):
        ret, frame = self.cam.read()
        frame = cv2.flip(frame, 1)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_resize = cv2.resize(frame, None, fx=1.2, fy=1.2)
        if self.tracking_flag:
            frame_resize = self.Hand_Tracking(frame_resize)
        frame_PIL = Image.fromarray(frame_resize)
        frame_tk = ImageTk.PhotoImage(frame_PIL)
        self.label.image = frame_tk
        self.label.configure(image=frame_tk)
        self.label.after(1, self.Re_Vision)

    def Hand_Tracking(self, frame):
        results = self.hands.process(frame)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
        my_list = []
        if results.multi_hand_landmarks:
            myHand = results.multi_hand_landmarks[0]
            for idx, lm in enumerate(myHand.landmark):
                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                cz = float(lm.z * c)
                my_list.append([idx, cx, cy, cz])

        if len(my_list) != 0:
            x1, y1, z1 = my_list[9][1], my_list[9][2], my_list[9][3]
            cv2.circle(frame, (x1, y1), 13, (255, 0, 255), cv2.FILLED)
            cv2.line(frame, (260, 0), (260, 640), (255, 0, 0), 3, cv2.LINE_AA)
            cv2.line(frame, (500, 0), (500, 640), (255, 0, 0), 3, cv2.LINE_AA)

            f_data = int(math.sqrt((my_list[17][1] - my_list[5][1]) ** 2 +
                                   (my_list[17][2] - my_list[5][2]) ** 2) * 9 / 10) + 40
            z_data = int((my_list[9][2] - 150) * 10 / 18)
            print('F: {} Z: {} Degree: {}'.format(f_data, z_data, self.degree))

            if abs(f_data - self.old_f_data) / self.old_f_data > 0.04:
                if 40 < f_data < 160:
                    self.old_f_data = f_data
                    self.ser.write(('f' + str(f_data)).encode('utf-8'))
                    time.sleep(0.001)

            if abs(z_data - self.old_z_data) / self.old_z_data > 0.04:
                if 20 < z_data < 120:
                    self.old_z_data = z_data
                    self.ser.write(('z' + str(140 - z_data)).encode('utf-8'))
                    time.sleep(0.001)

            if my_list[9][1] >= 500:
                if self.degree <= 0:
                    self.degree = 0
                else:
                    self.degree -= 2
                    self.ser.write(('b' + str(self.degree)).encode('utf-8'))
                    time.sleep(0.001)

            if my_list[9][1] <= 260:
                if self.degree >= 180:
                    self.degree = 180
                else:
                    self.degree += 2
                    self.ser.write(('b' + str(self.degree)).encode('utf-8'))
                    time.sleep(0.001)

            if my_list[6][2] - my_list[8][2] < 0 and \
                    my_list[10][2] - my_list[12][2] < 0 and my_list[14][2] - my_list[16][2] < 0 and \
                    my_list[18][2] - my_list[20][2] < 0 and not self.key_toggle_flag:
                self.key_toggle_flag = True
                print('close')
                self.ser.write('c130'.encode('utf-8'))
                time.sleep(0.001)
            elif my_list[6][2] - my_list[8][2] > 0 and \
                    my_list[10][2] - my_list[12][2] > 0 and my_list[14][2] - my_list[16][2] > 0 and \
                    my_list[18][2] - my_list[20][2] > 0 and self.key_toggle_flag:
                self.key_toggle_flag = False
                print('open')
                self.ser.write('c40'.encode('utf-8'))
                time.sleep(0.001)

        return frame

    def Start_mode(self):
        if self.tracking_flag:
            self.tracking_flag = False
            self.Start_Button.configure(text='Start')
        else:
            self.tracking_flag = True
            self.Start_Button.configure(text='Stop')

    def Close_mode(self):
        self.ser.close()
        self.main_window.destroy()


Main()
