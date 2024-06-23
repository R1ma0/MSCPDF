import wx
import os
from app_icons import *
from enum import Enum
from pdf_rw import PdfRW, SplitMode
from custom_file_picker import CustomFilePicker
from notebook_panel import NotebookPanel
from item_swapper import ItemSwapper, IdxSwapType
from utils import Utils



class RangeSpinType(Enum):
	MIN = 0
	MAX = 1



class PdfSplitPanel(wx.Panel, NotebookPanel):
	"""
	Panel containing actions for split PDF
	"""

	def __init__(self, parent: wx.Window):
		super(PdfSplitPanel, self).__init__(parent)
		NotebookPanel.__init__(self)

		self.__parent = parent
		self.__pdfRW = PdfRW()
		self.__pdfMeta = None
		self.__pathToSavePdf = None
		self.__pdfPageRangeList = []
		self.__rangesList = wx.ListBox(self)
		self.__margin = 15

		self.__createWidgets()

	def OnOpenPdfReadPath(self, event: wx.Event) -> None:
		self.__pdfRW.path = event.GetPath()
		
		try:
			self.__pdfMeta = self.__pdfRW.getMetadata()
		except FileNotFoundError:
			self.SetStatusBarText("The file specified for load was not found!")
		else:
			pages = int(self.__pdfMeta.pages)
			self.__totalPages.SetLabel(f"Total Pages: {pages}")

			self.__setMinMaxRanges(pages)
			self.__checkSavingConditions()

	def OnOpenPdfWritePath(self, event: wx.Event) -> None:
		self.__pathToSavePdf = event.GetPath()

		if not Utils.isDirExist(event.GetPath()):
			self.SetStatusBarText("The folder to be saved is incorrect!")
		else:
			self.SetStatusBarText("")

		self.__checkSavingConditions()

	def OnAddRange(self, event: wx.Event) -> None:
		minValue = self.__minPageSpinCtrl.GetValue()
		maxValue = self.__maxPageSpinCtrl.GetValue()

		if minValue != maxValue:
			rangeText = f"Pages {minValue} to {maxValue}"
			self.SetStatusBarText(f"Added pages {minValue} to {maxValue}")
		else:
			rangeText = f"Page {minValue}"
			self.SetStatusBarText(f"Added page {minValue}")

		self.__pdfPageRangeList.append([minValue, maxValue])

		lastItemIdx = self.__rangesList.GetCount()
		self.__rangesList.InsertItems([rangeText], lastItemIdx)

		self.__enableControlBtns()
		self.__checkSavingConditions()

	def OnRemoveRange(self, event: wx.Event) -> None:
		idx = self.__rangesList.GetSelection()

		if idx != -1:	
			minVal = self.__pdfPageRangeList[idx][0]
			maxVal = self.__pdfPageRangeList[idx][1]

			self.__rangesList.Delete(idx)
			self.__pdfPageRangeList.pop(idx)

			self.SetStatusBarText(f"Removed range pages {minVal} to {maxVal}")

		if self.__rangesList.GetCount() == 0:
			self.__enableControlBtns(False)

		self.__checkSavingConditions()

	def OnSavePdf(self, event: wx.Event) -> None:
		if self.__rangesList.GetCount() == 0:
			self.SetStatusBarText("Page ranges are not specified!")
			return

		selectedSplitMode = self.__spSaveMode.GetSelection()
		
		self.__pdfRW.writePagesToPDF(
			self.__pathToSavePdf, 
			self.__pdfPageRangeList, 
			SplitMode(selectedSplitMode)
		)

		Utils.showSucsessfulSaveDialog(self)

	def OnMinPageSpin(self, event: wx.Event) -> None:
		self.__checkRangeSpinValue(self.__maxPageSpinCtrl, RangeSpinType.MIN)

	def OnMaxPageSpin(self, event: wx.Event) -> None:
		self.__checkRangeSpinValue(self.__minPageSpinCtrl, RangeSpinType.MAX)

	def OnClearRanges(self, event: wx.Event) -> None:
		Utils.clearListBox(self.__rangesList)
		self.__checkSavingConditions()
		self.__enableControlBtns(False)
		self.SetStatusBarText("Range list cleared")

	def OnListItemMoveUp(self, event: wx.Event) -> None:
		if not Utils.isListBoxItemSelect(self.__rangesList):
			return

		ItemSwapper.listBoxAndListIdxSwap(
			IdxSwapType.LEFT, self.__rangesList, self.__pdfPageRangeList
		)

	def OnListItemMoveDown(self, event: wx.Event) -> None:
		if not Utils.isListBoxItemSelect(self.__rangesList):
			return

		ItemSwapper.listBoxAndListIdxSwap(
			IdxSwapType.RIGHT, self.__rangesList, self.__pdfPageRangeList
		)

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

	def __setMinMaxRanges(self, pages: int) -> None:
		self.__minPageSpinCtrl.SetRange(1, pages)
		self.__maxPageSpinCtrl.SetRange(1, pages)

		self.__minPageSpinCtrl.SetValue(1)
		self.__maxPageSpinCtrl.SetValue(2)

	def __createWidgets(self) -> None:
		"""
		Creates interface elements
		"""
		self.__mainSizer = wx.BoxSizer(wx.VERTICAL)
		self.__createFilePickers(self.__mainSizer)

		rngListAndBtnsSizer = wx.BoxSizer(wx.VERTICAL)
		self.__createRngListAndBtns(rngListAndBtnsSizer)

		rangesSizer = wx.BoxSizer(wx.HORIZONTAL)
		flags = wx.EXPAND | wx.BOTTOM | wx.LEFT
		rangesSizer.Add(
			rngListAndBtnsSizer, flag=flags, border=self.__margin, proportion=1
		)

		controlsSizer = wx.BoxSizer(wx.VERTICAL)

		flags = wx.EXPAND | wx.LEFT | wx.BOTTOM
		self.__spSaveMode = wx.RadioBox(
			self, label="Split Mode", choices=["Single File", "Multiple Files"]
		)
		controlsSizer.Add(self.__spSaveMode, flag=flags, border=self.__margin)

		flags = wx.LEFT | wx.BOTTOM
		self.__totalPages = wx.StaticText(self, label="PDF Total Pages: 0")
		controlsSizer.Add(self.__totalPages, flag=flags, border=self.__margin)

		self.__createPageRangeCtrls(controlsSizer)
		self.__createPagesControlButtons(controlsSizer)
		self.__createSavePDFButton(controlsSizer)
		self.__enableControlBtns(False)

		flags = wx.ALIGN_CENTER | wx.BOTTOM | wx.RIGHT
		rangesSizer.Add(
			controlsSizer, flag=flags, border=self.__margin, proportion=1
		)
		self.__mainSizer.Add(rangesSizer, flag=wx.EXPAND, proportion=1)

		self.__addPanelIcons()

		self.SetSizerAndFit(self.__mainSizer)

	def __createRngListAndBtns(self, sizer: wx.BoxSizer) -> None:
		size = (150, 30)

		flags = wx.EXPAND | wx.BOTTOM
		sizer.Add(
			self.__rangesList, flag=flags, border=self.__margin, proportion=1
		)

		rngControlBtnsSizer = wx.BoxSizer(wx.HORIZONTAL)

		self.__rngMoveUpBtn = wx.Button(self, label="Move Up", size=size)
		self.Bind(wx.EVT_BUTTON, self.OnListItemMoveUp, self.__rngMoveUpBtn)
		rngControlBtnsSizer.Add(
			self.__rngMoveUpBtn, flag=wx.RIGHT, border=self.__margin
		)

		self.__rngMoveDownBtn = wx.Button(self, label="Move Down", size=size)
		self.Bind(wx.EVT_BUTTON, self.OnListItemMoveDown, self.__rngMoveDownBtn)
		rngControlBtnsSizer.Add(self.__rngMoveDownBtn)

		sizer.Add(rngControlBtnsSizer, flag=wx.ALIGN_CENTRE_HORIZONTAL)

	def __createFilePickers(self, sizer: wx.BoxSizer) -> None:
		"""
		Creates file pickers for load and save paths
		"""
		pdfReadPicker = CustomFilePicker(
			self, 
			label="Select PDF file to read:", 
			msg="Select PDF file", 
			wildcard="PDF files (*.pdf)|*.pdf"
		)
		flags = wx.TOP | wx.EXPAND | wx.LEFT | wx.RIGHT
		sizer.Add(pdfReadPicker.getSizer(), flag=flags, border=self.__margin)
		self.Bind(
			wx.EVT_FILEPICKER_CHANGED, 
			self.OnOpenPdfReadPath, 
			pdfReadPicker.getPicker()
		)

		style = wx.FLP_SAVE | wx.FLP_OVERWRITE_PROMPT | wx.FLP_USE_TEXTCTRL
		pdfWritePicker = CustomFilePicker(
			self,
			label="Select path to save PDF:",
			msg="Enter filename to save",
			wildcard="PDF files (*.pdf)|*.pdf",
			pickerStyle=style
		)
		flags = wx.BOTTOM | wx.EXPAND | wx.LEFT | wx.RIGHT
		sizer.Add(pdfWritePicker.getSizer(), flag=flags, border=self.__margin)
		self.Bind(
			wx.EVT_FILEPICKER_CHANGED, 
			self.OnOpenPdfWritePath, 
			pdfWritePicker.getPicker()
		)

	def __createPageRangeCtrls(self, sizer: wx.BoxSizer) -> None:
		"""
		Creates page range controls 
		"""
		flags = wx.LEFT | wx.ALIGN_CENTRE_VERTICAL
		border = 15
		size = (150, 20)

		stBoxSizer = wx.StaticBoxSizer(wx.HORIZONTAL, self, label="Page Ranges")
		stBox = stBoxSizer.GetStaticBox()

		minPagesLabel = wx.StaticText(stBox, label="Pages")
		stBoxSizer.Add(minPagesLabel, flag=flags, border=self.__margin)

		self.__minPageSpinCtrl = wx.SpinCtrl(
			stBox, min=1, max=2, initial=1, size=size, style=wx.SP_WRAP
		)
		self.Bind(wx.EVT_SPINCTRL, self.OnMinPageSpin, self.__minPageSpinCtrl)
		stBoxSizer.Add(
			self.__minPageSpinCtrl, flag=wx.LEFT, border=self.__margin
		)

		maxPagesLabel = wx.StaticText(stBox, label="to")
		stBoxSizer.Add(maxPagesLabel, flag=flags, border=self.__margin)

		self.__maxPageSpinCtrl = wx.SpinCtrl(
			stBox, min=2, max=2, initial=2, size=size, style=wx.SP_WRAP
		)
		self.Bind(wx.EVT_SPINCTRL, self.OnMaxPageSpin, self.__maxPageSpinCtrl)
		stBoxSizer.Add(
			self.__maxPageSpinCtrl, flag=wx.LEFT, border=self.__margin
		)

		flags = wx.BOTTOM | wx.LEFT
		sizer.Add(stBoxSizer, flag=flags, border=self.__margin)

	def __createPagesControlButtons(self, sizer: wx.BoxSizer) -> None:
		flags = wx.BOTTOM
		size = (150, 30)

		topSizer = wx.BoxSizer(wx.HORIZONTAL)

		addRangeLabel = "Add Range"
		self.__addRangeBtn = wx.Button(self, label=addRangeLabel, size=size)
		self.Bind(wx.EVT_BUTTON, self.OnAddRange, self.__addRangeBtn)
		topSizer.Add(self.__addRangeBtn, flag=flags, border=self.__margin)

		rmRangeBtnLabel = "Remove Range"
		self.__rmRangeBtn = wx.Button(self, label=rmRangeBtnLabel, size=size)
		self.Bind(wx.EVT_BUTTON, self.OnRemoveRange, self.__rmRangeBtn)
		flags = flags | wx.LEFT
		topSizer.Add(self.__rmRangeBtn, flag=flags, border=self.__margin)

		flags = wx.LEFT | wx.ALIGN_CENTRE_HORIZONTAL
		sizer.Add(topSizer, flag=flags, border=self.__margin)

		clrRangesLabel = "Clear Ranges"
		self.__clrRangesBtn = wx.Button(self, label=clrRangesLabel, size=size)
		self.Bind(wx.EVT_BUTTON, self.OnClearRanges, self.__clrRangesBtn)
		flags = wx.BOTTOM | wx.ALIGN_CENTRE_HORIZONTAL
		sizer.Add(self.__clrRangesBtn, flag=flags, border=self.__margin)

	def __createSavePDFButton(self, sizer: wx.BoxSizer) -> None:
		size = (150, 30)

		Utils.addSeparator(self, sizer, self.__margin, wx.EXPAND | wx.LEFT)

		saveLabel = "Split"
		self.__saveBtn = wx.Button(self, label=saveLabel, size=size)
		self.Bind(wx.EVT_BUTTON, self.OnSavePdf, self.__saveBtn)
		flags = wx.ALIGN_CENTER | wx.TOP
		sizer.Add(self.__saveBtn, flag=flags, border=self.__margin)

	def __checkSavingConditions(self) -> None:
		srcPathNotNone = self.__pdfRW.path is not None
		savePathNotNone = self.__pathToSavePdf is not None
		isRangesNotEmpty = self.__pdfPageRangeList != []

		if savePathNotNone:
			isSaveDirExists = Utils.isDirExist(self.__pathToSavePdf)

		srcPathValid = srcPathNotNone and os.path.exists(self.__pdfRW.path)
		saveDirValid = savePathNotNone and isSaveDirExists

		isSaveCondition = srcPathValid and saveDirValid and isRangesNotEmpty
		isBtnEnable = True if isSaveCondition else False
		self.__saveBtn.Enable(isBtnEnable)

	def __enableControlBtns(self, state: bool = True) -> None:
		self.__saveBtn.Enable(state)
		self.__clrRangesBtn.Enable(state)
		self.__rmRangeBtn.Enable(state)
		self.__rngMoveUpBtn.Enable(state)
		self.__rngMoveDownBtn.Enable(state)

	def __addPanelIcons(self) -> None:
		iconsBtmp = getAppImagesList(24, 24)

		buttonsAndIcons = [
			[self.__addRangeBtn, iconsBtmp.GetBitmap(0)],
			[self.__rmRangeBtn, iconsBtmp.GetBitmap(1)],
			[self.__clrRangesBtn, iconsBtmp.GetBitmap(2)],
			[self.__saveBtn, iconsBtmp.GetBitmap(3)],
			[self.__rngMoveUpBtn, iconsBtmp.GetBitmap(4)],
			[self.__rngMoveDownBtn, iconsBtmp.GetBitmap(5)]
		]

		for items in buttonsAndIcons:
			items[0].SetBitmap(items[1])