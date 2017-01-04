#!usr/bin/python2.7
# -*- coding=utf-8 -*-

import os
import os.path
import numpy as np
import cv2
import DocManager

def ImageCropping(dirPath, sampleDirName, subRect):
    """
    剪裁样本
    :param dirPath:
    :param sampleDirName:
    :param subRect:
    :return:
    """
    sampleDir = os.path.join(dirPath, sampleDirName)
    SequenceNum = 0
    os.makedirs(sampleDir)
    DM = DocManager.DocManager()
    DM.ResetFilter(['.ppm'])
    DM.GetDirTree(dirPath)

    # t_imgPath = DM.docList[0]
    # t_img = cv2.imread(os.path.join(dirPath, t_imgPath))
    # tar_img = np.copy(t_img[4:124, 2:62])
    # cv2.imwrite(os.path.join(sampleDir, str(SequenceNum)+'.jpg'), tar_img)
    # cv2.imshow("show", tar_img)
    # cv2.waitKey(0)
    # print DM.docList

    for t_imgPath in DM.docList:
        t_img = cv2.imread(os.path.join(dirPath, t_imgPath))
        tar_img = np.copy(t_img[subRect[0]:subRect[1], subRect[2]:subRect[3]])
        cv2.imwrite(os.path.join(sampleDir, str(SequenceNum) + '.jpg'), tar_img)
        SequenceNum += 1

def ImageReshaping(dirPath, sampleDirName, newShape):
    """
    调整样本尺度
    :param dirPath: 原样本集路径
    :param sampleDirName: 调整尺度后存放文件夹名（存放在原样本集目录下）
    :param newShape:
    :return:
    """
    sampleDir = os.path.join(dirPath, sampleDirName)
    SequenceNum = 0
    os.makedirs(sampleDir)
    DM = DocManager.DocManager()
    DM.ResetFilter(['.jpg'])
    DM.GetDirTree(dirPath)

    # t_imgPath = DM.docList[0]
    # t_img = cv2.imread(os.path.join(dirPath, t_imgPath))
    # tar_img = np.copy(t_img[4:124, 2:62])
    # cv2.imwrite(os.path.join(sampleDir, str(SequenceNum)+'.jpg'), tar_img)
    # cv2.imshow("show", tar_img)
    # cv2.waitKey(0)
    # print DM.docList

    for t_imgPath in DM.docList:
        t_img = cv2.imread(os.path.join(dirPath, t_imgPath))
        tar_img = cv2.resize(t_img, newShape)
        cv2.imwrite(os.path.join(sampleDir, str(SequenceNum) + '.jpg'), tar_img)
        SequenceNum += 1

def MakeSamplesText(dirPath, txtName, _labelFlag):
    """
    将样本集用txt文档描述，格式为
        /PATH/cat0.jpg 0
        /PATH/cat1.jpg 0
        ...
        /PATH/dog0.jpg 1
        /PATH/dog1.jpg 1
        ...
        /PATH/pig0.jpg n
        /PATH/pig1.jpg n
        ...
    :param dirPath:
    :param txtName:
    :param _labelFlag: 标签规则((标签号, 个数),(...),...)
    :return:
    """
    DM = DocManager.DocManager()
    DM.ResetFilter(['.jpg'])
    DM.GetDirTree(dirPath)
    DM.docList.sort()

    f = open(os.path.join(dirPath, txtName), 'w')
    indx = 0
    kind = 0
    print len(DM.docList)
    while indx < len(DM.docList):
        # t_str = os.path.join(dirPath, DM.docList[indx]) + ' ' + str(_labelFlag[kind][0]) + '\n'
        t_str = DM.docList[indx] + ' ' + str(_labelFlag[kind][0]) + '\n'
        f.write(t_str)
        if indx+1 == _labelFlag[kind][1]:
            kind+=1
        indx+=1


def main():
    dirPath = "/home/yangzheng/testData/BodyDataset/body_28x28/validation"
    sampleDirName = 'Sample-28x28'
    subRect = (12, 116, 6, 58)
    newShape = (28, 28)
    # ImageCropping(dirPath, sampleDirName, subRect)
    # ImageReshaping(dirPath, sampleDirName, newShape)

    # DM = DocManager.DocManager([".jpg"])
    # dirPaths = [
    #     '/home/yangzheng/testData/BodyDataset/body_28x28/validation',
    #     '/home/yangzheng/testData/BodyDataset/notBody-28x28/validation',
    # ]
    # DM.DirectoriesMerge(dirPaths, "/home/yangzheng/testData/BodyDataset/validation", [".jpg"])
    # DM.GetDirTree("/home/yangzheng/testData/BodyDataset/training")
    # DM.docList.sort()
    MakeSamplesText("/home/yangzheng/testData/BodyDataset/train", 'train.txt', ((0, 1201), (1, 2402)))
    MakeSamplesText("/home/yangzheng/testData/BodyDataset/validation", 'validation.txt', ((0, 191), (1, 382)))
    pass

    # MakeSamplesText(dirPath, 'body_train.txt', '0')

if __name__ == "__main__":
    main()
