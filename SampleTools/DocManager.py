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
        文件夹搜索
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
        文件夹搜索
        :param dirPath: 文件夹路径
        :param nRetract: 文件缩进级别，用于判断文件的父目录
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

    def DirectoriesMerge(self, srcPaths, tarPath, newFilter=None, _startNum=0):
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
                    os.rename(os.path.join(tarPath, t_file), os.path.join(tarPath, 't_' + str(startNum) + os.path.splitext(t_file)[1]))
                    startNum += 1

def main():
    docman = DocManager("/home/yangzheng/testData/ucsd/vidf1_33_000.y/sample", ['.jpg'])
    # docman.GetDocList()
    # print repr(docman)
    mergeDirs = [
        "/home/yangzheng/testData/ucsd/vidf1_33_000.y/sample",
        "/home/yangzheng/testData/ucsd/vidf1_33_001.y/sample",
        "/home/yangzheng/testData/ucsd/vidf1_33_002.y/sample",
        "/home/yangzheng/testData/ucsd/vidf1_33_003.y/sample",
        "/home/yangzheng/testData/ucsd/vidf1_33_004.y/sample",
        "/home/yangzheng/testData/ucsd/vidf1_33_005.y/sample",
        "/home/yangzheng/testData/ucsd/vidf1_33_006.y/sample",
        "/home/yangzheng/testData/ucsd/vidf1_33_007.y/sample",
        "/home/yangzheng/testData/ucsd/vidf1_33_008.y/sample",
        "/home/yangzheng/testData/ucsd/vidf1_33_009.y/sample",
        "/home/yangzheng/testData/ucsd/vidf1_33_010.y/sample",
        "/home/yangzheng/testData/ucsd/vidf1_33_011.y/sample",
        "/home/yangzheng/testData/ucsd/vidf1_33_012.y/sample",
        "/home/yangzheng/testData/ucsd/vidf1_33_013.y/sample",
        "/home/yangzheng/testData/ucsd/vidf1_33_014.y/sample",
        "/home/yangzheng/testData/ucsd/vidf1_33_015.y/sample",
        "/home/yangzheng/testData/ucsd/vidf1_33_016.y/sample",
        "/home/yangzheng/testData/ucsd/vidf1_33_017.y/sample",
        "/home/yangzheng/testData/ucsd/vidf1_33_018.y/sample",
        "/home/yangzheng/testData/ucsd/vidf1_33_019.y/sample",
        "/home/yangzheng/testData/ucsd/vidf1_33_020.y/sample"
    ]
    docman.DirectoriesMerge(mergeDirs, "/home/yangzheng/testData/ucsd/body")

if __name__ == "__main__":
    main()

