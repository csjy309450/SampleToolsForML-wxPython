#!usr/bin/python2.7
# -*- coding=utf-8 -*-

import os
import os.path
import numpy as np
import cv2
import DocManager

def ImageCropping(dirPath, sampleDirName, subRect):
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

def main():
    dirPath = "/media/yangzheng/资料/专业学习资料/图形图像技术/机器学习/TrainingDataSet/dataset/CBCL/pedestrians128x64"
    sampleDirName = 'Sample-6'
    subRect = (12, 116, 6, 58)
    newShape = (16, 32)
    # ImageCropping(dirPath, sampleDirName, subRect)
    # ImageReshaping(os.path.join(dirPath, sampleDirName), sampleDirName+'16x32', newShape)

    DM = DocManager.DocManager()
    dirPath = [os.path.join(os.path.join(dirPath, sampleDirName), sampleDirName+'16x32')]
    DM.DirectoriesMerge(dirPath, "/home/yangzheng/testData/ucsd/body1", [".jpg"], _startNum=468)

if __name__ == "__main__":
    main()