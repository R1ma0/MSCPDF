import wx
from pdf_info import PdfInfo
from reader import Reader
from pdf_info_item import PdfInfoItem



class PdfInfoPanel(wx.Panel):
	
	def __init__(self, parent):
		super(PdfInfoPanel, self).__init__(parent)

		self.__parent = parent
		self.__reader = Reader()
		self.__infoItems = {
			"pages": PdfInfoItem(self, "Pages:"),
			"title": PdfInfoItem(self, "Title:"),
			"author": PdfInfoItem(self, "Author:"),
			"subject": PdfInfoItem(self, "Subject:"),
			"creator": PdfInfoItem(self, "Creator:"),
			"producer": PdfInfoItem(self, "Producer:"),
		}

		self.__fillPdfInfoItems()
		self.__createWidgets()

	def __createWidgets(self):
		viewSizer = wx.BoxSizer(wx.VERTICAL)

		openPdfBtn = wx.Button(self, label="Open PDF")
		self.Bind(wx.EVT_BUTTON, self.OnOpenPdf, openPdfBtn)
		viewSizer.Add(openPdfBtn)

		for item in self.__infoItems:
			itemData = self.__infoItems.get(item)
			itemSizer = self.__createInfoSizer(itemData)
			viewSizer.Add(itemSizer)
		
		self.SetSizerAndFit(viewSizer)

	def __createInfoSizer(self, item) -> wx.BoxSizer:
		sizer = wx.BoxSizer(wx.HORIZONTAL)

		sizer.Add(item.labelStatic, proportion=0)
		sizer.Add(item.dataStatic, proportion=1)

		return sizer

	def __fillPdfInfoItems(self):

		def setData(self, key, value) -> None:
			if value is not None:
				self.__infoItems.get(key).data = value

		meta = self.__reader.getMetadata()

		setData(self, "pages", meta.pages)
		setData(self, "title", meta.title)
		setData(self, "author", meta.author)
		setData(self, "subject", meta.subject)
		setData(self, "creator", meta.creator)
		setData(self, "producer", meta.producer)

	def OnOpenPdf(self, event) -> None:
		with wx.FileDialog(
			self, 
			"Select PDF file", 
			wildcard="PDF files (*.pdf)|*.pdf",
			style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
		) as openFileDialog:
			if openFileDialog.ShowModal() == wx.ID_CANCEL:
				return

			self.__reader.path = openFileDialog.GetPath()
			self.__fillPdfInfoItems()
		