#!/usr/bin/python
# -*-<coding=UTF-8>-*-

"""
@Type: wxPython Objects.
@Author: YangZheng, UESTC.
@Functions: Frame to copy and show sub-regions form original image which created by main frame.
"""

import wx
import os.path

class ReSizeDlg(wx.Dialog):
    """
    @Object: Dialog ReSizeDlg
    """
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

class CopyFrame(wx.Frame):
    """
    @Functions: 用于选取样本的小窗口
    """
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

        self.Show()

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