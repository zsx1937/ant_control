# show.py

## 运行环境

python3.7，建议安装anaconda和vscode

## 依赖同路径文件夹下文件

config.json

配置文件可配置展示界面所需文字，图片，和执行文件的地址，还可配置界面颜色，需配置正确

## 文件结构
使用tkinter搭建图形界面，主要分为三个模块
- send模块：使用checkbutton实现按下变色功能，send按钮绑定事件：telnet.py 把对应按钮代表的开关信息发送给个远端
- process模块：调用matlab生成的exe文件进行程序处理
- display模块：把process后得到的结果（分辨结果和展示图片）显示到结果区和展示区
## 程序中遇到的坑
- 在函数中修改configure时候注意加global，否则无法修改成功
- 耦合化严重，只有color部分是可配置部分，position，font和size都未去耦合，及其不易修改
## 界面

![](surface.png)

## author

[lovesatomi.xyz](http://47.100.138.49)，欢迎访问

## reference

[https://blog.csdn.net/ahilll/article/details/81531587](https://blog.csdn.net/ahilll/article/details/81531587)