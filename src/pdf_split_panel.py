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
		self.__rangesList = wx.ListBox(self)

		self.__createWidgets()

	def OnOpenPdfReadPath(self, event) -> None:
		self.__reader.path = event.GetPath()
		self.__setMinMaxRanges()

	def OnOpenPdfWritePath(self, event) -> None:
		self.__pathToSavePdf = event.GetPath()

	def OnAddRange(self, event) -> None:
		minValue = self.__minPageSpinCtrl.GetValue()
		maxValue = self.__maxPageSpinCtrl.GetValue()

		if minValue != maxValue:
			rangeText = f"Pages {minValue} to {maxValue}"
		else:
			rangeText = f"Page {minValue}"

		lastItemIdx = self.__rangesList.GetCount()
		self.__rangesList.InsertItems([rangeText], lastItemIdx)

		self.__removeRangeBtn.Enable()

	def OnRemoveRange(self, event) -> None:
		if self.__rangesList.GetSelection() != -1:
			idx = self.__rangesList.GetSelection()
			self.__rangesList.Delete(idx)

		if self.__rangesList.GetCount() == 0:
			self.__removeRangeBtn.Disable()

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

	def OnMinPageSpin(self, event) -> None:
		pass

	def OnMaxPageSpin(self, event) -> None:
		pass

	def __createWidgets(self) -> None:
		# File pickers

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

		rangesSizer = wx.BoxSizer(wx.HORIZONTAL)

		rangesSizer.Add(self.__rangesList, flag=wx.EXPAND | wx.BOTTOM, border=15, proportion=1)

		controlsSizer = wx.BoxSizer(wx.VERTICAL)

		self.__pagesStaticText = wx.StaticText(self, label="Total Pages: 0")
		controlsSizer.Add(self.__pagesStaticText, flag=wx.LEFT | wx.BOTTOM, border=15)

		# Pages spin ctrls

		pagesSizer = wx.BoxSizer(wx.HORIZONTAL)

		minPagesLabel = wx.StaticText(self, label="Pages")
		pagesSizer.Add(minPagesLabel, flag=wx.LEFT | wx.ALIGN_CENTRE_VERTICAL, border=15)

		self.__minPageSpinCtrl = wx.SpinCtrl(self, min=1, max=2, initial=1, size=(150, 20), style=wx.SP_WRAP)
		self.Bind(wx.EVT_SPINCTRL, self.OnMinPageSpin, self.__minPageSpinCtrl)
		pagesSizer.Add(self.__minPageSpinCtrl, flag=wx.LEFT, border=15)

		maxPagesLabel = wx.StaticText(self, label="to")
		pagesSizer.Add(maxPagesLabel, flag=wx.LEFT | wx.ALIGN_CENTRE_VERTICAL, border=15)

		self.__maxPageSpinCtrl = wx.SpinCtrl(self, min=2, max=2, initial=2, size=(150, 20), style=wx.SP_WRAP)
		self.Bind(wx.EVT_SPINCTRL, self.OnMaxPageSpin, self.__maxPageSpinCtrl)
		pagesSizer.Add(self.__maxPageSpinCtrl, flag=wx.LEFT, border=15)

		controlsSizer.Add(pagesSizer, flag=wx.BOTTOM, border=15)

		# Buttons

		addRangeBtn = wx.Button(self, label="Add Range", size=(150, 30))
		self.Bind(wx.EVT_BUTTON, self.OnAddRange, addRangeBtn)
		controlsSizer.Add(addRangeBtn, flag=wx.ALIGN_RIGHT | wx.BOTTOM, border=15)

		self.__removeRangeBtn = wx.Button(self, label="Remove Range", size=(150, 30))
		self.__removeRangeBtn.Disable()
		self.Bind(wx.EVT_BUTTON, self.OnRemoveRange, self.__removeRangeBtn)
		controlsSizer.Add(self.__removeRangeBtn, flag=wx.ALIGN_RIGHT | wx.BOTTOM, border=15)

		saveBtn = wx.Button(self, label="Save PDF", size=(150, 30))
		self.Bind(wx.EVT_BUTTON, self.OnSavePdf, saveBtn)
		controlsSizer.Add(saveBtn, flag=wx.ALIGN_RIGHT)

		# End

		rangesSizer.Add(controlsSizer, flag=wx.ALIGN_BOTTOM | wx.BOTTOM, border=15, proportion=1)
		self.__mainSizer.Add(rangesSizer, flag=wx.EXPAND, proportion=1)

		self.SetSizerAndFit(self.__mainSizer)

	def __setMinMaxRanges(self) -> None:
		meta = self.__reader.getMetadata()
		pages = int(meta.pages)

		self.__pagesStaticText.SetLabel(f"Total Pages: {pages}")

		self.__minPageSpinCtrl.SetRange(1, pages-1)
		self.__maxPageSpinCtrl.SetRange(2, pages)

		self.__minPageSpinCtrl.SetValue(1)
		self.__maxPageSpinCtrl.SetValue(2)