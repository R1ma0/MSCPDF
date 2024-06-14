import wx
from pdf_info_panel import PdfInfoPanel
from reader import Reader
import test_pdf



class MainWindow(wx.Frame):

    def __init__(self, *args, **kw):
        super(MainWindow, self).__init__(*args, **kw)

        self.__reader = Reader(test_pdf.PDF_PATHS[1])
        self.__pdfMetadata = self.__reader.getMetadata

        self.Centre()
        self.__createWidgets()
        self.__createMenuBar()
        self.CreateStatusBar()

    def __createWidgets(self):
        mainPanel = wx.Panel(self)

        notebook = self.__createNotebook(mainPanel)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(notebook, proportion=1, flag=wx.EXPAND)

        mainPanel.SetSizer(mainSizer)

    def __createNotebook(self, parent) -> wx.Notebook:
        notebook = wx.Notebook(parent)

        tabInfo = PdfInfoPanel(notebook, "Information", self.__pdfMetadata)
        notebook.AddPage(tabInfo, tabInfo.title)

        return notebook

    def __createMenuBar(self) -> None:
        fileMenu = wx.Menu()
        openPdfFileItem = fileMenu.Append(wx.ID_ANY, "&Open PDF\tCtrl-O")
        fileMenu.AppendSeparator()
        exitItem = fileMenu.Append(wx.ID_EXIT, "&Quit\tCtrl-Q", "Close app")

        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")

        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.OnExit, exitItem)
        self.Bind(wx.EVT_MENU, self.OnOpenPdf, openPdfFileItem)

    def OnExit(self, event) -> None:
        self.Close(True)

    def OnOpenPdf(self, event) -> None:
        print("OK")
