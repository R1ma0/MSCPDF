import wx
from reader import Reader
from pdf_info import PdfInfo
from pdf_info_item import PdfInfoItem
from custom_filepicker import CustomFilepicker



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
		self.__showPdfInfoItems(False)

		self.__mainSizer = wx.BoxSizer(wx.VERTICAL)

		self.__fillPdfInfoItems()
		self.__createWidgets()

	def OnOpenPdf(self, event) -> None:
		self.__reader.path = event.GetPath()
		self.__fillPdfInfoItems()
		self.__showPdfInfoItems()
		self.SetSizerAndFit(self.__mainSizer)		

	def __createWidgets(self) -> None:
		pdfPicker = CustomFilepicker(
			self, 
			size=(775, 30), 
			label="Select PDF file", 
			msg="Select PDF file", 
			wildcard="PDF files (*.pdf)|*.pdf"
		)
		self.__mainSizer.Add(pdfPicker.getSizer(), flag=wx.TOP | wx.BOTTOM, border=15)
		self.Bind(wx.EVT_FILEPICKER_CHANGED, self.OnOpenPdf, pdfPicker.getPicker())

		for item in self.__infoItems:
			itemData = self.__infoItems.get(item)
			itemSizer = self.__createInfoSizer(itemData)
			self.__mainSizer.Add(itemSizer)
		
		self.SetSizerAndFit(self.__mainSizer)

	def __createInfoSizer(self, item) -> wx.BoxSizer:
		sizer = wx.BoxSizer(wx.HORIZONTAL)

		sizer.Add(item.labelStatic, proportion=0)
		sizer.Add(item.dataStatic, proportion=1)

		return sizer

	def __fillPdfInfoItems(self) -> None:

		def setData(self, key, value) -> None:
			self.__infoItems.get(key).data = value if value is not None else "Empty"

		meta = self.__reader.getMetadata()

		setData(self, "pages", meta.pages)
		setData(self, "title", meta.title)
		setData(self, "author", meta.author)
		setData(self, "subject", meta.subject)
		setData(self, "creator", meta.creator)
		setData(self, "producer", meta.producer)

	def __showPdfInfoItems(self, state=True) -> None:
		for item in self.__infoItems:
			i = self.__infoItems.get(item)
			i.show(state)