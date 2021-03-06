#!/usr/bin/python
# -*-<coding=UTF-8>-*-

"""Hello,wxPython! program."""

import wx
import os.path


class Frame(wx.Frame):
    """
    创建一个wx.Frame的子类
    """

    def __init__(self, parent=None, id=-1, pos=wx.DefaultPosition, title="sample tool"):
        """
        __init__中哪些参数是必须的,每次这么多参数,谁能记得住.
        不过,参数没有顺序要求.想想,创建一个frame需要哪些东西,无非就是位置,大小,标题,ID之类的内容.
        """

        wx.Frame.__init__(self, parent, id, title, pos, size=(400, 400))

        self.InitUI()
        self.InitDrawTools()

        self.PositiveSampleRect = [[None, None]]
        self.NegativeSampleRect = [[None, None]]
        self.CurrentBmpPosition = [0, 0]

        # 绑定鼠标在图片上的操作事件响应函数
        self.ImgWin.Bind(wx.EVT_LEFT_DOWN, self.On_Mouse_Left_Down)
        # self.ImgWin.Bind(wx.EVT_MOTION, self.On_Mouse_Move)
        self.ImgWin.Bind(wx.EVT_LEFT_UP, self.On_Mouse_Left_Up)
        self.ImgWin.Bind(wx.EVT_RIGHT_DOWN, self.On_Mouse_Right_Down)
        self.ImgWin.Bind(wx.EVT_RIGHT_UP, self.On_Mouse_Right_Up)
        #self.scroller.Bind(wx.EVT_PAINT, self.OnPaint)
        self.scroller.Bind(wx.EVT_SCROLLWIN_THUMBTRACK, self.On_ScrollBar_Down)
        self.Bind(wx.EVT_MENU, self.On_Menu_Open, self.menuItemOpen)
        self.Bind(wx.EVT_MENU, self.On_Menu_Save, self.menuItemSave)
        self.Bind(wx.EVT_MENU, self.On_Menu_Next, self.menuItemNext)

    """
    初始化窗口中的GUI
    """
    def InitUI(self):
        # 添加滑动栏，主要解决显示大图的问题
        self.scroller = wx.ScrolledWindow(self, -1)

        #添加菜单栏
        menubar = wx.MenuBar()
        menuFile = wx.Menu()
        self.menuItemOpen = menuFile.Append(-1, "&Open")
        self.menuItemSave = menuFile.Append(-1, "&Save")
        self.menuItemNext = menuFile.Append(-1, "&Next")
        menubar.Append(menuFile, "&File")
        self.SetMenuBar(menubar)

        #静态位图panel
        self.ImgWin = wx.StaticBitmap(parent=self.scroller)


    """
    初始化画笔工具
    """
    def InitDrawTools(self):
        # 初始化画笔
        self.Pen = wx.Pen("green", 2, wx.SOLID)
        self.Brush = wx.Brush('green', wx.TRANSPARENT)  # 透明填充

    """
    重新获取设备上下文缓冲区（绘图缓冲区）
    """
    def ResetBufferDC(self, color='red'):
        # 以图片作为设备双下文缓冲区，意思就是要直接在图像上作画的意思，BufferedDC的第一个参数估计是缓冲区的输出，第二个参数则是输入
        self.dc = wx.BufferedDC(None, self.Bmp)
        if color == 'red':
            self.Pen.SetColour('red')
            self.Brush.SetColour('red')
            self.dc.SetPen(self.Pen)
            self.dc.SetBrush(self.Brush)
        elif color == 'green':
            self.Pen.SetColour('green')
            self.Brush.SetColour('green')
            self.dc.SetPen(self.Pen)
            self.dc.SetBrush(self.Brush)
        # self.dc.DrawLine(0,0,50,50)

    # def OnPaint(self, event):
    #     self.dc = wx.BufferedDC(wx.ClientDC(self.scroller), self.Bmp)  # 处理一个paint（描绘）请求
    #     #self.scroller.Refresh()

    def On_ScrollBar_Down(self, event):
        print ('bottom:' if event.Orientation == 4 else 'right:'), event.Position
        if event.Orientation == 4:
            self.CurrentBmpPosition[0] = event.Position
        else:
            self.CurrentBmpPosition[1] = event.Position

    """
    鼠标点击事件响应函数
    """
    def On_Mouse_Left_Down(self, event):
        # print event.Position
        #self.startPoint = event.Position
        if self.PositiveSampleRect[len(self.PositiveSampleRect)-1][1] == None:
            del self.PositiveSampleRect[len(self.PositiveSampleRect)-1]
        self.PositiveSampleRect.append([event.Position, None])

    def On_Mouse_Left_Up(self, event):
        # print event.Position
        # self.endPoint = event.Position
        self.PositiveSampleRect[len(self.PositiveSampleRect)-1][1] = event.Position

        #初始化设备上下文
        self.ResetBufferDC(color='green')

        startPoint = self.PositiveSampleRect[len(self.PositiveSampleRect)-1][0]
        endPoint = self.PositiveSampleRect[len(self.PositiveSampleRect)-1][1]

        self.dc.DrawRectangle(startPoint[0] + self.CurrentBmpPosition[0], startPoint[1] + self.CurrentBmpPosition[1], endPoint[0] - startPoint[0], endPoint[1] - startPoint[1])

        self.ImgWin.SetBitmap(self.Bmp)

    def On_Mouse_Right_Down(self, event):
        if self.NegativeSampleRect[len(self.NegativeSampleRect) - 1][1] == None:
            del self.NegativeSampleRect[len(self.NegativeSampleRect) - 1]
        self.NegativeSampleRect.append([event.Position, None])

    def On_Mouse_Right_Up(self, event):
        self.NegativeSampleRect[len(self.NegativeSampleRect) - 1][1] = event.Position

        # 初始化设备上下文
        self.ResetBufferDC(color='red')

        startPoint = self.NegativeSampleRect[len(self.NegativeSampleRect) - 1][0]
        endPoint = self.NegativeSampleRect[len(self.NegativeSampleRect) - 1][1]

        self.dc.DrawRectangle(startPoint[0] + self.CurrentBmpPosition[0], startPoint[1] + self.CurrentBmpPosition[1],
                              endPoint[0] - startPoint[0], endPoint[1] - startPoint[1])

        self.ImgWin.SetBitmap(self.Bmp)

    def On_Mouse_Move(self, event):
        pass

    """
    菜单Open选项的响应函数，加载要进行采样的图片
    """
    def On_Menu_Open(self, event):
        dlg = wx.FileDialog(self, style=wx.DEFAULT_DIALOG_STYLE|wx.FD_MULTIPLE|wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.ImgPaths = dlg.GetPaths()
            dlg.Close()
            # print self.ImgPaths
        if len(self.ImgPaths) <= 0:
            pass
        else:
            try:
                del self.Bmp
            except AttributeError, err:
                print "There have no Bitmap file currently!"
            self.currentBmpPath = self.ImgPaths.pop()
            self.Bmp = wx.Image(self.currentBmpPath, wx.BITMAP_TYPE_ANY).ConvertToBitmap()

            # 获取图片大小,同时作为Frame的大小
            self.BmpSize = size = self.Bmp.GetWidth(), self.Bmp.GetHeight()

            # 创建静态位图窗口
            self.ImgWin.SetBitmap(self.Bmp)
            # 设置窗口的最大大小
            self.SetMaxSize([size[0], size[1] + 21])
            #设置滑动条尺寸
            self.scroller.SetScrollbars(1, 1, size[0], size[1])

    def On_Menu_Next(self, event):
        if len(self.ImgPaths) <= 0:
            print "Have no next bitmap file!"
        else:
            try:
                del self.Bmp
            except AttributeError, err:
                print "There have no Bitmap file currently!"
            self.currentBmpPath = self.ImgPaths.pop()
            self.Bmp = wx.Image(self.currentBmpPath, wx.BITMAP_TYPE_ANY).ConvertToBitmap()

            # 获取图片大小,同时作为Frame的大小
            self.BmpSize = size = self.Bmp.GetWidth(), self.Bmp.GetHeight()

            # 创建静态位图窗口
            self.ImgWin.SetBitmap(self.Bmp)
            # 设置窗口的最大大小
            self.SetMaxSize([size[0], size[1] + 21])
            # 设置滑动条尺寸
            self.scroller.SetScrollbars(1, 1, size[0], size[1])

    def On_Menu_Save(self, event):
        splitPath = os.path.splitext(self.currentBmpPath)
        tempFile = file(splitPath[0]+'.txt', 'w')
        tempFile.write(repr(self.PositiveSampleRect))


class App(wx.App):
    def OnInit(self):

        self.frame = Frame()

        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True


def main():
    app = App()
    app.MainLoop()


if __name__ == "__main__":
    main()