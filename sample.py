# coding=utf8

import wx


class MsgWindow(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, pos=(640, 0))

        # 重要的就下边两句
        self.scroller = wx.ScrolledWindow(self, -1)
        self.scroller.SetScrollbars(1, 1, 1440, 900)

        self.pnl = pnl = wx.Panel(self.scroller)
        self.ms = ms = wx.BoxSizer(wx.VERTICAL)

        self.SetMinSize((300, 640))
        self.pnl.SetSizer(self.ms)
        self.ms.Fit(self)


if __name__ == '__main__':
    app = wx.App(redirect=False)
    msg_win = MsgWindow(None, -1, u'消息')
    msg_win.Show(True)
    app.MainLoop()