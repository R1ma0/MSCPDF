import wx
from reader import Reader



class PdfSplitPanel(wx.Panel):

	def __init__(self, parent):
		super(PdfSplitPanel, self).__init__(parent)

		self.__parent = parent
		self.__reader = Reader()

		self.__mainSizer = wx.BoxSizer(wx.VERTICAL)

		self.__createWidgets()

	def __createWidgets(self) -> None:
		self.SetSizerAndFit(self.__mainSizer)