import wx
from pdf_info import PdfInfo
from constants import *



class PdfInfoPanel(wx.Panel):
	
	def __init__(self, parent, title, pdfInfo):
		super(PdfInfoPanel, self).__init__(parent)

		self.title = title
		self.__pdfInfo = pdfInfo
		self.__parent = parent

		self.__createWidgets()

	def __createWidgets(self):
		info = self.__pdfInfo

		infoItems = (
			("Pages:", info.pages),
			("Title:", info.title),
			("Author:", info.author),
			("Subject:", info.subject),
			("Creator:", info.creator),
			("Producer:", info.producer)
		)

		viewSizer = wx.BoxSizer(wx.VERTICAL)

		for item in infoItems:
			itemSizer = self.__createInfoSizer(item[0], item[1])
			viewSizer.Add(itemSizer)
		
		self.SetSizerAndFit(viewSizer)

	def __createInfoSizer(self, label, text) -> wx.BoxSizer:
		fontBold = wx.Font(12, wx.DEFAULT, wx.BOLD, wx.NORMAL)
		fontNormal = wx.Font(12, wx.DEFAULT, wx.ITALIC, wx.NORMAL)

		subjectLabel = wx.StaticText(self, label=label, size=(100, 30))
		subjectLabel.SetFont(fontBold)

		subjectText = wx.StaticText(self, label=text)
		subjectText.SetFont(fontNormal)
		subjectText.Wrap(WINDOW_WIDTH - 125)
		
		sizer = wx.BoxSizer(wx.HORIZONTAL)
		sizer.Add(subjectLabel, proportion=0)
		sizer.Add(subjectText, proportion=1)

		return sizer