# 文件：南京理工大学多媒体通信技术课设，主程序
# 作者：黄炫宇 xuanyuhuang2001@gmail.com
# 说明：功能选择，调用对应的模块
import os
import threading
import time
import haffman
import LZW
import UDP_send_JPG
import UDP_receive_JPG
from PIL import ImageGrab

def file_remove(filename):
    os.remove(filename)

if __name__ == '__main__':
    while 1:
        print("1. Haffman")
        print("2. LZW")
        print("3. UDP-Socket")
        function_choose = input("请输入：")
        if function_choose == "1":
            haffman_str_default = input("Input a str or \"0\" to use a default str \"NJUSTMultimedia\"")
            if haffman_str_default == "0":
                haffman_str = "NJUSTMultimedia"
            else:
                haffman_str = haffman_str_default
            print("计数:", haffman.freChar(haffman_str))  # 计数后的结果
            tree = haffman.HuffmanTree(haffman.freChar(haffman_str))
            tree.get_code()
        elif function_choose == "2":
            LZW_str_default = input("Input a str or \"0\" to use a default str \"NJUSTMultimedia\"")
            if LZW_str_default == "0":
                LZW_str = "NJUSTMultimedia"
            else:
                LZW_str = LZW_str_default
            LZW.LZW(LZW_str)
        elif function_choose == "3":
            UDP_send_or_receive = input("Input \"0\" to send or \"1\" to receive")
            if UDP_send_or_receive == "0":
                host = input("Input the target IP or \"0\" to use a default IP")
                if host == "0":
                    host = "192.168.10.27"
                port = int(input("Input the target port or \"0\" to use a default port"))
                if port == 0:
                    port = 1234
                address = (host, port)
                while 1:
                    filename_time = time.strftime("%H-%M-%S", time.localtime())
                    filename = filename_time + 'S.jpg'
                    pic = ImageGrab.grab()
                    pic.save(filename)
                    # t = threading.Thread(target=UDP_send_JPG.send, args=(address, filename))
                    # t.start()
                    UDP_send_JPG.send(address, filename)
                    time.sleep(0.5)
                    t_remove = threading.Thread(target=file_remove, args=(filename,))
                    t_remove.start()
                # received(address, filename)
            elif UDP_send_or_receive == "1":
                address = input("Input the receive address or \"0\" to use a default address")
                if address == "0":
                    address = "192.168.10.27"
                port = int(input("Input the receive port or \"0\" to use a default port"))
                if port == 0:
                    port = 1234
                t = threading.Thread(target=UDP_receive_JPG.recvived, args=(address, port))
                t.start()
                # send(address)
            else:
                print("Wrong input")
        else:
            print("Wrong input")
