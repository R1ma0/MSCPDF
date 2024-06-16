import wx
import os
from enum import Enum
from pypdf import PdfWriter
from reader import Reader
from custom_filepicker import CustomFilepicker



class SplitMode(Enum):
	SINGLE = 0
	MULTIPLE = 1



class PdfSplitPanel(wx.Panel):

	def __init__(self, parent):
		super(PdfSplitPanel, self).__init__(parent)

		self.__parent = parent
		self.__reader = Reader()
		self.__pathToSavePdf = None
		self.__pdfPageRangeList = []

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

		self.__pdfPageRangeList.append([minValue, maxValue])

		lastItemIdx = self.__rangesList.GetCount()
		self.__rangesList.InsertItems([rangeText], lastItemIdx)

		self.__removeRangeBtn.Enable()
		self.__clearRangesBtn.Enable()

	def OnRemoveRange(self, event) -> None:
		if self.__rangesList.GetSelection() != -1:
			idx = self.__rangesList.GetSelection()
			self.__rangesList.Delete(idx)

			self.__pdfPageRangeList.pop(idx)

		if self.__rangesList.GetCount() == 0:
			self.__removeRangeBtn.Disable()
			self.__clearRangesBtn.Disable()

	def OnSavePdf(self, event) -> None:
		srcPathNotNone = self.__reader.path is not None
		savePathNotNone = self.__pathToSavePdf is not None
		pageRangesNotEmpty = len(self.__pdfPageRangeList) != 0

		dialogMessage = "File successfully saved"
		dialogCaption = "PDF Read & Write Information!"
		dialogStyle = wx.OK_DEFAULT | wx.ICON_INFORMATION

		if srcPathNotNone and savePathNotNone and pageRangesNotEmpty:
			selectedSplitMode = self.__splitSaveModeRadio.GetSelection()

			if selectedSplitMode == SplitMode.SINGLE.value:
				self.__writeSinglePdf()
			if selectedSplitMode == SplitMode.MULTIPLE.value:
				self.__writeMultiplePdf()
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

	def OnClearRanges(self, event) -> None:
		for i in range(self.__rangesList.GetCount()):
			idx = self.__rangesList.GetTopItem()
			self.__rangesList.Delete(idx)

		self.__clearRangesBtn.Disable()
		self.__removeRangeBtn.Disable()

	def __addRangesToWriter(self, writer, pages) -> None:
		pageIdx1 = pages[0] - 1
		pageIdx2 = pages[1] - 1

		pageRange = [pageIdx1] if pageIdx1 == pageIdx2 else [pageIdx1, pageIdx2]

		writer.append(self.__reader.path, pageRange)

	def __writeSinglePdf(self) -> None:
		writer = PdfWriter()

		for pages in self.__pdfPageRangeList:
			self.__addRangesToWriter(writer, pages)			
		
		writer.write(self.__pathToSavePdf)
		writer.close()

	def __writeMultiplePdf(self) -> None:
		for idx, pages in enumerate(self.__pdfPageRangeList):
			srcPath = os.path.dirname(self.__pathToSavePdf)
			srcFileName, srcSuffix = os.path.splitext(self.__pathToSavePdf)
			saveFileName = srcFileName + f"_{idx + 1}" + srcSuffix
			pathToSave = os.path.join(srcPath, saveFileName)

			writer = PdfWriter()

			self.__addRangesToWriter(writer, pages)

			writer.write(pathToSave)
			writer.close()

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

		self.__splitSaveModeRadio = wx.RadioBox(self, label="Split Mode", choices=["Single File", "Multiple Files"])
		controlsSizer.Add(self.__splitSaveModeRadio, flag=wx.LEFT | wx.BOTTOM, border=15)

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

		self.__clearRangesBtn = wx.Button(self, label="Clear Ranges", size=(150, 30))
		self.__clearRangesBtn.Disable()
		self.Bind(wx.EVT_BUTTON, self.OnClearRanges, self.__clearRangesBtn)
		controlsSizer.Add(self.__clearRangesBtn, flag=wx.ALIGN_RIGHT | wx.BOTTOM, border=15)

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

		self.__minPageSpinCtrl.SetRange(1, pages)
		self.__maxPageSpinCtrl.SetRange(1, pages)

		self.__minPageSpinCtrl.SetValue(1)
		self.__maxPageSpinCtrl.SetValue(2)