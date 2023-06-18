# 文件：南京理工大学多媒体通信技术课设，LZW编码模块
# 作者：黄炫宇 xuanyuhuang2001@gmail.com
# 说明：LZW编码

def LZW(string):
    print("压缩前的编码：", string)

    dictionary = {chr(i): i for i in range(0, 256)}  # 导入ASC码进入字典1
    last = 256  # 新的编码从第256位开始
    p = ""  # 定义前一个字符，开始为空
    result1 = []  # 定义一个空数组作为编码输出

    for c in string:  # c为后一个字符，如果c在字符串中执行循环，执行完一次后c指向下一个字符
        pc = p + c  # 将前后两个字符组成一个新的字符用pc表示
        if pc in dictionary:  # 如果pc在字典中，把pc作为前一个字符
            p = pc
        else:
            result1.append(dictionary[p])  # 如果pc不在字典中，把前一个字符编码输出
            dictionary[pc] = last  # 把pc编码并存入字典
            last += 1
            p = c  # P指向下一个字符

    if p != '':  # 处理最后一个字符
        result1.append(dictionary[p])
    x2 = len(result1)  # 计算编码长度
    print(dictionary)
    print('压缩后的编码为：', result1)  # 输出编码

    # 译码
    dictionary2 = {i: chr(i) for i in range(0, 256)}  # 反向导入ASC码入字典2
    last2 = 256

    result2 = []
    p = result1.pop(0)  # 把编码1给p，并从输出数组中删除
    result2.append(dictionary2[p])  # 把编码1译出的字符存入译码数组中

    for c in result1:  # 因为编码1删除了，所以c从第二个编码开始
        if c in dictionary2:
            entry = dictionary2[c]
        result2.append(entry)  # 将编码译出的字符存入译码数组中
        dictionary2[last2] = dictionary2[p] + entry[0]  # 将前后两个码译出的字符组成新的字符存入字典2中
        last2 += 1
        p = c

    result2 = ''.join(result2)  # 将译码结果输出为字符串形式
    # print('译码结果为：', result2)
