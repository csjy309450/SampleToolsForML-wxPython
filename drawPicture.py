import wx

class mainFrame(wx.Frame):
    def __init__(self, parent=None, pos=wx.DefaultPosition, title="Hello,wxPython!"):
        wx.Frame.__init__(self, parent=parent, title=title, pos=pos, size=(1000, 1000))

        temp = wx.Image("/home/yangzheng/myProgram/test/crow1.jpg", wx.BITMAP_TYPE_ANY)
        self.Bmp = temp.ConvertToBitmap()
        #self.BmpWin = wx.StaticBitmap(parent=self, bitmap=self.Bmp)
        #print self.BmpWin
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnPaint(self):
        dc = wx.PaintDC(self)
        dc.clear()
        dc.SetPen(wx.Pen(wx.BLACK, 4))
        dc.DrawLine(0, 0, 50, 50)

def main():
    app = wx.App()
    mainWin = mainFrame()
    mainWin.Show()
    app.SetTopWindow(mainWin)
    app.MainLoop()

if __name__=='__main__':
    main()