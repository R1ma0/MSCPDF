import wx
from pypdf import PdfWriter
from reader import Reader
from custom_filepicker import CustomFilepicker



class PdfSplitPanel(wx.Panel):

	def __init__(self, parent):
		super(PdfSplitPanel, self).__init__(parent)

		self.__parent = parent
		self.__reader = Reader()
		self.__pathToSavePdf = None

		self.__mainSizer = wx.BoxSizer(wx.VERTICAL)

		self.__createWidgets()

	def __createWidgets(self) -> None:
		pdfReadPath = CustomFilepicker(
			self, 
			label="Select PDF file to read:", 
			msg="Select PDF file", 
			wildcard="PDF files (*.pdf)|*.pdf"
		)
		self.__mainSizer.Add(pdfReadPath.getSizer(), flag=wx.TOP | wx.EXPAND, border=15)
		self.Bind(wx.EVT_FILEPICKER_CHANGED, self.OnOpenPdfReadPath, pdfReadPath.getPicker())

		pdfWritePath = CustomFilepicker(
			self,
			label="Select path to save PDF:",
			msg="Enter filename to save",
			wildcard="PDF files (*.pdf)|*.pdf",
			pickerStyle=wx.FLP_SAVE | wx.FLP_OVERWRITE_PROMPT | wx.FLP_USE_TEXTCTRL
		)
		self.__mainSizer.Add(pdfWritePath.getSizer(), flag=wx.BOTTOM | wx.EXPAND, border=15)
		self.Bind(wx.EVT_FILEPICKER_CHANGED, self.OnOpenPdfWritePath, pdfWritePath.getPicker())

		saveBtn = wx.Button(self, label="Save PDF")
		self.__mainSizer.Add(saveBtn)
		self.Bind(wx.EVT_BUTTON, self.OnSavePdf, saveBtn)

		self.SetSizerAndFit(self.__mainSizer)
	
	def OnOpenPdfReadPath(self, event) -> None:
		self.__reader.path = event.GetPath()

	def OnOpenPdfWritePath(self, event) -> None:
		self.__pathToSavePdf = event.GetPath()

	def OnSavePdf(self, event) -> None:
		dialogMessage = "File successfully saved"
		dialogCaption = "PDF Read & Write Information!"
		dialogStyle = wx.OK_DEFAULT | wx.ICON_INFORMATION

		if self.__reader.path is not None and self.__pathToSavePdf is not None:
			writer = PdfWriter()
			# writer.append(self.__reader.path, [0, 2, 4])
			# writer.write(self.__pathToSavePdf)
			writer.close()
		else:
			dialogMessage = "Select paths for reading and writing PDFs"
			dialogCaption = "PDF Read & Write Warning!"
			dialogStyle = wx.OK_DEFAULT | wx.ICON_WARNING

		msgDialog = wx.MessageDialog(
			self, 
			message=dialogMessage, 
			caption=dialogCaption,
			style=dialogStyle
		)
		msgDialog.ShowModal()