import wx
from pdf_rw import PdfRW
from pdf_info import PdfInfo
from pdf_info_item import PdfInfoItem
from custom_file_picker import CustomFilePicker
from notebook_panel import NotebookPanel



class PdfInfoPanel(wx.Panel, NotebookPanel):
	"""
	Panel containing PDF metadata
	"""
	
	def __init__(self, parent: wx.Window):
		super(PdfInfoPanel, self).__init__(parent)
		NotebookPanel.__init__(self)

		self.__parent = parent
		self.__pdfRW = PdfRW()
		self.__infoItems = self.__initInfoItems()
		
		self.__showPdfInfoItems(False)
		self.__fillPdfInfoItems()
		self.__createWidgets()

	def OnOpenPdf(self, event: wx.Event) -> None:
		self.__pdfRW.path = event.GetPath()

		try:
			_ =self.__pdfRW.getMetadata() 
		except FileNotFoundError:
			self.SetStatusBarText("Specified file not found!")
		else:
			self.__fillPdfInfoItems()
			self.__showPdfInfoItems()

			self.SetSizerAndFit(self.__mainSizer)		

	def __createWidgets(self) -> None:
		"""
		Creates interface elements
		"""
		self.__mainSizer = wx.BoxSizer(wx.VERTICAL)

		self.__createFilePicker()
		self.__createInfoItems()
		
		self.SetSizerAndFit(self.__mainSizer)

	def __createFilePicker(self) -> None:
		pdfFP = CustomFilePicker(
			self, 
			size=(745, 30), 
			label="Select PDF file", 
			msg="Select PDF file", 
			wildcard="PDF files (*.pdf)|*.pdf"
		)
		self.__mainSizer.Add(pdfFP.getSizer(), flag=wx.ALL, border=15)
		self.Bind(wx.EVT_FILEPICKER_CHANGED, self.OnOpenPdf, pdfFP.getPicker())

	def __initInfoItems(self) -> dict:
		"""
		Filling initial metadata parameters
		"""
		return {
			"pages": PdfInfoItem(self, "Pages:"),
			"title": PdfInfoItem(self, "Title:"),
			"author": PdfInfoItem(self, "Author:"),
			"subject": PdfInfoItem(self, "Subject:"),
			"creator": PdfInfoItem(self, "Creator:"),
			"producer": PdfInfoItem(self, "Producer:"),
		}

	def __createInfoItems(self) -> None:
		"""
		Creates a pair of title and metadata text
		"""
		for item in self.__infoItems:
			itemData = self.__infoItems.get(item)
			itemSizer = self.__createInfoSizer(itemData)

			self.__mainSizer.Add(itemSizer, flag=wx.LEFT | wx.RIGHT, border=15)

	def __createInfoSizer(self, item: PdfInfoItem) -> wx.BoxSizer:
		sizer = wx.BoxSizer(wx.HORIZONTAL)

		sizer.Add(item.labelStatic, proportion=0)
		sizer.Add(item.textStatic, proportion=1)

		return sizer

	def __fillPdfInfoItems(self) -> None:
		"""
		Display metadata after PDF load
		"""
		def setData(self, key: str, value: str) -> None:
			self.__infoItems.get(key).text = value if value != None else "Empty"

		meta = self.__pdfRW.getMetadata() 

		setData(self, "pages", meta.pages)
		setData(self, "title", meta.title)
		setData(self, "author", meta.author)
		setData(self, "subject", meta.subject)
		setData(self, "creator", meta.creator)
		setData(self, "producer", meta.producer)

	def __showPdfInfoItems(self, state: bool = True) -> None:
		"""
		Hides or shows metadata items
		"""
		for item in self.__infoItems:
			i = self.__infoItems.get(item)
			i.show(state)