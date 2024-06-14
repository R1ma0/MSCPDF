import wx
from main_window import MainWindow
from constants import *



if __name__ == "__main__":
    app = wx.App()

    frame = MainWindow(
        None, 
        size=(WINDOW_WIDTH, WINDOW_HEIGHT), 
        title=WINDOW_TITLE, 
        style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)
    )
    frame.Show()

    app.MainLoop()
