# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: lovesatomi.xyz
# reference : https://blog.csdn.net/ahilll/article/details/81531587

import tkinter as tk
from PIL import Image,ImageTk
import subprocess
import os
import json
import time
from win32com.client import Dispatch

###############################################################################
# Logic process & function define
###############################################################################
# Load config
config_json = open("config.json")
try:
    config = json.load(config_json)
except Exception:
    print("Read config error!")
    exit()
finally:
    config_json.close()


def writefile(path, content):
    f = open(path, 'w')
    try:
        f.write(content)
    except Exception:
        print("Write file error!")
    finally:
        f.close()


def readfile(path):
    f = open(path, 'r',encoding="utf-8")
    try:
        c = f.read()
    except Exception:
        print("Read file error!")
        c = ""
    finally:
        f.close()
    return c

# 1 -> [1000000] , 2-> [01000000] , 254 -> [0111111]
def dec2bin(num):
    res = []
    for i in range(8):
        res.append(num % 2)
        num = int(num / 2)
    return res


def bin2dec(bin_list):
    res = 0
    for i in range(8):
        res = res * 2 + bin_list[7 - i]
    return res



# i*3+j           id              num
# 0  1  2         0  1  2         3  2  1
# 3  4  5   ->    3         ->    4      
# 6  7  8         4  5  6         5  6  7

ids = [0,1,2,3,-1,-1,4,-1,-1]
nums = [3,2,1,4,5]

def ij2id(i, j):
    #l = [0, 1, 2, 3, -1, 4, 5, 6, 7]
    global ids
    return ids[i * 3 + j]

def id2num(id):
    #l = [3, 2, 1, 4, 8, 5, 6, 7]
    global nums
    return nums[id]


###############################################################################
# Function connected to windows
###############################################################################
def var_tips_clean():
    var_tips.set("")
    window.update_idletasks()
    time.sleep(0.1)

# Send Button
def send():
    var_tips_clean()
    # count status of checkbuttons
    status = [0, 0, 0, 0, 0, 0, 0, 0]

    # for i in range(3):
    #     for j in range(3):
    #         if (i==1 and j==1):
    #             continue
    #         num = ij2id(i,j)
    #         if (varbuttons[num].get() == 1):
    #             status[num] = 1

    for id in range(len(nums)):
        num = id2num(id)
        if (varbuttons[id].get() == 1):
            status[num - 1] = 1

    # read json
    exe_path = config['send_exe_path']
    commands_path = config['send_exe_paras']['commands_path']
    results_path = config['send_exe_paras']['results_path']
    host_ip = config['send_exe_paras']['host_ip']
    host_port = config['send_exe_paras']['host_port']
    paras = [commands_path, results_path, host_ip, host_port]

    # write para to commands.txt
    content = "s " + str(bin2dec(status))
    writefile(commands_path, content)

    # call cmd
    if os.path.exists(exe_path):
        commands = exe_path
        for para in paras:
            commands = commands + " " + para
        rc, out = subprocess.getstatusoutput(commands)
        if (rc == 0):
            var_tips.set("Send success!")
        else:
            print("Send fail!")
            var_tips.set("Send fail!")
            return
        print(out)
    else:
        print("Send exe file not exist!")
        var_tips.set("Send exe file not exist!")
        return


# Process Button
def process():
    var_tips_clean()
    # read json
    exe_path = config['process_exe_path']
    #paras = []
    if os.path.exists(exe_path):
    #if 1:
        command = exe_path
        #for para in paras:
        #    command = command + " " + para
        #rc, out = subprocess.getstatusoutput(command)
        os.system(command)
        var_tips.set("Process success!")
    else:
        print("Process exe file not exist!")
        var_tips.set("Process exe file not exist!")
        return
    


# Display Button
def display():
    var_tips_clean()
    # read json
    results_path = config['display_result_path']
    if os.path.exists(results_path):
        pass
    else:
        print("Result file not exist!")
        var_tips.set("Result file not exist!")
        return
    c = readfile(results_path)
    if int(c)==-1:
        print("Classify error!")
        var_tips.set("Classify error!")
        return
    status = dec2bin(int(c))

    # image display
    global img_width,img_height,display_img
    photo_url = config["display_img_path"]
    if os.path.exists(photo_url):
        pass
    else:
        print("Image file not exist!")
        var_tips.set("Image file not exist!")
        return
    pil_image = Image.open(photo_url)
    pil_image = pil_image.resize((img_width, img_height),Image.ANTIALIAS)
    display_img= ImageTk.PhotoImage(pil_image)
    label_display.configure(image = display_img,width=img_width,height=img_height)

    #text_display.
    for id in range(len(nums)):
        num = id2num(id)
        if status[num - 1] == 1:
            #var_strings[id].set("1")
            dlabels[id].configure(bg=config['result_bg1'])
        else:
            #var_strings[id].set("0")
            dlabels[id].configure(bg=config['result_bg0'])
    # for i in range(3):
    #     for j in range(3):
    #         if (i==1 and j ==1 ):
    #             continue
    #         num = ij2num(i,j)
    #         if status[num]==1:
    #             var_strings[num].set("1")
    #         else:
    #             var_strings[num].set("0")
    var_tips.set("Display success!")

