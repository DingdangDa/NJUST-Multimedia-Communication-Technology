# 文件：南京理工大学多媒体通信技术课设，UDP发送端模块
# 作者：黄炫宇 xuanyuhuang2001@gmail.com
# 说明：UDP发送端

import threading
import socket
import tqdm
import os
import cv2
from time import ctime, sleep


def send(address, filename):
    # 传输数据间隔符
    SEPARATOR = '<SEPARATOR>'
    # 服务器信息
    host, port = address

    # 文件缓冲区
    Buffersize = 4096 * 10
    # 传输文件名字
    filename = filename
    # 文件大小)
    file_size = os.path.getsize(filename)
    # 创建socket链接
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(f'服务器连接中{host}:{port}')
    s.connect((host, port))
    print('与服务器连接成功')

    # 发送文件名字和文件大小，必须进行编码处理
    # s.sendto(f'{filename}{SEPARATOR}{file_size}'.encode(), ("127.0.0.1", 1234))
    s.send(f'{filename}{SEPARATOR}{file_size}'.encode('utf-8'))

    # 文件传输
    progress = tqdm.tqdm(range(file_size), f'发送{filename}', unit='B', unit_divisor=1024)

    with open(filename, 'rb') as f:
        # 读取文件
        for _ in progress:
            bytes_read = f.read(Buffersize)
            # print(bytes_read)
            if not bytes_read:
                print('exit退出传输，传输完毕！')
                s.sendall('file_download_exit'.encode('utf-8'))
                break
            # sendall 确保络忙碌的时候，数据仍然可以传输
            s.sendall(bytes_read)
            progress.update(len(bytes_read))
            sleep(0.001)

    # 关闭资源
    s.close()