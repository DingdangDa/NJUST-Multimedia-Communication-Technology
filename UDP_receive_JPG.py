# 文件：南京理工大学多媒体通信技术课设，UDP接收端模块
# 作者：黄炫宇 xuanyuhuang2001@gmail.com
# 说明：UDP接收端

import io
import os
import socket
import threading
import time
import tkinter as tk
import tqdm
from PIL import Image, ImageTk

def delay_remove(filename):
    time.sleep(1)
    os.remove(filename)

def recvived(address, port):
    # 传输数据间隔符
    SEPARATOR = '<SEPARATOR>'
    # 文件缓冲区
    Buffersize = 4096 * 10

    # 创建Tkinter窗口
    window = tk.Tk()
    window.title("屏幕截图")
    screen_label = tk.Label(window)
    screen_label.pack()

    while True:
        print('准备接收新的文件...')

        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.bind((address, port))
        recv_data = udp_socket.recvfrom(Buffersize)
        # try:
        recv_file_info = recv_data[0].decode('utf-8')  # 存储接收到的数据,文件名
        # except Exception as e:
        #     print(f"recv_data[0].decode发生异常: {str(e)}")
        print(f'接收到的文件信息{recv_file_info}')
        c_address = recv_data[1]  # 存储客户的地址信息
        # 打印客户端ip
        print(f'客户端{c_address}连接')
        # recv_data = udp_socket.recv()
        # 接收客户端信息
        # received = udp_socket.recvfrom(Buffersize).decode()
        filename, file_size = recv_file_info.split(SEPARATOR)
        # 获取文件的名字,大小
        filename = os.path.basename(filename)
        file_size = int(file_size)

        # 文件接收处理
        progress = tqdm.tqdm(range(file_size), f'接收{filename}', unit='B', unit_divisor=1024, unit_scale=True)

        with open(filename, 'wb') as f:
            for _ in progress:
                # 从客户端读取数据

                bytes_read = udp_socket.recv(Buffersize)
                # 如果没有数据传输内容
                # print(bytes_read)
                if bytes_read == b'file_download_exit':
                    print('完成传输！')
                    print(bytes_read)
                    break
                # 读取写入
                f.write(bytes_read)
                # 更新进度条
                progress.update(len(bytes_read))
        udp_socket.close()

        try:
            image = Image.open(filename)
            # 调整图像大小以适应窗口
            window_width, window_height = 1920, 1080
            image.thumbnail((window_width, window_height))

            image_bytes = io.BytesIO()
            image.save(image_bytes, format='PNG')
            image_bytes.seek(0)

            # 显示图像
            photo = ImageTk.PhotoImage(Image.open(image_bytes))
            screen_label.config(image=photo)
            screen_label.image = photo  # 保持引用，避免垃圾回收

            # 更新窗口
            window.update()
            image.close()  # 关闭图像对象
        except Exception as e:
            print(f"图像处理发生异常: {str(e)}")
            # 可以在此处进行异常处理操作，例如记录日志或发送错误通知

        t = threading.Thread(target=delay_remove, args=(filename,))
        t.start()