# M-matrix button

def mmatrix():
    var_tips_clean()
    # need to use the third library win32com.client
    file_path = config["mmatrix_file_path"]
    if os.path.exists(file_path):
        xlApp = Dispatch('EXCEL.Application')
        xlApp.Visible = True
        xlApp.Workbooks.Open(file_path)
        var_tips.set("M-matrix success!")
    else:
        print("Mmatrix file not exist!")
        var_tips.set("Mmatrix file not exist!")
        return
    

# Update time
def update_time():
    clock_label.configure(text=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))
    clock_label.after(1000,update_time)
###############################################################################


###############################################################################
# Init windows
###############################################################################
window = tk.Tk()
window.title('SuperView')
window.geometry('1200x950') 
window['bg'] = config['background_color']

###############################################################################
# Title
###############################################################################
x_title = 250
y_title = 30
tk.Label(window, text="上海交通大学超孔径项目", bg=config['title_bg'], fg=config['title_fg'], font=("SimHei", 24, "bold"), width=40, height=2).place(x=x_title, y=y_title,anchor='nw')

###############################################################################
# 3 Distribute Title
###############################################################################
x_distribute = 50
y_distribute = 150
tk.Label(window, text="发射区", bg=config["distribute_title_bg"], fg=config["distribute_title_fg"], font=('Arial', 12), width=26, height=1).place(x=x_distribute, y=y_distribute,anchor='nw')
tk.Label(window, text="判别结果", bg=config["distribute_title_bg"], fg=config["distribute_title_fg"], font=('Arial', 12), width=26, height=1).place(x=x_distribute+350, y=y_distribute,anchor='nw')
tk.Label(window, text="采样值", bg=config["distribute_title_bg"], fg=config["distribute_title_fg"], font=('Arial', 12), width=30, height=1).place(x=x_distribute+740, y=y_distribute,anchor='nw')


###############################################################################
# 8 Checkbuttons
###############################################################################
# Position
start_x = 50
start_y = 200
step = 100
varbuttons = []
# cbuttons = []

# Generate 8 checkbutton
# ----------------> x
# |
# |
# y
for i in range(3):
    for j in range(3):
        id = ij2id(i, j)
        if id == -1:
            continue
        num = id2num(id)
        x = start_x + step * j
        y = start_y + step * i
        varnum = tk.IntVar()
        varbuttons.append(varnum)
        cnum = tk.Checkbutton(window, text="ANT" + str(num), variable=varnum, onvalue=1, offvalue=0,bg=config["button_bg0"],indicatoron=False,selectcolor=config["button_bg1"]).place(x=x, y=y,anchor='nw')
        #cbuttons.append(cnum)


###############################################################################
# 2 Min Distance
###############################################################################
x_h_distance = 100
y_h_distance = 200
tk.Label(window, text="22.5cm", bg=config["background_color"], fg=config["min_distance_fg"], font=('Arial', 10), width=5, height=1).place(x=x_h_distance, y=y_h_distance,anchor='nw')

x_v_distance = 50
y_v_distance = 250
tk.Label(window, text="77.5cm", bg=config["background_color"], fg=config["min_distance_fg"], font=('Arial', 10), width=5, height=1).place(x=x_v_distance, y=y_v_distance,anchor='nw')

###############################################################################
# 8 Display Label
###############################################################################
# Position
start_dx = 400
start_dy = 200
stepd = 100
var_strings = []
dlabels = []

# Generate display text
for i in range(3):
    for j in range(3):
        id = ij2id(i, j)
        if id == -1:
            continue
        num = id2num(id)
        x = start_dx + stepd * j
        y = start_dy + stepd * i
        varnum = tk.StringVar()
        var_strings.append(varnum)
        dlabel = tk.Label(window, textvariable=varnum, bg=config['result_bg0'], fg=config['result_fg'], font=('Arial', 12), width=4, height=2)
        dlabel.place(x=x,y=y,anchor='nw')
        dlabels.append(dlabel)

