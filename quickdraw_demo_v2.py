import tkinter as tk
from matplotlib import pyplot as plt
import numpy as np
import math
import random
from PIL import ImageTk, Image
import load_model_v2 as load_model
import time
from threading import Timer


# 可以在這邊設定繪圖畫板長寬，範例畫板是16:9
width = 960
height = 540
topic_class = ['飛機', '蝙蝠', '熊', '鳥', '蠟燭', '車', '大象', '眼睛', '花朵', '冰淇淋', '鑰匙', '棒棒糖', '老鼠', '嘴巴', '鼻子', '豬', '鯊魚', '草莓', '太陽', '電視']
topic_class_eng = ['airplane', 'bat', 'bear', 'bird', 'candle', 'car', 'elephant', 'eye', 'flower', 'ice_cream', 'key', 'lollipop', 'mouse', 'mouth', 'nose', 'pig', 'shark', 'strawberry', 'sun', 'television']
dictionary = dict(zip(topic_class_eng, topic_class))


# #########主畫面TK區
class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        # super().__init__(self) # 太詭異了吧 為什麼這個不行上面可以
        self._frame = None
        self.resizable(False, False)
        self.switch_frame(StartPage)
        self.title('造畫弄人!!')

    def switch_frame(self, frame_class):
        # frame_class 要繼承自tk.Frame，傳入自己(i.e. SampleApp， 也就是tk.Tk())建構
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()
# ##########主畫面TK區

# ##########首頁Frame


class StartPage(tk.Frame):
    def __init__(self, master):
        global width, height
        tk.Frame.__init__(self, master)
        self.ref = Image.open('image/main.png')
        self.ref = self.ref.resize((width, height), Image.BILINEAR)
        self.bg_image = ImageTk.PhotoImage(self.ref)

        # tk.Label(self,image = bg_image,width = width, height = height*1.2).pack()
        tk.Label(self, image=self.bg_image).pack()

        tk.Button(self, text='Game Start', font=('Arial', 25), fg='Blue',
                  command=lambda: master.switch_frame(MainPage)).pack()
# ##########首頁Frame

# ##########遊戲頁Frame


