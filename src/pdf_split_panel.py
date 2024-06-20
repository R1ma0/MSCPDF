import wx
import os
from enum import Enum
from pypdf import PdfWriter
from reader import Reader
from custom_file_picker import CustomFilePicker



class SplitMode(Enum):
	SINGLE = 0
	MULTIPLE = 1

class RangeSpinType(Enum):
	MIN = 0
	MAX = 1



class PdfSplitPanel(wx.Panel):
	"""
	Panel containing actions for split PDF
	"""

	def __init__(self, parent: wx.Window):
		super(PdfSplitPanel, self).__init__(parent)

		self.__parent = parent
		self.__reader = Reader()
		self.__pdfMeta = None
		self.__pathToSavePdf = None
		self.__pdfPageRangeList = []
		self.__rangesList = wx.ListBox(self)

		self.__createWidgets()

	def OnOpenPdfReadPath(self, event: wx.Event) -> None:
		self.__reader.path = event.GetPath()
		self.__pdfMeta = self.__reader.getMetadata()

		pages = int(self.__pdfMeta.pages)
		self.__pagesStaticText.SetLabel(f"Total Pages: {pages}")

		self.__setMinMaxRanges()

	def OnOpenPdfWritePath(self, event: wx.Event) -> None:
		self.__pathToSavePdf = event.GetPath()

	def OnAddRange(self, event: wx.Event) -> None:
		# TODO: Disable if src and save paths not set
		minValue = self.__minPageSpinCtrl.GetValue()
		maxValue = self.__maxPageSpinCtrl.GetValue()

		if minValue != maxValue:
			rangeText = f"Pages {minValue} to {maxValue}"
		else:
			rangeText = f"Page {minValue}"

		self.__pdfPageRangeList.append([minValue, maxValue])

		lastItemIdx = self.__rangesList.GetCount()
		self.__rangesList.InsertItems([rangeText], lastItemIdx)

		self.__rmRangeBtn.Enable()
		self.__clrRangesBtn.Enable()

	def OnRemoveRange(self, event: wx.Event) -> None:
		if self.__rangesList.GetSelection() != -1:
			idx = self.__rangesList.GetSelection()
			self.__rangesList.Delete(idx)
			self.__pdfPageRangeList.pop(idx)

		if self.__rangesList.GetCount() == 0:
			self.__rmRangeBtn.Disable()
			self.__clrRangesBtn.Disable()

	def OnSavePdf(self, event: wx.Event) -> None:
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

	def OnMinPageSpin(self, event: wx.Event) -> None:
		self.__checkRangeSpinValue(self.__maxPageSpinCtrl, RangeSpinType.MIN)

	def OnMaxPageSpin(self, event: wx.Event) -> None:
		self.__checkRangeSpinValue(self.__minPageSpinCtrl, RangeSpinType.MAX)

	def OnClearRanges(self, event: wx.Event) -> None:
		for i in range(self.__rangesList.GetCount()):
			idx = self.__rangesList.GetTopItem()
			self.__rangesList.Delete(idx)

		self.__clrRangesBtn.Disable()
		self.__rmRangeBtn.Disable()

	def __checkRangeSpinValue(
		self, 
		spin: wx.SpinCtrl, 
		rangeType: RangeSpinType=RangeSpinType.MAX
	) -> None:
		"""
		Performs validation of range input items
		"""
		minValue = self.__minPageSpinCtrl.GetValue()
		maxValue = self.__maxPageSpinCtrl.GetValue()

		newValue = maxValue

		if rangeType == RangeSpinType.MIN:
			newValue = minValue

		if minValue >= maxValue:
			spin.SetValue(newValue)

	def __setMinMaxRanges(self) -> None:
		pages = int(self.__pdfMeta.pages)

		self.__minPageSpinCtrl.SetRange(1, pages)
		self.__maxPageSpinCtrl.SetRange(1, pages)

		self.__minPageSpinCtrl.SetValue(1)
		self.__maxPageSpinCtrl.SetValue(2)

	def __addRangesToWriter(self, writer: PdfWriter, pages: list) -> None:
		pageIdx1 = pages[0] - 1
		pageIdx2 = pages[1] - 1

		pageRange = [pageIdx1] if pageIdx1 == pageIdx2 else [pageIdx1, pageIdx2]

		writer.append(self.__reader.path, pageRange)

	def __writeSinglePdf(self) -> None:
		"""
		Writing selected ranges to a single PDF file
		"""
		writer = PdfWriter()

		for pages in self.__pdfPageRangeList:
			self.__addRangesToWriter(writer, pages)			
		
		writer.write(self.__pathToSavePdf)
		writer.close()

	def __writeMultiplePdf(self) -> None:
		"""
		Writing selected ranges to multiple PDF files
		"""
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
		"""
		Creates interface elements
		"""
		border = 15

		self.__mainSizer = wx.BoxSizer(wx.VERTICAL)
		self.__createFilePickers(self.__mainSizer)

		rangesSizer = wx.BoxSizer(wx.HORIZONTAL)
		flags = wx.EXPAND | wx.BOTTOM
		rangesSizer.Add(
			self.__rangesList, flag=flags, border=border, proportion=1
		)

		controlsSizer = wx.BoxSizer(wx.VERTICAL)

		flags = wx.LEFT | wx.BOTTOM
		self.__pagesStaticText = wx.StaticText(self, label="Total Pages: 0")
		controlsSizer.Add(self.__pagesStaticText, flag=flags, border=border)

		self.__splitSaveModeRadio = wx.RadioBox(
			self, label="Split Mode", choices=["Single File", "Multiple Files"]
		)
		controlsSizer.Add(self.__splitSaveModeRadio, flag=flags, border=border)

		self.__createPageRangeCtrls(controlsSizer)
		self.__createControlButtons(controlsSizer)

		flags = wx.ALIGN_BOTTOM | wx.BOTTOM
		rangesSizer.Add(controlsSizer, flag=flags, border=border, proportion=1)
		self.__mainSizer.Add(rangesSizer, flag=wx.EXPAND, proportion=1)

		self.SetSizerAndFit(self.__mainSizer)

	def __createFilePickers(self, sizer: wx.BoxSizer) -> None:
		"""
		Creates file pickers for load and save paths
		"""
		border = 15

		pdfReadPath = CustomFilePicker(
			self, 
			label="Select PDF file to read:", 
			msg="Select PDF file", 
			wildcard="PDF files (*.pdf)|*.pdf"
		)
		flags = wx.TOP | wx.EXPAND
		sizer.Add(pdfReadPath.getSizer(), flag=flags, border=border)
		self.Bind(
			wx.EVT_FILEPICKER_CHANGED, 
			self.OnOpenPdfReadPath, 
			pdfReadPath.getPicker()
		)

		style = wx.FLP_SAVE | wx.FLP_OVERWRITE_PROMPT | wx.FLP_USE_TEXTCTRL
		pdfWritePath = CustomFilePicker(
			self,
			label="Select path to save PDF:",
			msg="Enter filename to save",
			wildcard="PDF files (*.pdf)|*.pdf",
			pickerStyle=style
		)
		flags = wx.BOTTOM | wx.EXPAND
		sizer.Add(pdfWritePath.getSizer(), flag=flags, border=border)
		self.Bind(
			wx.EVT_FILEPICKER_CHANGED, 
			self.OnOpenPdfWritePath, 
			pdfWritePath.getPicker()
		)

	def __createPageRangeCtrls(self, sizer: wx.BoxSizer) -> None:
		"""
		Creates page range controls 
		"""
		flags = wx.LEFT | wx.ALIGN_CENTRE_VERTICAL
		border = 15
		size = (150, 20)

		pagesRangeSizer = wx.BoxSizer(wx.HORIZONTAL)

		minPagesLabel = wx.StaticText(self, label="Pages")
		pagesRangeSizer.Add(minPagesLabel, flag=flags, border=border)

		self.__minPageSpinCtrl = wx.SpinCtrl(
			self, min=1, max=2, initial=1, size=size, style=wx.SP_WRAP
		)
		self.Bind(wx.EVT_SPINCTRL, self.OnMinPageSpin, self.__minPageSpinCtrl)
		pagesRangeSizer.Add(self.__minPageSpinCtrl, flag=wx.LEFT, border=border)

		maxPagesLabel = wx.StaticText(self, label="to")
		pagesRangeSizer.Add(maxPagesLabel, flag=flags, border=border)

		self.__maxPageSpinCtrl = wx.SpinCtrl(
			self, min=2, max=2, initial=2, size=size, style=wx.SP_WRAP
		)
		self.Bind(wx.EVT_SPINCTRL, self.OnMaxPageSpin, self.__maxPageSpinCtrl)
		pagesRangeSizer.Add(self.__maxPageSpinCtrl, flag=wx.LEFT, border=border)

		sizer.Add(pagesRangeSizer, flag=wx.BOTTOM, border=border)

	def __createControlButtons(self, sizer: wx.BoxSizer) -> None:
		flags = wx.ALIGN_RIGHT | wx.BOTTOM
		border = 15
		size = (150, 30)

		addRangeLabel = "Add Range"
		addRangeBtn = wx.Button(self, label=addRangeLabel, size=size)
		self.Bind(wx.EVT_BUTTON, self.OnAddRange, addRangeBtn)
		sizer.Add(addRangeBtn, flag=flags, border=border)

		rmRangeBtnLabel = "Remove Range"
		self.__rmRangeBtn = wx.Button(self, label=rmRangeBtnLabel, size=size)
		self.__rmRangeBtn.Disable()
		self.Bind(wx.EVT_BUTTON, self.OnRemoveRange, self.__rmRangeBtn)
		sizer.Add(self.__rmRangeBtn, flag=flags, border=border)

		clrRangesLabel = "Clear Ranges"
		self.__clrRangesBtn = wx.Button(self, label=clrRangesLabel, size=size)
		self.__clrRangesBtn.Disable()
		self.Bind(wx.EVT_BUTTON, self.OnClearRanges, self.__clrRangesBtn)
		sizer.Add(self.__clrRangesBtn, flag=flags, border=border)

		saveLabel = "Save PDF"
		saveBtn = wx.Button(self, label=saveLabel, size=size)
		self.Bind(wx.EVT_BUTTON, self.OnSavePdf, saveBtn)
		sizer.Add(saveBtn, flag=wx.ALIGN_RIGHT)