#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@Function:绘图
@Input：NONE
@Output: NONE
@author: YangZheng
@date:2016-12-15
'''

import wx
import os


class PaintFrame(wx.Frame):
    def __init__(self, parent=None, id=-1, pos=wx.DefaultPosition, title="Painter tool"):
        wx.Frame.__init__(self, parent, id, title, pos, size=(800, 800))
        self.SetBackgroundColour(wx.GREEN)
        self.color = "White"
        self.thickness = 10

        # 创建一个画笔
        self.pen = wx.Pen(self.color, self.thickness, wx.SOLID)
        self.lines = []
        self.curLine = []
        self.pos = (0, 0)
        self.InitBuffer()
        self.InitUI()

        # 连接事件
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_IDLE, self.OnIdle)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_MENU, self.On_Menu_Open, self.menuItemOpen)
        self.Bind(wx.EVT_MENU, self.On_Menu_Save, self.menuItemSave)


    def InitUI(self):
        # 添加菜单栏
        menubar = wx.MenuBar()
        menuFile = wx.Menu()
        self.menuItemOpen = menuFile.Append(-1, '&Open')
        self.menuItemSave = menuFile.Append(-1, "&Save")
        menubar.Append(menuFile, "&File")
        self.SetMenuBar(menubar)

    def InitBuffer(self):
        self.size = size = self.GetClientSize()
        # 创建缓存的设备上下文
        self.buffer = wx.EmptyBitmap(size.width, size.height)
        dc = wx.BufferedDC(None, self.buffer)
        # 使用设备上下文
        dc.SetBackground(wx.Brush(wx.BLACK))
        dc.Clear()
        self.refreshBuffer = False

    def GetLinesData(self):
        return self.lines[:]

    def SetLinesData(self, lines):
        self.lines = lines[:]
        self.InitBuffer()
        self.Refresh()

    def On_Menu_Open(self, event):
        dlg = wx.FileDialog(self, defaultDir="./", style=wx.DEFAULT_DIALOG_STYLE|wx.FD_MULTIPLE|wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.ImgPaths = dlg.GetPaths()
            # print self.ImgPaths
            dlg.Close()
            # print self.ImgPaths
        else:
            return
        if len(self.ImgPaths) <= 0:
            pass
        else:
            img = wx.Image(self.ImgPaths[0], wx.BITMAP_TYPE_ANY)
            if self.size.width<img.Width:
                self.size.width = img.Width
            if self.size.height<img.Height:
                self.size.height = img.Height
            del self.buffer
            self.buffer = wx.EmptyBitmap(self.size.width, self.size.height)
            self.buffer = img.ConvertToBitmap()
            self.refreshBuffer = True

            # 重新调整尺度
            # self.Bmp = self.image.ConvertToBitmap()
            # self.image.Rescale(200, 200)

    def On_Menu_Save(self, event):
        dlg = wx.FileDialog(self, style=wx.FD_CHANGE_DIR|wx.FD_SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            self.SamplePath = dlg.GetPaths()
            print self.SamplePath
            dlg.Close()
        else:
            return
        if len(self.SamplePath) > 0:
            img = self.buffer.ConvertToImage()
            img.SaveFile(self.SamplePath[0], wx.BITMAP_TYPE_JPEG )


    def OnLeftDown(self, event):
        self.curLine = []

        # 获取鼠标位置
        self.pos = event.GetPositionTuple()
        self.CaptureMouse()

    def OnLeftUp(self, event):
        if self.HasCapture():
            self.lines.append((self.color,
                               self.thickness,
                               self.curLine))
            self.curLine = []
            self.ReleaseMouse()

    def OnMotion(self, event):
        if event.Dragging() and event.LeftIsDown():#判断是否处于拖拽状态和鼠标左键按下状态
            dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
            self.drawMotion(dc, event)
            event.Skip()
        """
	    event.skip()的作用是告诉MainLoop继续处理这个消息，而不是在当前handler处理完了就中断了，
	    这是为了保证一个动作中触发的多个同类事件均受到处理而不遗漏
	    """

    def drawMotion(self, dc, event):
        dc.SetPen(self.pen)
        newPos = event.GetPositionTuple()
        coords = self.pos + newPos
        self.curLine.append(coords)
        dc.DrawLine(*coords)
        self.pos = newPos

    def OnSize(self, event):
        size = self.GetClientSize()
        # 创建缓存的设备上下文,重新调整绘图缓冲区的大小
        if self.size.width < size.width:
            self.size.width = size.width
        if self.size.height < size.height:
            self.size.height = size.height
        tmpImg = self.buffer #保存原来的图像
        self.buffer = wx.EmptyBitmap(self.size.width, self.size.height)#申请新大小的绘图缓冲区
        dc = wx.BufferedDC(None, self.buffer)
        # 使用设备上下文重绘制，注：需要重新绘制背景，新申请的绘图缓冲区里面有意想不到的数据残留
        dc.SetBackground(wx.Brush(wx.BLACK))
        dc.Clear()
        dc.DrawBitmap(tmpImg, 0, 0)
        self.refreshBuffer = True

    def OnIdle(self, event):#系统定时send的事件，可用于定时自动刷新一次窗口
        if self.refreshBuffer:
            self.refreshBuffer = False
            self.Refresh(False)

    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self, self.buffer)#派生自wx.BufferedDC.可采用双缓冲绘图以避免刷新时的闪烁，一般在EVT_PAINT响应函数中调用

    def DrawLines(self, dc):
        for colour, thickness, line in self.lines:
            pen = wx.Pen(colour, thickness, wx.SOLID)
            dc.SetPen(pen)
            for coords in line:
                dc.DrawLine(*coords)

    def SetColor(self, color):
        self.color = color
        self.pen = wx.Pen(self.color, self.thickness, wx.SOLID)

    def SetThickness(self, num):
        self.thickness = num
        self.pen = wx.Pen(self.color, self.thickness, wx.SOLID)


if __name__ == '__main__':
    app = wx.App()
    frame = PaintFrame(None)
    frame.Show(True)
    app.MainLoop()
