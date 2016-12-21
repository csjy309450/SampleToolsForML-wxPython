#!/usr/bin/python
# -*-<coding=UTF-8>-*-

"""
Hello,wxPython! program.
@Author: YangZheng, UESTC
@Functions: Sample training set from loading images
"""

import wx
import SampleFrame

class App(wx.App):
    """
    @Object: wxApp
    @Functions: Create a wx App.
    """
    def OnInit(self):
        self.frame = SampleFrame.SampleFrame()

        self.SetTopWindow(self.frame)
        return True

def main():
    app = App()
    app.MainLoop()

if __name__ == "__main__":
    main()