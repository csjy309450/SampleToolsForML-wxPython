#!usr/bin/python2.7
# -*- coding=utf-8 -*-

import os
import os.path

class DocManager:
    """
    @functions: manage and search the documents
    """
    def __init__(self, _docFilter=['.doc', '.py']):
        """
        :param docFilter: interesting documents' extension name
        """
        self.docList = []
        self.docFilter = _docFilter
        # self.GetDocList()

    def ResetFilter(self, newFilter):
        self.docFilter = newFilter

    def AddFilter(self, afilter):
        self.docFilter.append(afilter)

    def isFIleInFilter(self, filePath):
        """
        :判断是否是感兴趣文件
        :param filePath: 文件绝对路径
        :return:
        """
        fileType = os.path.splitext(filePath)
        if fileType[1] in self.docFilter:
            return True
        else:
            return False

    def __dirSearch(self, dirPath, nRetract=0):
        """
        文件夹遍历
        :param dirPath: 文件夹路径
        :param nRetract: 文件缩进级别，用于判断文件的父目录
        :return:
        """
        dirlist = os.listdir(dirPath)
        if len(dirlist) <= 0:
            return False
        dirName = os.path.split(dirPath)
        self.docList.append([dirName[1], nRetract, 0])
        dirHaveRightDoc = False
        for t_file in dirlist:
            # print os.path.join(dirPath, t_file)
            if not os.path.isdir(os.path.join(dirPath, t_file)):
                if self.isFIleInFilter(t_file):
                    self.docList.append([t_file, nRetract+1, 1])
                    dirHaveRightDoc = dirHaveRightDoc or True
            else:
                a = self.__dirSearch(os.path.join(dirPath, t_file), nRetract=nRetract+1)
                dirHaveRightDoc = dirHaveRightDoc or a
        if not dirHaveRightDoc:
            del self.docList[-1]
        return dirHaveRightDoc

    def __dirSearch2(self, dirPath, deep=0):
        """
        根据深度deep搜索文件夹文件
        :param dirPath: 文件夹路径
        :param deep: 文件夹搜索深度
        :return:
        """
        dirHaveRightDoc = False
        if deep<0:
            return dirHaveRightDoc
        dirlist = os.listdir(dirPath)
        if len(dirlist) <= 0:
            return False
        # dirName = os.path.split(dirPath)
        # self.docList.append([dirName[1], nRetract, 0])
        for t_file in dirlist:
            # print os.path.join(dirPath, t_file)
            if not os.path.isdir(os.path.join(dirPath, t_file)):
                if self.isFIleInFilter(t_file):
                    splitFileName = os.path.splitext(t_file)
                    self.docList.append(t_file)
                    dirHaveRightDoc = dirHaveRightDoc or True
            else:
                a = self.__dirSearch2(os.path.join(dirPath, t_file), deep=deep-1)
                dirHaveRightDoc = dirHaveRightDoc or a
        if not dirHaveRightDoc:
            del self.docList[-1]
        return dirHaveRightDoc

    def GetDirTree(self, dirPath):
        self.__dirSearch2(dirPath)

    def __repr__(self):
        """
        打印目录
        :return: 目录的文本
        """
        reprStr = ''
        for t_file in self.docList:
            if t_file[2] == 0:#文件夹
                reprStr += '|' * (t_file[1]) + '>' + t_file[0] + '\n'
            else:
                reprStr += '|' * (t_file[1]) + t_file[0] + '\n'
        return reprStr

    def IntToSeqNum(self, _int, _order):
        """
        将数字序号转化成字符系列，且保持字符序列长度相同（不够的补零）
        :param _int[int] 数字序列
        :param _order[int] 规定字符序列的长度
        :return[string]
        """
        order = 1
        strNum = str(_int)
        while order <= _order:
            if _int < pow(10, order):
                strNum = (_order-order)*'0' + str(_int)
                break
            order+=1

        return strNum
        # if _int < 10:
        #     strNum = '000' + str(_int)
        # elif _int < 100:
        #     strNum = '00' + str(_int)
        # elif _int < 1000:
        #     strNum = '0' + str(_int)
        # else:
        #     strNum = '0' + str(_int)

    def DirectoriesMerge(self, srcPaths, tarPath, newFilter=None, _startNum=0, _order=5):
        """
        合并多文件中的文件到指定文件夹下
        :param srcPaths:
        :param tarPath:
        :param newFilter:
        :param _startNum: 指定文件名的起始序列
        :param _order: 指定文件名数字序列的长度
        :return:
        """
        import shutil
        if newFilter != None:
            self.docFilter = newFilter
        startNum = _startNum
        for srcPath in srcPaths:
            print srcPath
            if os.path.isdir(srcPath):
                self.docList = []
                self.__dirSearch2(srcPath)
                for t_file in self.docList:
                    # print t_file
                    # shutil.copy()
                    t_filePath = os.path.join(srcPath, t_file)
                    shutil.copy(t_filePath, tarPath)
                    strNum = self.IntToSeqNum(startNum, _order)
                    os.rename(os.path.join(tarPath, t_file), os.path.join(tarPath, strNum + '_t' + os.path.splitext(t_file)[1]))
                    startNum += 1


def main():
    DM = DocManager(['.jpg'])
    # DM.GetDirTree('/home/yangzheng/testData/BodyDataset/training')
    # DM.docList.sort(cmp=lambda x, y: cmp(x, y))
    print DM.IntToSeqNum(11, 6)
    pass

if __name__ == "__main__":
    main()

