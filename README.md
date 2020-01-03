# show.py

## 运行环境

python3.7，建议安装anaconda和vscode
使用pyinstaller生成exe
```
pyinstaller telnet.py
pyinstaller show.py
```

## 依赖同路径文件夹下文件

config.json

配置文件可配置展示界面所需文字，图片，和执行文件的地址，还可配置界面颜色，需配置正确

## 文件结构
使用tkinter搭建图形界面，主要分为三个模块
- send模块：使用checkbutton实现按下变色功能，send按钮绑定事件：telnet.py 把对应按钮代表的开关信息发送给个远端
- process模块：调用matlab生成的exe文件进行程序处理
- display模块：把process后得到的结果（分辨结果和展示图片）显示到结果区和展示区

## 界面
![](surface.png)

## 程序中遇到的坑
- 在函数中修改configure时候注意加global，否则无法修改成功，具体代码如下
```
    # image display
    global img_width,img_height,display_img
    photo_url = config["display_img_path"]
    pil_image = Image.open(photo_url)
    pil_image = pil_image.resize((img_width, img_height),Image.ANTIALIAS)
    display_img= ImageTk.PhotoImage(pil_image)
    label_display.configure(image = display_img,width=img_width,height=img_height)
```


- 耦合化严重，只有color部分是可配置部分，position，font和size都未去耦合，不易修改

# telnet.py
两种调用方式：
- 带参数的，需要手动输入四个参数：`telnet.exe commands.txt results.txt 192.168.10.200 4001`，无需配置文件
- 不带参数的，可以直接运行exe，但需配置文件telnet_config.json与执行文件在同一路径下


# Author

[lovesatomi.xyz](http://47.100.138.49)，欢迎访问

# Reference

[https://blog.csdn.net/ahilll/article/details/81531587](https://blog.csdn.net/ahilll/article/details/81531587)