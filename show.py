# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: lovesatomi.xyz
# reference : https://blog.csdn.net/ahilll/article/details/81531587

import tkinter as tk
import subprocess
import os
import json

###############################################################################
# Logic process & function define
###############################################################################
config = json.load(open("config.json"))

def writefile(path, content):
    f = open(path, 'w')
    f.write(content)
    f.close()

def readfile(path):
    f = open(path, 'r')
    c = f.read()
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


def ij2id(i,j):
    l = [0,1,2,3,-1,4,5,6,7]
    return l[i*3 + j]

# id              num
# 0  1  2         3  2  1
# 3     4   ->    4     8
# 6  7  8         5  6  7
def id2num(id):
    l = [3,2,1,4,8,5,6,7]
    return l[id]

###############################################################################
# Function connected to windows
###############################################################################
# Send Button
def send():
    # count status of checkbuttons
    status = [0,0,0,0,0,0,0,0]

    # for i in range(3):
    #     for j in range(3):
    #         if (i==1 and j==1):
    #             continue
    #         num = ij2id(i,j)
    #         if (varbuttons[num].get() == 1):
    #             status[num] = 1

    for id in range (8):
        num = id2num(id)
        if (varbuttons[id].get() == 1):
            status[num-1] = 1

    # read json
    exe_path = config['send_exe_path']
    commands_path = config['send_exe_paras']['commands_path']
    results_path = config['send_exe_paras']['results_path']
    host_ip = config['send_exe_paras']['host_ip']
    host_port = config['send_exe_paras']['host_port']
    paras = [commands_path,results_path,host_ip,host_port]

    # write para to commands.txt
    content="s " + str(bin2dec(status))
    writefile(commands_path, content)

    # call cmd
    if os.path.exists(exe_path):
        commands = exe_path
        for para in paras:
            commands = commands + " " + para
        rc, out = subprocess.getstatusoutput(commands)
        if (rc == 0):
            var_tips.set("send success")
        else:
            print("send fail!")
            var_tips.set("send fail!")
        #print(out)
    else:
        print("send exe file not exist!")
        var_tips.set("send exe file not exist!")


# Process Button
process_path="notepad"
def process():
    # read json
    exe_path = config['process_exe_path']
    para1 = config['process_exe_paras']['para1']
    paras = [para1]
    #if os.path.exists(process_path):
    if 1:
        command = exe_path
        for para in paras:
            command = command + " " + para
        rc, out = subprocess.getstatusoutput(command)
        print(rc)
        print('*' * 10)
        print(out)
    var_tips.set("process success")

# Display Button
def display():
    # read json
    exe_path = config['display_exe_path']
    results_path = config['display_exe_paras']['results_path']
    c = readfile(results_path)
    status = dec2bin(int(c))

    for id in range(8):
        num = id2num(id)
        if status[num-1] == 1 :
            var_strings[id].set("1")
        else:
            var_strings[id].set("0")
    # for i in range(3):
    #     for j in range(3):
    #         if (i==1 and j ==1 ):
    #             continue
    #         num = ij2num(i,j)
    #         if status[num]==1:
    #             var_strings[num].set("1")
    #         else:
    #             var_strings[num].set("0")
    var_tips.set("display success")

###############################################################################




###############################################################################
# Init windows
###############################################################################
window = tk.Tk()
window.title('SuperView')
window.geometry('800x500')  # 这里的乘是小x
window['bg'] = 'black'


###############################################################################
# 8 Checkbuttons
###############################################################################
# Position
start_x = 50
start_y = 50
step = 100
varbuttons = []
#cbuttons = []

# Generate 8 checkbutton
# ----------------> x
# |
# |
# y
for i in range(3):
    for j in range(3):
        if (i==1 and j==1):
            continue
        id = ij2id(i,j)
        num = id2num(id)
        x = start_x + step * j
        y = start_y + step * i
        varnum = tk.IntVar()
        varbuttons.append(varnum)
        cnum = tk.Checkbutton(window, text="ANT" + str(num),variable=varnum, onvalue=1, offvalue=0).place(x=x, y=y, anchor='nw')
        #cbuttons.append(cnum)

###############################################################################
# 8 Display Text
###############################################################################
# Position
start_dx = 400
start_dy = 50
stepd = 100
var_strings = []

# Generate display text
for i in range(3):
    for j in range(3):
        if (i==1 and j==1):
            continue
        id = ij2id(i,j)
        num = id2num(id)
        x = start_dx + stepd * j
        y = start_dy + stepd * i
        varnum = tk.StringVar()
        var_strings.append(varnum)
        tk.Label(window, textvariable=varnum, bg='green', fg='white', font=('Arial', 12), width=4, height=2).place(x=x,y=y,anchor='nw')

###############################################################################
# 3 buttons
###############################################################################
# Position
start_bx = 50
start_by = 350
step_bx = 100

b_send = tk.Button(window, text='Send', font=('Arial', 12), width=10, height=1, command=send).place(x=start_bx + step_bx * 0, y=start_by, anchor='nw')
b_process = tk.Button(window, text='Process', font=('Arial', 12), width=10, height=1, command=process).place(x=start_bx + step_bx * 1, y=start_by, anchor='nw')
b_display = tk.Button(window, text='Display', font=('Arial', 12), width=10, height=1, command=display).place(x=start_bx + step_bx * 2, y=start_by, anchor='nw')

###############################################################################
# Tips Text
###############################################################################
x_tips = 50
y_tips = 400
var_tips = tk.StringVar()
tk.Label(window, text="Tips: ",bg='grey', fg='black', font=('Arial', 12), width=5, height=1).place(x=x_tips, y=y_tips,anchor='nw')
tk.Label(window, textvariable=var_tips, bg='grey', fg='black', font=('Arial', 12), width=70, height=1,anchor='w').place(x=x_tips+50, y=y_tips,anchor='nw')


###############################################################################
# Windows loop
###############################################################################
window.mainloop()
