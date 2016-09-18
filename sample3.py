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

        # # 绑定鼠标在图片上的操作事件响应函数
        # self.ImgWin.Bind(wx.EVT_LEFT_DOWN, self.On_Mouse_Left_Down)
        # # self.ImgWin.Bind(wx.EVT_MOTION, self.On_Mouse_Move)
        # self.ImgWin.Bind(wx.EVT_LEFT_UP, self.On_Mouse_Left_Up)
        # self.ImgWin.Bind(wx.EVT_RIGHT_DOWN, self.On_Mouse_Right_Down)
        # self.ImgWin.Bind(wx.EVT_RIGHT_UP, self.On_Mouse_Right_Up)
        #self.scroller.Bind(wx.EVT_PAINT, self.OnPaint)
        self.scroller.Bind(wx.EVT_SCROLLWIN_THUMBTRACK, self.On_ScrollBar_Down)
        self.Bind(wx.EVT_MENU, self.On_Menu_Open, self.menuItemOpen)
        self.Bind(wx.EVT_MENU, self.On_Menu_Save, self.menuItemSave)
        self.Bind(wx.EVT_MENU, self.On_Menu_Next, self.menuItemNext)
        self.Bind(wx.EVT_MENU, self.On_Menu_Screenshot, self.menuItemScreenshotWindow)
        self.Bind(wx.EVT_MENU, self.On_Menu_DirectDraw, self.menuItemDirectDraw)
        self.Bind(wx.EVT_SIZE, self.On_Window_Resize)
        self.slider.Bind(wx.EVT_SLIDER, self.On_Slider_Motion)


    """
    初始化窗口中的GUI
    """
    def InitUI(self):
        # 添加滑块,调整图像尺度
        self.slider = wx.Slider(self, -1, 10, 0, 20, pos=(0, 0),
                           style=wx.SL_HORIZONTAL |wx.SL_LABELS)
        self.slider.SetTickFreq(1, 1)

        # 添加滑动栏，主要解决显示大图的问题
        sliderSize = self.slider.GetClientSize()
        self.scroller = wx.ScrolledWindow(self, -1, pos=(0, sliderSize.y))

        #添加菜单栏
        menubar = wx.MenuBar()
        menuFile = wx.Menu()
        self.menuItemOpen = menuFile.Append(-1, '&Open')
        self.menuItemSave = menuFile.Append(-1, "&Save")
        self.menuItemNext = menuFile.Append(-1, "&Next")
        self.menuItemScreenshotWindow = menuFile.Append(-1, "&Screenshot Window")
        self.menuItemDirectDraw = menuFile.Append(-1, "&Direct Draw")
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

    def ResizeWindowByBmp(self):

        # 获取图片大小,同时作为Frame的大小
        self.BmpSize = size = self.Bmp.GetWidth(), self.Bmp.GetHeight()

        # 创建静态位图窗口
        self.ImgWin.SetBitmap(self.Bmp)
        # 设置窗口的最大大小
        self.SetMaxSize([size[0], size[1] + 74])
        # 设置滑动条尺寸
        self.scroller.SetScrollbars(1, 1, size[0], size[1])

    def LoadImage(self):
        self.image = wx.Image(self.currentBmpPath, wx.BITMAP_TYPE_ANY)
        self.Bmp = self.image.ConvertToBitmap()
        self.SetTitle(self.currentBmpPath)
        print self.currentBmpPath

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
        dlg = wx.FileDialog(self, defaultDir="/home/yangzheng/myDataset", style=wx.DEFAULT_DIALOG_STYLE|wx.FD_MULTIPLE|wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.ImgPaths = dlg.GetPaths()
            # print self.ImgPaths
            dlg.Close()
            # print self.ImgPaths
        if len(self.ImgPaths) <= 0:
            pass
        else:
            try:
                del self.Bmp
            except AttributeError, err:
                print "There have no Bitmap file currently!"
            self.currentBmpPath = self.ImgPaths.pop(0)
            # print self.currentBmpPath
            splitPath = os.path.split(self.currentBmpPath)
            self.BmpDirPath = os.path.join(splitPath[0], u'sample')
            if not os.path.isdir(self.BmpDirPath):
                os.makedirs(self.BmpDirPath)
                # print(self.BmpDirPath)
            self.sampleCount = len(os.listdir(self.BmpDirPath))
            # print type(self.sampleCount), self.sampleCount
            self.LoadImage()
            # 重新调整尺度
            # self.Bmp = self.image.ConvertToBitmap()
            # self.image.Rescale(200, 200)
            self.ResizeWindowByBmp()

    def On_Menu_Next(self, event):
        if len(self.ImgPaths) <= 0:
            print "Have no next bitmap file!"
        else:
            try:
                del self.Bmp
            except AttributeError, err:
                print "There have no Bitmap file currently!"
            self.currentBmpPath = self.ImgPaths.pop(0)
            self.LoadImage()
            # self.Bmp = self.image.ConvertToBitmap()
            self.ResizeWindowByBmp()

    def On_Menu_Save(self, event):
        dlg = wx.FileDialog(self, style=wx.FD_CHANGE_DIR)
        if dlg.ShowModal() == wx.ID_OK:
            self.SamplePath = dlg.GetPaths()
            print self.SamplePath
            dlg.Close()

    def On_Menu_Screenshot(self, event):
        # print repr(self)
        screenshotFrame = CopyFrame(self)
        screenshotFrame.Show()

    def On_Menu_DirectDraw(self, event):
        # 绑定鼠标在图片上的操作事件响应函数
        self.ImgWin.Bind(wx.EVT_LEFT_DOWN, self.On_Mouse_Left_Down)
        # self.ImgWin.Bind(wx.EVT_MOTION, self.On_Mouse_Move)
        self.ImgWin.Bind(wx.EVT_LEFT_UP, self.On_Mouse_Left_Up)
        self.ImgWin.Bind(wx.EVT_RIGHT_DOWN, self.On_Mouse_Right_Down)
        self.ImgWin.Bind(wx.EVT_RIGHT_UP, self.On_Mouse_Right_Up)

    def On_Window_Resize(self, event):
        winSize = self.GetClientSize()
        sliderSize = self.slider.GetClientSize()
        sliderSize.x = winSize.x
        # print repr(sliderSize)
        self.slider.SetSize(sliderSize)
        self.scroller.SetSize(wx.Size(winSize.x, winSize.y-sliderSize.y))

    def On_Slider_Motion(self, event):
        # print self.slider.GetValue()
        newScalar = self.slider.GetValue()
        size = self.image.GetSize()
        self.ScaleImag = self.image.Copy()
        self.ScaleImag.Rescale(size.x*newScalar*0.1, size.y*newScalar*0.1)
        self.Bmp = self.ScaleImag.ConvertToBitmap()
        self.ResizeWindowByBmp()

"""
用于选取样本的小窗口
"""
class CopyFrame(wx.Frame):
    def __init__(self, parent):
        self.parentWin = parent
        pos = parent.scroller.GetScreenPosition()
        # print pos
        self.frameSize = wx.Size(50, 50)
        wx.Frame.__init__(self, parent, wx.NewId(), pos=pos, size=self.frameSize,
                          style=wx.NO_BORDER | wx.STAY_ON_TOP)
        #self.SetBackgroundStyle(wx.BG_STYLE_COLOUR)
        self.SetBackgroundColour(wx.Colour(0, 0, 0, wx.ALPHA_TRANSPARENT))

        self.InitUI()

        self.MouseDown = False
        self.BGBmpWin = wx.StaticBitmap(self)

        self.BGBmpWin.Bind(wx.EVT_LEFT_DOWN, self.On_LeftMouse_Down)
        self.BGBmpWin.Bind(wx.EVT_LEFT_UP, self.On_LeftMouse_Up)
        self.BGBmpWin.Bind(wx.EVT_MOTION, self.On_Mouse_Move)
        self.BGBmpWin.Bind(wx.EVT_RIGHT_UP, self.On_RightMouse_up)
        self.Bind(wx.EVT_PAINT, self.On_Paint)
        self.Bind(wx.EVT_MENU, self.On_MenuCopy_Down, self.MenuItemCopy)
        self.Bind(wx.EVT_MENU, self.On_MenuClose_Down, self.MenuItemClose)

    def InitUI(self):
        self.popMenu = wx.Menu()
        self.MenuItemCopy = self.popMenu.Append(-1, "&Copy")
        self.MenuItemClose = self.popMenu.Append(-1, "&Close")

    def On_LeftMouse_Down(self, event):
        self.GetCapture()
        self.startPos = self.ClientToScreen(event.GetPosition())

    def On_LeftMouse_Up(self, event):
        if self.HasCapture():
            self.ReleaseMouse()

    def On_Mouse_Move(self, event):
        if event.Dragging() and event.LeftIsDown():
            endPos = wx.GetMousePosition()
            delta = endPos - self.startPos
            winPos = self.GetScreenPosition()
            # print repr(winPos)
            range = self.parentWin.scroller.GetScreenRect()
            # print repr(range)
            newpos = [winPos.x+delta.x, winPos.y+delta.y]
            # print repr(newpos)
            # if newpos[0]>=range.GetTopLeft().x and newpos[0] <= range.GetTopRight().x - self.frameSize.width and \
            #     newpos[1] >= range.GetTopLeft().y and newpos[1] <= range.GetBottomLeft().y - self.frameSize.height:
            #     self.Move(newpos)
            #     self.startPos = endPos

            if newpos[0] < range.GetTopLeft().x:
                newpos[0] = range.GetTopLeft().x
            if newpos[0] > range.GetTopRight().x - self.frameSize.width:
                newpos[0] = range.GetTopRight().x - self.frameSize.width
            if newpos[1] < range.GetTopLeft().y:
                newpos[1] = range.GetTopLeft().y
            if newpos[1] > range.GetBottomLeft().y - self.frameSize.height:
                newpos[1] = range.GetBottomLeft().y - self.frameSize.height
            self.Move(newpos)
            self.startPos = wx.Point(endPos[0], endPos[1])

    def On_RightMouse_up(self, event):
        self.PopupMenu(self.popMenu)

    def On_MenuCopy_Down(self, event):
        print self.subBmpRect
        image = self.parentWin.Bmp.GetSubBitmap(self.subBmpRect).ConvertToImage()
        self.parentWin.sampleCount = self.parentWin.sampleCount + 1
        imageFimeName = os.path.join(self.parentWin.BmpDirPath, repr(self.parentWin.sampleCount)) + u'.jpg'
        image.SaveFile(imageFimeName, wx.BITMAP_TYPE_JPEG)

    def On_MenuClose_Down(self, event):
        self.Close()

    def On_Paint(self, event):
        subBmpPos = self.parentWin.scroller.ScreenToClient(self.GetPosition())
        self.subBmpRect = subBmpRect = wx.Rect(subBmpPos.x, subBmpPos.y, self.frameSize.width, self.frameSize.height)
        bmp = self.parentWin.Bmp.GetSubBitmap(subBmpRect)
        dc = wx.BufferedDC(None, bmp)
        dc.SetPen(wx.Pen('red', width=2))
        dc.SetBrush(wx.Brush('red', wx.TRANSPARENT))
        dc.DrawRectangleRect(self.GetClientRect())
        self.BGBmpWin.SetBitmap(bmp)



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