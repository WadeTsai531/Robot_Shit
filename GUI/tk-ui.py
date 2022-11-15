# -*- coding: UTF-8 -*-
import tkinter as tk  # 大小寫要注意,如果小寫不行就改大寫
import time
from PIL import ImageTk, Image, ImageDraw
import random


def st():
    # 亂數產生1~4的數字
    s = random.randint(1, 4)
    img_right = ImageTk.PhotoImage(Image.open('D:\\' + str(s) + '.jpg'))  # 取得圖片
    label_right.imgtk = img_right  # 換圖片
    label_right.config(image=img_right)  # 換圖片


def ed():
    s1 = random.randint(1, 4)
    img_left = ImageTk.PhotoImage(Image.open('D:\\' + str(s1) + '.jpg'))
    label_left.imgtk = img_left
    label_left.config(image=img_left)


# 創建一個視窗
top = tk.Tk()
# 視窗名稱
top.title('GUI')
# 寬:300高:200的視窗,放在寬:600高:300的位置
top.geometry('1200x500+200+100')

# 開啟照片
img = ImageTk.PhotoImage(Image.open('hand 5.png'))
img2 = ImageTk.PhotoImage(Image.open('hand 5.png'))

# 用label來放照片
label_right = tk.Label(top, height=360, width=480, bg='gray94', fg='blue', image=img)
label_left = tk.Label(top, height=360, width=480, bg='gray94', fg='blue', image=img2)
# 按鈕
button_1 = tk.Button(top, text='start', bd=4, height=4, width=22, bg='gray94', command=st)
button_2 = tk.Button(top, text='close', bd=4, height=4, width=22, bg='gray94', command=ed)

# 位置
label_right.grid(row=1, column=0, padx=20, pady=20, sticky="nw")
label_left.grid(row=1, column=0, padx=600, pady=20, sticky="nw")
button_1.grid(row=1, column=0, padx=150, pady=400, sticky="nw")
button_2.grid(row=1, column=0, padx=760, pady=400, sticky="nw")
top.mainloop()  # 執行視窗
