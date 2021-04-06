import tkinter as tk
import numpy as np
from PIL import Image, ImageTk

width = 600
height = 450
ok_dataset = []
i = 0

def accept():
  global i, ok_dataset
  ok_dataset.append(i)
  i += 1
  show_next_img()
  if i > 4000:
  	if len(ok_dataset) >= 3000:
  		label_hint.config(text = '三千張了喔', font = ('微軟正黑體', 35), fg = 'Red')



def deny():
  global i
  i += 1
  show_next_img()

def show_next_img():
  global i, dataset, img
  ndarr = dataset[i].reshape(28,28)
  img = Image.fromarray(ndarr)
  img = img.resize((280,280), Image.BILINEAR)
  img = ImageTk.PhotoImage(img)
  canvas.create_image(20, 20, anchor = 'nw', image = img)
  label_hint.config(text = f'這是第{i+1}張', font = ('Arial', 25))



# root_pre = tk.Tk()
# root.title('選擇要哪個資料集')
# root_pre.mainloop()


root = tk.Tk()
root.title('篩選資料集')
root.geometry(f'{width}x{height}')
root.resizable(False, False)

# !!!!!!!!!!!!!!修改↓!!!!!!!!!!!!!!!!!!!!!!!!
class_name = 'bear'
# !!!!!!!!!!!!!!修改↑!!!!!!!!!!!!!!!!!!!!!!!!


dataset = np.load(f'{class_name}.npy')
ndarr = dataset[i].reshape(28,28)
# print(ndarr)
img = Image.fromarray(ndarr)
img = img.resize((280,280), Image.BILINEAR)
img = ImageTk.PhotoImage(img)

frame_up = tk.Frame(root, width = 300, height = 50, bg = '#DCDCDC')
frame_up.pack()
label = tk.Label(frame_up)
label.config(text = class_name, font = ('Arial', 25))
label.pack()

canvas = tk.Canvas(root, width = 300, height = 300)
canvas.create_image(20, 20, anchor = 'nw', image = img)
canvas.pack()

frame = tk.Frame(root, width = 300, height = 50, bg = '#DCDCDC')
frame.pack()

btn_ok = tk.Button(frame)
btn_ok.config(text = 'O', font = ('Arial', 25), fg = '#FFFFFF', bg = '#0cf036', command = accept)
btn_ok.place(relx = 0.25, rely = 0)

btn_no_good = tk.Button(frame)
btn_no_good.config(text = 'X', font = ('Arial', 25), fg = '#FFFFFF', bg = '#ed2424', command = deny)
btn_no_good.place(relx = 0.65, rely = 0)

frame_bottom = tk.Frame(root, width = 300, height = 50, bg = '#A9A9A9')
frame_bottom.pack()
label_hint = tk.Label(frame_bottom)
label_hint.config(text = f'這是第{i+1}張', font = ('微軟正黑體', 25), fg = 'Blue')
label_hint.place(relx = 0.19, rely = 0)

root.mainloop()

with open(f'{class_name}.txt', 'a+') as f:
  f.write(str(ok_dataset))

print('DONE!!')