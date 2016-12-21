#!/usr/bin/python
# -*-<coding=UTF-8>-*-

"""
Hello,wxPython! program.
@ Author: YangZheng, UESTC
@ Functions: Sample training set from loading images
"""

import wx
import os.path


class SampleFrame(wx.Frame):
    """
    创建一个wx.Frame的子类
    """

    def __init__(self, parent=None, id=-1, pos=wx.DefaultPosition, title="sample tool"):
        """
        __init__中哪些参数是必须的,每次这么多参数,谁能记得住.
        不过,参数没有顺序要求.想想,创建一个frame需要哪些东西,无非就是位置,大小,标题,ID之类的内容.
        """

        wx.Frame.__init__(self, parent, id, title, pos, size=(400, 400))

        self.PositiveSampleRect = [[None, None]]
        self.NegativeSampleRect = [[None, None]]
        self.CurrentBmpPosition = [0, 0]
        self.ImgPathsManager = {'index': -1, 'Paths': []}

        self.InitUI()
        self.InitDrawTools()

        # # 绑定鼠标在图片上的操作事件响应函数
        self.scroller.Bind(wx.EVT_SCROLLWIN_THUMBTRACK, self.On_ScrollBar_Down)
        self.Bind(wx.EVT_MENU, self.On_Menu_Open, self.menuItemOpen)
        self.Bind(wx.EVT_MENU, self.On_Menu_Save, self.menuItemSave)
        self.Bind(wx.EVT_MENU, self.On_Menu_Next, self.menuItemNext)
        self.Bind(wx.EVT_MENU, self.On_Menu_Prior, self.menuItemPrior)
        self.Bind(wx.EVT_MENU, self.On_Menu_Screenshot, self.menuItemScreenshotWindow)
        self.Bind(wx.EVT_MENU, self.On_Menu_DirectDraw, self.menuItemDirectDraw)
        self.Bind(wx.EVT_MENU, self.On_Menu_Close, self.menuItemClose)
        self.Bind(wx.EVT_SIZE, self.On_Window_Resize)
        self.slider.Bind(wx.EVT_SLIDER, self.On_Slider_Motion)


    """
    初始化窗口中的GUI
    """
    def InitUI(self):
        WindSize = self.GetClientSize()
        # 添加滑块,调整图像尺度
        self.slider = wx.Slider(self, -1, 10, 0, 20, pos=(0, 0),
                           style=wx.SL_HORIZONTAL |wx.SL_LABELS)
        self.slider.SetTickFreq(1, 1)

        # 添加滑动栏，主要解决显示大图的问题
        # sliderSize = self.slider.GetClientSize()
        self.scroller = wx.ScrolledWindow(self, -1, pos=(0, self.slider.GetClientSize().y))

        #添加菜单栏
        menubar = wx.MenuBar()
        menuFile = wx.Menu()
        self.menuItemOpen = menuFile.Append(-1, '&Open')
        self.menuItemSave = menuFile.Append(-1, "&Save")
        self.menuItemNext = menuFile.Append(-1, "&Next")
        self.menuItemPrior = menuFile.Append(-1, "&Prior")
        self.menuItemScreenshotWindow = menuFile.Append(-1, "&Screenshot Window")
        self.menuItemDirectDraw = menuFile.Append(-1, "&Direct Draw")
        self.menuItemClose = menuFile.Append(-1, "&Close")
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
        self.TileSize_y = TileSize_y = self.GetSize()[1]-self.GetClientSize()[1]
        # 获取图片大小,同时作为Frame的大小
        self.BmpSize = self.Bmp.GetWidth(), self.Bmp.GetHeight()

        # 创建静态位图窗口
        self.ImgWin.SetBitmap(self.Bmp)
        # 设置窗口的最大大小
        self.SetMaxSize([self.BmpSize[0], self.BmpSize[1] + self.slider.GetSize()[1]+TileSize_y])
        # 设置滑动条尺寸
        self.scroller.SetScrollbars(1, 1, self.BmpSize[0], self.BmpSize[1])

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
            self.ImgPathsManager['Paths'] = dlg.GetPaths()
            self.ImgPathsManager['Index'] = -1
            # print self.ImgPaths
            dlg.Close()
            # print self.ImgPaths
        if len(self.ImgPathsManager['Paths']) <= 0:
            pass
        else:
            try:
                del self.Bmp
            except AttributeError, err:
                print "There have no Bitmap file currently!"
            self.ImgPathsManager['Index'] += 1
            self.currentBmpPath = self.ImgPathsManager['Paths'][self.ImgPathsManager['Index']]
            # print self.currentBmpPath
            # create sample directory
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

    def On_Menu_Next(self, event=None):
        if len(self.ImgPathsManager['Paths']) <= self.ImgPathsManager['Index']+1:
            print "Have no next bitmap file!"
        else:
            try:
                del self.Bmp
            except AttributeError, err:
                print "There have no Bitmap file currently!"

            self.ImgPathsManager['Index'] += 1
            self.currentBmpPath = self.ImgPathsManager['Paths'][self.ImgPathsManager['Index']]
            self.LoadImage()
            # self.Bmp = self.image.ConvertToBitmap()
            self.ResizeWindowByBmp()

    def On_Menu_Prior(self, event=None):
        if self.ImgPathsManager['Index'] <= 0:
            print "Have no prior bitmap file!"
        else:
            try:
                del self.Bmp
            except AttributeError, err:
                print "There have no Bitmap file currently!"

            self.ImgPathsManager['Index'] -= 1
            self.currentBmpPath = self.ImgPathsManager['Paths'][self.ImgPathsManager['Index']]
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
        self.slider_screenshotFrameSizer = wx.Slider(self, -1, 10, 0, 20, pos=(self.GetClientSize()[0]/2, 0),
                           style=wx.SL_HORIZONTAL |wx.SL_LABELS)
        # print self.slider.GetSize()[1] + self.slider_screenshotFrameSizer.GetSize()[1]
        self.slider.SetTickFreq(1, 1)
        self.SetMaxSize((self.BmpSize[0], self.slider.GetSize()[1]+self.BmpSize[1]+self.TileSize_y))
        self.Refresh(False)
        self.screenshotFrame = CopyFrame(parent=self, Pos=self.scroller.GetScreenPosition())
        self.screenshotFrame.Show()


    def On_Menu_DirectDraw(self, event):
        # 绑定鼠标在图片上的操作事件响应函数
        self.ImgWin.Bind(wx.EVT_LEFT_DOWN, self.On_Mouse_Left_Down)
        # self.ImgWin.Bind(wx.EVT_MOTION, self.On_Mouse_Move)
        self.ImgWin.Bind(wx.EVT_LEFT_UP, self.On_Mouse_Left_Up)
        self.ImgWin.Bind(wx.EVT_RIGHT_DOWN, self.On_Mouse_Right_Down)
        self.ImgWin.Bind(wx.EVT_RIGHT_UP, self.On_Mouse_Right_Up)

    # def On_Key_Down(self, event):
    #     keycode = event.GetKeyCode()
    #     print type(keycode), ':', chr(keycode)
    #     if chr(keycode) == 'E':
    #         self.parentWin.On_Menu_Next()
    #     elif chr(keycode) == 'Q':
    #         self.parentWin.On_Menu_Prior()

    def On_Window_Resize(self, event):
        winSize = self.GetClientSize()
        sliderSize = self.slider.GetClientSize()
        sliderSize.x = winSize.x/2
        # print repr(sliderSize)
        self.slider.SetSize(sliderSize)
        try:
            self.slider_screenshotFrameSizer.SetPosition((winSize.x/2, 0))
            self.slider_screenshotFrameSizer.SetSize(sliderSize)
        except AttributeError, err:
            pass
        self.scroller.SetSize(wx.Size(winSize.x, winSize.y-sliderSize.y))

    def On_Menu_Close(self, event):
        pass

    def On_Slider_Motion(self, event):
        # print self.slider.GetValue()
        newScalar = self.slider.GetValue()
        size = self.image.GetSize()
        self.ScaleImag = self.image.Copy()
        self.ScaleImag.Rescale(size.x*newScalar*0.1, size.y*newScalar*0.1)
        self.Bmp = self.ScaleImag.ConvertToBitmap()
        self.ResizeWindowByBmp()
    def __del__(self):
        self.screenshotFrame.Destroy()


