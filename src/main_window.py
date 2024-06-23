import wx
from pdf_info_panel import PdfInfoPanel
from pdf_split_panel import PdfSplitPanel
from pdf_merge_panel import PdfMergePanel
from app_icons import *



class MainWindow(wx.Frame):

    def __init__(self, *args, **kw):
        super(MainWindow, self).__init__(*args, **kw)

        self.__statusBar = self.CreateStatusBar()
        self.Centre()
        self.__createWidgets()
        self.__createMenuBar()

    def OnExit(self, event: wx.Event) -> None:
        self.Close(True)

    def __createWidgets(self):
        """
        Creates interface elements
        """
        mainPanel = wx.Panel(self)
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        notebook = self.__createNotebook(mainPanel)
        mainSizer.Add(notebook, proportion=1, flag=wx.EXPAND)

        mainPanel.SetSizer(mainSizer)

    def __createNotebook(self, parent: wx.Window) -> wx.Notebook:
        appIcons = getAppImagesList(24, 24)
        notebook = wx.Notebook(parent)
        notebook.AssignImageList(appIcons)

        tabMetadata = PdfInfoPanel(notebook)
        tabMetadata.SetStatusBar(self.__statusBar)
        notebook.AddPage(tabMetadata, "Metadata")
        notebook.SetPageImage(0, 6)

        tabSplit = PdfSplitPanel(notebook)
        tabSplit.SetStatusBar(self.__statusBar)
        notebook.AddPage(tabSplit, "Split")
        notebook.SetPageImage(1, 7)

        tabMerge = PdfMergePanel(notebook)
        tabMerge.SetStatusBar(self.__statusBar)
        notebook.AddPage(tabMerge, "Merge")
        notebook.SetPageImage(2, 8)

        return notebook

    def __createMenuBar(self) -> None:
        fileMenu = wx.Menu()
        fileMenu.AppendSeparator()

        exitItem = fileMenu.Append(wx.ID_EXIT, "&Quit\tCtrl-Q", "Close app")
        self.Bind(wx.EVT_MENU, self.OnExit, exitItem)

        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")

        self.SetMenuBar(menuBar)