class MainPage(tk.Frame):
    # constructor
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.stroke = 0
        self.draw = [[[], []]]
        self.predictions_stack = []
        self.guessed = []
        self.guessed_index = 0
        self.construct()
        self.t = Timer(20, self.times_up)
        self.t.start()
    # constructor

    # 計時器(背景執行緒)
    def times_up(self):
        self.master.switch_frame(FailureEndingPage)
    # 計時器(背景執行緒)

    # 畫畫中
    def drawing(self, event):
        global width, height
        color = 'Black'
        x, y = event.x, event.y
        self.canvas.create_oval((x-12), (y-12), (x+12), (y+12), fill=color)
        self.draw[self.stroke][0].append(x*256//(width-100))
        self.draw[self.stroke][1].append(y*256//(height-30))
    # 畫畫中

    # 提起畫筆
    def end_stroke(self, event):
        global dictionary
        if self.draw[self.stroke] != [[], []]:
            self.stroke += 1
            self.draw.append([[], []])
        if (self.stroke > 0) and (self.stroke % 3 == 0):
            self.auto_predict()

        if self.predictions_stack:
            guess = dictionary[self.predictions_stack[self.guessed_index]]
            if guess not in self.guessed:
                self.answer_lbl.config(
                    text=f'我猜你畫的是...{guess}', font=('微軟正黑體', 20))
                self.guessed_index += 1
                self.guessed_index %= 3
            if self.answer == guess:
                print('猜中了')
                self.t.cancel()
                time.sleep(0.5)
                self.master.switch_frame(EndingPage)
            else:
                self.guessed.append(guess)
                print(f'沒中, guessed = {self.guessed}')

    # 提起畫筆

    # 清除畫布
    def clear(self):
        self.canvas.delete('all')
        self.stroke = 0
        self.draw = [[[], []]]
        self.answer_lbl.config(text='...')
    # 清除畫布

    # 換題目
    def change_topic(self):
        ind = random.randint(1, len(topic_class))
        self.answer = topic_class[ind-1]
        self.question.config(text=f'題目: {self.answer}')
        self.clear()
        self.t.cancel()
        self.t = Timer(20, self.times_up)
        self.t.start()
    # 換題目

    # 跑預測
    def auto_predict(self):
        global predictions
        if self.isListEmpty(self.draw):
            return
        # 可能
        self.draw.pop()

        self.predictions_stack = load_model.predict(self.draw)

        self.draw.append([[], []])
        # self.master.switch_frame(PredictionPage)
    # 跑預測

    # 檢查陣列是不是空空的
    def isListEmpty(self, inList):
        if isinstance(inList, list):  # Is a list
            return all(map(self.isListEmpty, inList))
        return False
    # 檢查陣列是不是空空的

    def construct(self):
        global width, height
        # 上層區塊
        self.frame_top = tk.Frame(
            self, width=width-100, height=30, bg='#DCDCDC')
        self.frame_top.pack()

        # 清除畫布按鈕
        self.clear_btn = tk.Button(self.frame_top)
        self.clear_btn.config(text='神奇橡皮擦', font=(
            '微軟正黑體', 14), command=self.clear, fg="Blue")
        self.clear_btn.place(relx=0.16, rely=0)
        # 清除畫布按鈕

        # 題目標示
        self.question = tk.Label(self.frame_top)
        # #隨機出題
        ind = random.randint(1, len(topic_class))
        self.answer = topic_class[ind-1]
        # #隨機出題
        self.question.config(
            text=f'題目: {self.answer}', font=('微軟正黑體', 16), fg='Blue')
        self.question.place(relx=0.4, rely=0)
        # 題目標示

        # 切換題目按鈕
        self.submit_btn = tk.Button(self.frame_top)
        self.submit_btn.config(text='重抽題目', font=(
            '微軟正黑體', 14), command=self.change_topic, fg="Blue")
        self.submit_btn.place(relx=0.6, rely=0)
        # 切換題目按鈕
        # 上層區塊

        # 中間繪圖畫布
        self.frame_canvas = tk.Frame(self, width=width-100, height=height-30)
        self.frame_canvas.pack()

        self.canvas = tk.Canvas(
            self.frame_canvas, width=width-100, height=height-30, bg='White')
        self.canvas.place(relx=0, rely=0)
        self.canvas.bind('<Button1-Motion>', self.drawing)  # 按著滑鼠左鍵滑動
        self.canvas.bind('<Button1-ButtonRelease>', self.end_stroke)  # 放開滑鼠左鍵
        # 中間繪圖畫布

        # 下層顯示作答區塊
        self.frame_bottom = tk.Frame(
            self, width=width-100, height=50, bg='#DCDCDC')
        self.frame_bottom.pack()

        self.answer_lbl = tk.Label(
            self.frame_bottom, text='...', font=('Arial', 20), fg='Red')
        self.answer_lbl.pack()
        # 下層顯示作答區塊

# ##########遊戲頁Frame

# ##########看之後要不要做個統計頁面這樣
# class PredictionPage(tk.Frame):
#   def __init__(self, master):
#     global predictions, dictionary
#     tk.Frame.__init__(self, master)
#     self.ref = Image.open('image/ending.png')
#     self.ref = self.ref.resize((400,400), Image.BILINEAR)
#     self.bg_image = ImageTk.PhotoImage(self.ref)
#     tk.Label(self, image = self.bg_image).pack()

#     tk.Label(self, text = f'我們的神經網路判斷你畫的是...{dictionary[predictions[0]]}', font = ('微軟正黑體', 30), fg = 'Red').pack()
#     tk.Label(self, text = f'我們的神經網路覺得你畫的還可能是...{dictionary[predictions[1]]}', font = ('微軟正黑體', 16), fg = 'Green').pack()
#     tk.Label(self, text = f'我們的神經網路覺得你畫的還可能是...{dictionary[predictions[2]]}', font = ('微軟正黑體', 16), fg = 'Green').pack()
#     tk.Label(self, text = f'我們的神經網路覺得你畫的還可能是...{dictionary[predictions[3]]}', font = ('微軟正黑體', 16), fg = 'Green').pack()
#     tk.Label(self, text = f'我們的神經網路覺得你畫的還可能是...{dictionary[predictions[4]]}', font = ('微軟正黑體', 16), fg = 'Green').pack()


#     tk.Button(self, text = '想回到最初的起點', font = ('微軟正黑體', 25), fg = 'Blue', command = lambda:master.switch_frame(StartPage)).pack()
# ##########看之後要不要做個統計頁面這樣


# ##########結束頁Frame
class EndingPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text='恭喜！你是靈魂繪師', font=('微軟正黑體', 25), fg='Red').pack()
        self.ref = Image.open('image/ending.png')
        self.ref = self.ref.resize((960, 485), Image.BILINEAR)
        self.bg_image = ImageTk.PhotoImage(self.ref)
        tk.Label(self, image=self.bg_image).pack()
        tk.Button(self, text='想回到最初的起點', font=('微軟正黑體', 25), fg='Blue',
                  command=lambda: master.switch_frame(StartPage)).pack()
# ##########結束頁Frame

# ##########失敗頁Frame


class FailureEndingPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text='施主,您還是多修練修練畫工吧',
                 font=('微軟正黑體', 25), fg='Red').pack()
        self.ref = Image.open('image/ending.png').convert('LA')
        self.ref = self.ref.resize((960, 485), Image.BILINEAR)
        self.bg_image = ImageTk.PhotoImage(self.ref)
        tk.Label(self, image=self.bg_image).pack()
        tk.Button(self, text='想回到最初的起點', font=('微軟正黑體', 25), fg='Blue',
                  command=lambda: master.switch_frame(StartPage)).pack()
# ##########失敗頁Frame


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