###########################################################################
## Class ReSizeDlg
###########################################################################
class ReSizeDlg(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=-1, title=wx.EmptyString, pos=wx.DefaultPosition,
                               size=wx.Size(100, 150), style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        self.m_button_OK = wx.Button(self, wx.ID_ANY, u"OK", wx.Point(100, 10), wx.DefaultSize, 0)
        bSizer1.Add(self.m_button_OK, 0, wx.ALL, 5)

        self.m_textCtrl_width = wx.TextCtrl(self, wx.ID_ANY, str(parent.frameSize.width), wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.m_textCtrl_width, 0, wx.ALL, 5)

        self.m_textCtrl_height = wx.TextCtrl(self, wx.ID_ANY, str(parent.frameSize.height), wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.m_textCtrl_height, 0, wx.ALL, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        self.Bind(wx.EVT_BUTTON, self.OnButtonOk, source=self.m_button_OK)

    def OnButtonOk(self, event):
        try:
            self.newWidth = int(self.m_textCtrl_width.GetLineText(0))
            self.newHeight = int(self.m_textCtrl_height.GetLineText(0))
        except:
            pass
        self.EndModal(wx.ID_OK)

"""
用于选取样本的小窗口
"""
class CopyFrame(wx.Frame):
    def __init__(self, parent=None, Pos=None):
        self.parentWin = parent
        # print pos
        self.frameSize = wx.Size(50, 50)
        if Pos == None:
            t_pos = parent.scroller.GetScreenPosition()
            wx.Frame.__init__(self, None, wx.NewId(), pos=t_pos, size=self.frameSize,
                              style=wx.NO_BORDER | wx.STAY_ON_TOP)
        else:
            wx.Frame.__init__(self, None, wx.NewId(), pos=Pos, size=self.frameSize,
                              style=wx.NO_BORDER | wx.STAY_ON_TOP)

        self.SetBackgroundColour(wx.Colour(0, 0, 0, wx.ALPHA_TRANSPARENT))

        self.InitUI()
        self.InitBufferDC()

        self.MouseDown = False

        self.Bind(wx.EVT_LEFT_DOWN, self.On_LeftMouse_Down)
        self.Bind(wx.EVT_LEFT_UP, self.On_LeftMouse_Up)
        self.Bind(wx.EVT_MOTION, self.On_Mouse_Move)
        self.Bind(wx.EVT_RIGHT_UP, self.On_RightMouse_up)
        self.Bind(wx.EVT_PAINT, self.On_Paint)
        self.Bind(wx.EVT_SIZE, self.On_Size)
        self.Bind(wx.EVT_MENU, self.On_MenuCopy_Down, self.MenuItemCopy)
        self.Bind(wx.EVT_MENU, self.On_MenuClose_Down, self.MenuItemClose)
        self.Bind(wx.EVT_MENU, self.On_MenuResize_Down, self.MenuItemResize)
        self.Bind(wx.EVT_IDLE, self.On_Idle)
        self.Bind(wx.EVT_KEY_DOWN, self.On_Key_Down)
        self.panel.Bind(wx.EVT_KEY_DOWN, self.On_Key_Down)
        self.panel.SetFocus()

    def __del__(self):
        del self.parentWin
        del self.frameSize
        del self.MouseDown
        del self.popMenu
        del self.MenuItemCopy
        del self.MenuItemClose
        del self.MenuItemResize
        del self.BGBmp
        del self.dc
        del self.refreshFlag

    def InitUI(self):
        self.panel = wx.Panel(self, size=(0, 0))
        self.popMenu = wx.Menu()
        self.MenuItemCopy = self.popMenu.Append(-1, "&Copy")
        self.MenuItemClose = self.popMenu.Append(-1, "&Close")
        self.MenuItemResize = self.popMenu.Append(-1, "&Resize")

    def InitBufferDC(self):
        self.BGBmp = wx.EmptyBitmap(self.frameSize.width, self.frameSize.height)
        # dc2=self.panel.SetDoubleBuffered()
        self.dc = wx.BufferedDC(None, self.BGBmp)
        self.refreshFlag = True

    def On_LeftMouse_Down(self, event):
        self.GetCapture()
        self.startPos = self.ClientToScreen(event.GetPosition())

    def On_LeftMouse_Up(self, event):
        if self.HasCapture():
            self.ReleaseMouse()

    def __WinMoveTo(self, moveFlage, _newpos=None):
        """
        :param moveFlage: 'Drage', 'Up', 'Down', 'Right', 'Left'
        :param _newpos: when moveFlage=='Drage', param gives new position for moving.
        :return:
        """
        newpos = wx.Point()
        if moveFlage == 'Drage' and _newpos != None:
            newpos = _newpos
        elif moveFlage == 'Up':
            newpos = self.GetScreenPosition()
            newpos[1] -= 1
        elif moveFlage == 'Down':
            newpos = self.GetScreenPosition()
            newpos[1] += 1
        elif moveFlage == 'Right':
            newpos = self.GetScreenPosition()
            newpos[0] += 1
        elif moveFlage == 'Left':
            newpos = self.GetScreenPosition()
            newpos[0] -= 1
        else:
            return
        range = self.parentWin.scroller.GetScreenRect()
        if newpos[0] < range.GetTopLeft().x:
            newpos[0] = range.GetTopLeft().x
        if newpos[0] > range.GetTopRight().x - self.frameSize.width:
            newpos[0] = range.GetTopRight().x - self.frameSize.width
        if newpos[1] < range.GetTopLeft().y:
            newpos[1] = range.GetTopLeft().y
        if newpos[1] > range.GetBottomLeft().y - self.frameSize.height:
            newpos[1] = range.GetBottomLeft().y - self.frameSize.height
        self.Move(newpos)
        self.refreshFlag = True


    def On_Mouse_Move(self, event):
        if event.Dragging() and event.LeftIsDown():
            endPos = wx.GetMousePosition()
            delta = endPos - self.startPos
            winPos = self.GetScreenPosition()
            # print repr(winPos)
            # print repr(range)
            newpos = [winPos.x+delta.x, winPos.y+delta.y]
            # print repr(newpos)

            # move to new position
            # range = self.parentWin.scroller.GetScreenRect()
            # if newpos[0] < range.GetTopLeft().x:
            #     newpos[0] = range.GetTopLeft().x
            # if newpos[0] > range.GetTopRight().x - self.frameSize.width:
            #     newpos[0] = range.GetTopRight().x - self.frameSize.width
            # if newpos[1] < range.GetTopLeft().y:
            #     newpos[1] = range.GetTopLeft().y
            # if newpos[1] > range.GetBottomLeft().y - self.frameSize.height:
            #     newpos[1] = range.GetBottomLeft().y - self.frameSize.height
            # self.Move(newpos)
            self.__WinMoveTo('Drage', newpos)
            self.startPos = wx.Point(endPos[0], endPos[1])
        event.Skip()
        self.panel.SetFocus()

    def On_RightMouse_up(self, event):
        self.PopupMenu(self.popMenu)

    def On_MenuCopy_Down(self, event=None):
        print self.subBmpRect
        image = self.parentWin.Bmp.GetSubBitmap(self.subBmpRect).ConvertToImage()
        self.parentWin.sampleCount = self.parentWin.sampleCount + 1
        imageFimeName = os.path.join(self.parentWin.BmpDirPath, repr(self.parentWin.sampleCount)) + u'.jpg'
        image.SaveFile(imageFimeName, wx.BITMAP_TYPE_JPEG)
        self.panel.SetFocus()

    def On_MenuClose_Down(self, event):
        try:
            self.Close(True)
        except:
            pass
        self.panel.SetFocus()

    def On_MenuResize_Down(self, event):
        reSizeDlg = ReSizeDlg(self)
        if reSizeDlg.ShowModal() == wx.ID_OK:
            self.frameSize = wx.Size(reSizeDlg.newWidth, reSizeDlg.newHeight)
            self.SetSize(self.frameSize)
            self.refreshFlag = True
        self.panel.SetFocus()

    def On_Paint(self, event):
        self.dc = wx.BufferedPaintDC(self, self.BGBmp)
        self.SetFocus()
        event.Skip()
        self.panel.SetFocus()

    def On_Size(self, event):
        self.BGBmp.SetWidth(self.frameSize.width)
        self.BGBmp.SetHeight(self.frameSize.height)
        self.refreshFlag = True
        self.panel.SetFocus()

    def On_Idle(self, event):
        if self.refreshFlag == True:
            subBmpPos = self.parentWin.scroller.ScreenToClient(self.GetPosition())
            self.subBmpRect = subBmpRect = wx.Rect(subBmpPos.x, subBmpPos.y, self.frameSize.width, self.frameSize.height)
            bmp = self.parentWin.Bmp.GetSubBitmap(subBmpRect)
            self.dc.SetPen(wx.Pen('red', width=1))
            self.dc.SetBrush(wx.Brush('red', wx.TRANSPARENT))
            # print self.GetClientRect()
            self.dc.DrawBitmap(bmp, 0, 0)
            self.dc.DrawRectangleRect(self.GetClientRect())
            self.Refresh(False)
            self.refreshFlag = False
        event.Skip()
        self.SetFocus()

    def On_Key_Down(self, event):
        keycode = event.GetKeyCode()
        print type(keycode), ':', chr(keycode)
        if chr(keycode) == 'E':
            self.parentWin.On_Menu_Next()
        elif chr(keycode) == 'Q':
            self.parentWin.On_Menu_Prior()
        elif chr(keycode) == 'A':
            self.__WinMoveTo('Left')
        elif chr(keycode) == 'D':
            self.__WinMoveTo('Right')
        elif chr(keycode) == 'W':
            self.__WinMoveTo('Up')
        elif chr(keycode) == 'S':
            self.__WinMoveTo('Down')
        elif chr(keycode) == 'F':
            self.On_MenuCopy_Down()
        else:
            self.SetFocus()
            event.Skip()
            return
        event.Skip()
        self.refreshFlag = True
        self.SetFocus()


class App(wx.App):
    def OnInit(self):

        self.frame = SampleFrame()

        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True


def main():
    app = App()
    app.MainLoop()


if __name__ == "__main__":
    main()