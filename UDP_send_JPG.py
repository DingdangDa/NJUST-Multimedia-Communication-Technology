import socket
import time
import threading
import pyautogui
import cv2
import numpy as np


# 发送截屏图像
def send_msg():
    while True:
        # 起始坐标 0  0  截取一张 X宽  y 高的图像  返回数据类型PIL.Image.Image image mode=RGB
        pil_im = pyautogui.screenshot(region=(0, 0, pic_width, pic_height))
        # 将PIL.Image.Image 转换为  numpy.ndarray 类型的数组 可以 使用cv2.imshow('a', np_img)显示
        np_img = cv2.cvtColor(np.asarray(pil_im), cv2.COLOR_RGB2BGR)
        # 将图片编码  send_data_num为0-255数字
        res, send_data_num = cv2.imencode('.jpg', np_img, (cv2.IMWRITE_JPEG_QUALITY, 50))
        send_data = send_data_num.tobytes()  # 编码转换为 字节流
        send_data_len = len(send_data)  # 获取数据长度
        i = send_data_len // package_len  # 分包发送 包的个数
        j = send_data_len % package_len  # 剩余字节的个数
        client.sendto(begin_flag, host)  # 发送起始标志
        for n in range(0, i):  # 分包发送
            client.sendto(send_data[n * package_len:package_len * (n + 1)], host)
        client.sendto(send_data[-j:], host)  # 发送剩余字节
        client.sendto(end_flag, host)  # 发送结束标志
        # time.sleep(10)


# 接受数据
def recv_data():
    while True:
        back_data = client.recv(1024).decode()
        print('收到服务器端的信息：' + back_data)


# 截屏的大小
pic_width = 800
pic_height = 600
begin_flag = b'Framebegin:'  # 一张图像起始标志
end_flag = b'Frameovers:'  # 一张图片结束标志
package_len = 1024  # 包的大小
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = ('121.4.99.98', 8081)
client.sendto("Client Msg".encode(), host)  # 要先向服务器发送一条数据 建立连接  连接不上服务器 也不报错
t0 = threading.Thread(target=recv_data)
t0.start()
t1 = threading.Thread(target=send_msg)
t1.start()

