# -*- coding: utf-8 -*-

import os
import re
import time

"""对文件夹中cs文件重命名py"""


def ReFileNamePy(dirPath, pattern):
    """
    :param dirPath: 文件夹路径
    :param pattern: 正则匹配模式
    :return:
    """
    # 对目录下的文件进行遍历
    for file in os.listdir(dirPath):
        # 判断是否是文件
        if os.path.isfile(os.path.join(dirPath, file)) == True:
            # 用正则匹配，去掉不需要的词
            newName = re.sub(pattern, "py", file)
            # 设置新文件名
            newFilename = file.replace(file, newName)
            # 重命名
            os.rename(os.path.join(dirPath, file), os.path.join(dirPath, newFilename))
    # print("文件名已统一修改成功")


#判断文件夹
def listdir2(path, pic_list):  # 传入存储的list

    for file in os.listdir(path):
        full_file_path = os.path.join(path, file)

        if os.path.isdir(full_file_path):
            listdir2(full_file_path, pic_list)

        if not os.path.isdir(full_file_path):
            pic_list.append(path)
    # print(type(pic_list))
    # print(path)
    # print(pic_list)
    return pic_list

#重写文件
def ReWriteFile(dirPath):
    for file in os.listdir(dirPath):
        # print(type(file))
        if os.path.isfile(os.path.join(dirPath, file)) == True:

            filename = os.path.join(dirPath, file)
            if os.path.splitext(filename)[-1] == '.py':
                fpath1 = os.path.join(dirPath, file)
                fpath2 = os.path.join(dirPath, f'{file}.xml')
                # print(fpath1)
                # print(fpath2)
                with open(fpath1, 'r', encoding='UTF-8') as f:
                    # readlines()方法，读取文件中所有行，每一行作为一个字符串存入在列表中，并且换行符用\n来表示。
                    # 这样我们得到了一个字符串列表，字符串列表中的每个元素代表一行内容
                    aaa_content = f.readlines()
                    # 以列表的形式打印aaa.txt中的内容
                    # print('aaa.txt中的内容为：{}'.format(aaa_content))
                    # 以追加的形式打开文件fpath2
                    with open(fpath2, 'w+', encoding='UTF-8') as f1:
                    # with open(fpath2, 'a+') as f1:
                        # 循环遍历aaa.txt中每一行的内容，写入文件遇到\n时自动换行
                        for i in aaa_content:
                            f1.write(i)
#删除py结尾
def FindFileNamePy(dirPath):
    for file in os.listdir(dirPath):
        # print(type(file))
        if os.path.isfile(os.path.join(dirPath, file)) == True:
            filename = os.path.join(dirPath, file)
            # print(filename)
            if os.path.splitext(filename)[-1] == '.py':
                os.remove(filename)
            # print(os.path.splitext(filename))

def ReFileNameCs(dirPath, pattern):
    """
    :param dirPath: 文件夹路径
    :param pattern: 正则匹配模式
    :return:
    """
    # 对目录下的文件进行遍历
    for file in os.listdir(dirPath):
        # 判断是否是文件
        if os.path.isfile(os.path.join(dirPath, file)) == True:
            # 用正则匹配，去掉不需要的词
            newName = re.sub(pattern, ".cs", file)
            # 设置新文件名
            newFilename = file.replace(file, newName)
            # 重命名
            os.rename(os.path.join(dirPath, file), os.path.join(dirPath, newFilename))
    # print("文件转换成功")

if __name__ == '__main__':
    pic_list = []
    timeStart = time.time()
    # path = r"D:\code\cool\dir"

    path = input("输入你需要转换的文件初始目录：")
    list2 = listdir2(path, pic_list)
    print("===等待准备转换，请稍等====")
    for i in range(len(list2)):
        # print(list2[i])
        pattern = re.compile(r'cs$')
        # print(pattern)
        ReFileNamePy(list2[i], pattern)
    time.sleep(4)
    for j in range(len(list2)):
        ReWriteFile(list2[j])
    time.sleep(4)
    for k in range(len(list2)):
        FindFileNamePy(list2[k])
    time.sleep(4)
    for l in range(len(list2)):
        # print(list2[i])
        pattern = re.compile(r'.py.xml$')
        # print(pattern)
        ReFileNameCs(list2[l], pattern)
    timeEnd = time.time()
    print("程序走了%d秒" % (timeEnd - timeStart))
    input("按任意键退出")
