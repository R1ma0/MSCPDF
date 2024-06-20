import wx
from pdf_info_panel import PdfInfoPanel
from pdf_split_panel import PdfSplitPanel



class MainWindow(wx.Frame):
    
    def __init__(self, *args, **kw):
        super(MainWindow, self).__init__(*args, **kw)

        self.Centre()
        self.__createWidgets()
        self.__createMenuBar()
        self.CreateStatusBar()

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
        notebook = wx.Notebook(parent)

        tabMetadata = PdfInfoPanel(notebook)
        notebook.AddPage(tabMetadata, "Metadata")

        tabSplit = PdfSplitPanel(notebook)
        notebook.AddPage(tabSplit, "Split")

        tabMerge = wx.Panel(notebook)
        notebook.AddPage(tabMerge, "Merge")

        return notebook

    def __createMenuBar(self) -> None:
        fileMenu = wx.Menu()
        fileMenu.AppendSeparator()

        exitItem = fileMenu.Append(wx.ID_EXIT, "&Quit\tCtrl-Q", "Close app")
        self.Bind(wx.EVT_MENU, self.OnExit, exitItem)

        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")

        self.SetMenuBar(menuBar)