###############################################################################
# Display img (by using label)
###############################################################################
x_display = 700
y_display = 200

img_width = 450
img_height = 450
label_display = tk.Label(window,width=0, height=0,bg=config["background_color"])
label_display.place(x=x_display, y=y_display,anchor='nw')
photo_url = config["default_img_path"]
pil_image = Image.open(photo_url)
pil_image = pil_image.resize((img_width, img_height),Image.ANTIALIAS)
display_img= ImageTk.PhotoImage(pil_image)
label_display.configure(image = display_img,width=img_width,height=img_height)

###############################################################################
# Discribe txt
###############################################################################
x_discribe = 50
y_discribe = 480
text_discribe_content = readfile(config["illustration_path"])

text_discribe = tk.Text(window, bg=config['discribe_bg'], fg=config['discribe_fg'], font=('Arial', 12), width=65, height=10)
text_discribe.place(x=x_discribe, y=y_discribe,anchor='nw')
text_discribe.insert(tk.INSERT,text_discribe_content)
text_discribe.config(state=tk.DISABLED)


###############################################################################
# 4 buttons
###############################################################################
# Position
start_bx = 50
start_by = 740
step_bx = 100

b_send = tk.Button(window, text='Send', font=('Arial', 12), width=10, height=1, command=send).place(x=start_bx + step_bx * 0, y=start_by, anchor='nw')
b_process = tk.Button(window, text='Process', font=('Arial', 12), width=10, height=1, command=process).place(x=start_bx + step_bx * 1, y=start_by, anchor='nw')
b_display = tk.Button(window, text='Display', font=('Arial', 12), width=10, height=1, command=display).place(x=start_bx + step_bx * 2, y=start_by, anchor='nw')
b_mmatrix = tk.Button(window, text='M-matrix', font=('Arial', 12), width=10, height=1, command=mmatrix).place(x=start_bx + step_bx * 3, y=start_by, anchor='nw')
#b_quit = tk.Button(window, text='Quit', font=('Arial', 12), width=10, height=1, command=exit).place(x=start_bx + step_bx * 4, y=start_by, anchor='nw')
###############################################################################
# Tips Text
###############################################################################
x_tips = 50
y_tips = 800
var_tips = tk.StringVar()
tk.Label(window, text="Tips: ", bg=config["tips_bg"], fg=config["tips_fg"], font=('Arial', 12), width=5, height=1).place(x=x_tips, y=y_tips,anchor='nw')
tk.Label(window, textvariable=var_tips, bg=config["tips_bg"], fg=config["tips_fg"], font=('Arial', 12), width=60, height=1,anchor='w').place(x=x_tips + 50, y=y_tips, anchor='nw')


###############################################################################
# Copyright
###############################################################################
x_copyright = 600
y_copyright = 900
tk.Label(window, text="Copyright © 2019 SJTU.All Rights Reserved.", bg=config["background_color"], fg=config["copyright_fg"], font=('Arial', 10), width=50, height=1).place(x=x_copyright, y=y_copyright,anchor='n')


###############################################################################
# Divided line
###############################################################################
x_canva_h1 = 345
y_canva_h1 = 150
w_canva_h1 = 1
h_canva_h1 = 300
canva_h1 = tk.Canvas(window, bg=config['canvas_bg'], width=w_canva_h1, height=h_canva_h1)
canva_h1.place(x=x_canva_h1, y=y_canva_h1,anchor='n')



x_canva_h2 = 670
y_canva_h2 = 150
w_canva_h2 = 1
h_canva_h2 = 550
canva_h2 = tk.Canvas(window, bg=config['canvas_bg'], width=w_canva_h2, height=h_canva_h2)
canva_h2.place(x=x_canva_h2, y=y_canva_h2,anchor='n')


x_canva_v1 = 600
y_canva_v1 = y_canva_h2 + h_canva_h2
w_canva_v1 = 1100
h_canva_v1 = 1
canva_v1 = tk.Canvas(window, bg=config['canvas_bg'], width=w_canva_v1, height=h_canva_v1)
canva_v1.place(x=x_canva_v1, y=y_canva_v1,anchor='n')



###############################################################################
# Windows loop
###############################################################################

x_clock = 950
y_clock = 850
clock_label = tk.Label(window, text="", bg=config["background_color"], fg=config["clock_fg"], font=('Arial', 11), width=25, height=1)
clock_label.place(x=x_clock, y=y_clock,anchor='nw')
update_time()

###############################################################################
# Windows loop
###############################################################################
window.mainloop()
