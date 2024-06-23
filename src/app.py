import wx
from main_window import MainWindow
from constants import *
from app_icons import *



if __name__ == "__main__":
    app = wx.App()
    appIcons = getAppImagesList(24, 24)

    frame = MainWindow(
        None, 
        size=(WINDOW_WIDTH, WINDOW_HEIGHT), 
        title=WINDOW_TITLE, 
        style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)
    )
    frame.SetIcon(wx.Icon(appIcons.GetBitmap(9)))
    frame.Show()

    app.MainLoop()
