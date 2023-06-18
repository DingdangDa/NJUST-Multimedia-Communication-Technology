# 文件：南京理工大学多媒体通信技术课设，haffman编码模块
# 作者：黄炫宇 xuanyuhuang2001@gmail.com
# 说明：haffman编码

# codeDic = {}
#
#
# # 树节点类构建
# class TreeNode(object):
#     def __init__(self, data):
#         self.val = data[0]
#         self.priority = data[1]
#         self.leftChild = None
#         self.rightChild = None
#         self.code = ""
#
#
# # 创建树节点队列函数
# def creatnodeQ(codes):
#     q = []
#     for code in codes:
#         q.append(TreeNode(code))
#     # print("q:", q)
#     return q
#
#
# # 为队列添加节点元素，并保证优先度从大到小排列
# def addQ(queue, nodeNew):
#     if len(queue) == 0:
#         return [nodeNew]
#     for i in range(len(queue)):
#         if queue[i].priority >= nodeNew.priority:
#             return queue[:i] + [nodeNew] + queue[i:]
#     return queue + [nodeNew]
#
#
# # 节点队列类定义
# class nodeQeuen(object):
#     def __init__(self, code):
#         self.que = creatnodeQ(code)
#         self.size = len(self.que)
#
#     def addNode(self, node):
#         self.que = addQ(self.que, node)
#         self.size += 1
#
#     def popNode(self):
#         self.size -= 1
#         return self.que.pop(0)


# 各个字符在字符串中出现的次数，即计算优先度
def freChar(string):
    d = {}
    for c in string:
        if not c in d:
            d[c] = 1
        else:
            d[c] += 1
    return sorted(d.items(), key=lambda x: x[1])


# 创建哈夫曼树
# def creatHuffmanTree(nodeQ):
#     while nodeQ.size != 1:
#         node1 = nodeQ.popNode()
#         node2 = nodeQ.popNode()
#         r = TreeNode([None, node1.priority + node2.priority])
#         r.leftChild = node1
#         r.rightChild = node2
#         nodeQ.addNode(r)
#     return nodeQ.popNode()
#
#
# # 由哈夫曼树得到哈夫曼编码表
# def HuffmanCodeDic(head, x):
#     global codeDic, codeList
#     if head:
#         HuffmanCodeDic(head.leftChild, x + '0')
#         head.code += x
#         if head.val:
#             codeDic[head.val] = head.code
#         HuffmanCodeDic(head.rightChild, x + '1')
#
#
# # 字符串编码
# def TransEncode(string):
#     global codeDic
#     transcode = ""
#     for c in string:
#         transcode += codeDic[c]
#     return transcode



# 节点类
class Node(object):
    def __init__(self, name=None, value=None):
        self._name = name
        self._value = value
        self._left = None
        self._right = None


# 哈夫曼树类
class HuffmanTree(object):
    # 根据Huffman树的思想：以叶子节点为基础，反向建立Huffman树
    def __init__(self, char_weights):
        self.a = [Node(part[0], part[1]) for part in char_weights]  # 根据输入的字符及其频数生成叶子节点
        while len(self.a) != 1:
            self.a.sort(key=lambda node: node._value, reverse=True)
            c = Node(value=(self.a[-1]._value + self.a[-2]._value))
            c._left = self.a.pop(-1)
            c._right = self.a.pop(-1)
            self.a.append(c)
        self.root = self.a[0]
        self.b = list(range(10))  # self.b用于保存每个叶子节点的Haffuman编码,range的值只需要不小于树的深度就行

    # 用递归的思想生成编码
    def pre(self, tree, length):
        node = tree
        if (not node):
            return
        elif node._name:
            x = str(node._name) + '的编码为:'
            for i in range(length):
                x += str(self.b[i])
            print(x)
            return
        self.b[length] = 0
        self.pre(node._left, length + 1)
        self.b[length] = 1
        self.pre(node._right, length + 1)

    # 生成哈夫曼编码
    def get_code(self):
        self.pre(self.root, 0)
