import threading
import haffman
import LZW
import UDP_send_JPG
import UDP_receive_JPG
from PIL import ImageGrab

if __name__ == '__main__':
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
        t = haffman.nodeQeuen(haffman.freChar(haffman_str))
        tree = haffman.creatHuffmanTree(t)
        haffman.HuffmanCodeDic(tree, '')
        print("哈夫曼编码如下：\n", haffman.codeDic)
        print("原字符串为：\n", haffman_str)
        a = haffman.TransEncode(haffman_str)
        print("经哈夫曼编码转换后如下：", a)
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
                host = "127.0.0.1"
            port = int(input("Input the target port or \"0\" to use a default port"))
            if port == "0":
                port = 1234
            address = (host, port)
            pic = ImageGrab.grab()
            pic.save('1.jpg')
            filename = '1.jpg'
            t = threading.Thread(target=UDP_send_JPG.send, args=(address, filename))
            t.start()
            # received(address, filename)
        elif UDP_send_or_receive == "1":
            address = input("Input the receive address or \"0\" to use a default address")
            if address == "0":
                address = "127.0.0.1"
            port = int(input("Input the receive port or \"0\" to use a default port"))
            if port == "0":
                port = 1234
            t = threading.Thread(target=UDP_receive_JPG.recvived, args=(address, port))
            t.start()
            # send(address)
        else:
            print("Wrong input")
    else:
        print("Wrong input")