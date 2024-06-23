import wx
from pathlib import Path
from pdf_rw import PdfRW
from notebook_panel import NotebookPanel
from custom_file_picker import CustomFilePicker
from item_swapper import ItemSwapper, IdxSwapType
from utils import Utils



class PdfMergePanel(wx.Panel, NotebookPanel):
	"""
	"""

	def __init__(self, parent: wx.Window):
		super(PdfMergePanel, self).__init__(parent)
		NotebookPanel.__init__(self)

		self.__parent = parent
		self.__pdfRW = PdfRW()
		self.__itemSwapper = ItemSwapper()
		self.__pdfPathList = []
		self.__margin = 15

		self.__createWidgets()

	def OnAddPathToSave(self, event: wx.Event) -> None:
		self.__pdfRW.path = event.GetPath()

		if not Utils.isDirExist(event.GetPath()):
			self.SetStatusBarText("The folder to be saved is incorrect!")
		else:
			self.SetStatusBarText("")

	def OnAddBtn(self, event: wx.Event) -> None:
		with wx.FileDialog(
			self, 
			message="Select PDF files", 
			wildcard="PDF files (*.pdf)|*.pdf",
			style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE
		) as fileDialog:
			if fileDialog.ShowModal() == wx.ID_CANCEL:
				return

			pathList = fileDialog.GetPaths()
			
			Utils.clearListBox(self.__pdfTitlesBox)
			self.__addPathToListBox(pathList)
			self.__pdfPathList = pathList

	def OnRemoveBtn(self, event: wx.Event) -> None:
		idx = self.__pdfTitlesBox.GetSelection()

		if idx != -1:
			rmItemTxt = self.__pdfTitlesBox.GetString(idx)
			self.SetStatusBarText(f"Removed '{rmItemTxt}'")

			self.__pdfTitlesBox.Delete(idx)
			self.__pdfPathList.pop(idx)

		if self.__pdfTitlesBox.GetCount() == 0:
			pass

	def OnClearBtn(self, event: wx.Event) -> None:
		Utils.clearListBox(self.__pdfTitlesBox)
		self.SetStatusBarText("File list cleared")

	def OnMoveUpBtn(self, event: wx.Event) -> None:
		ItemSwapper.listBoxAndListIdxSwap(
			IdxSwapType.LEFT, self.__pdfTitlesBox, self.__pdfPathList 
		)

	def OnMoveDownBtn(self, event: wx.Event) -> None:
		ItemSwapper.listBoxAndListIdxSwap(
			IdxSwapType.RIGHT, self.__pdfTitlesBox, self.__pdfPathList
		)

	def OnSaveBtn(self, event: wx.Event) -> None:
		self.__pdfRW.mergePDFFiles(self.__pdfPathList)

	def __createWidgets(self) -> None:
		"""
		Creates interface elements
		"""
		self.__mainSizer = wx.BoxSizer(wx.VERTICAL)

		self.__createSavePathPicker(self.__mainSizer)

		contentSizer = wx.BoxSizer(wx.HORIZONTAL)

		self.__createPdfTitlesListBox(contentSizer)
		self.__createControlsButtons(contentSizer)

		flags = wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM
		self.__mainSizer.Add(
			contentSizer, flag=flags, border=self.__margin, proportion=1
		)

		self.SetSizerAndFit(self.__mainSizer)

	def __createSavePathPicker(self, sizer: wx.BoxSizer) -> None:
		style = wx.FLP_SAVE | wx.FLP_OVERWRITE_PROMPT | wx.FLP_USE_TEXTCTRL
		pdfWritePicker = CustomFilePicker(
			self,
			label="Select path to save PDF:",
			msg="Enter filename to save",
			wildcard="PDF files (*.pdf)|*.pdf",
			pickerStyle=style
		)
		flags = wx.EXPAND | wx.ALL
		self.Bind(
			wx.EVT_FILEPICKER_CHANGED,
			self.OnAddPathToSave,
			pdfWritePicker.getPicker()
		)
		sizer.Add(pdfWritePicker.getSizer(), flag=flags, border=self.__margin) 

	def __createPdfTitlesListBox(self, sizer: wx.BoxSizer) -> None:
		self.__pdfTitlesBox = wx.ListBox(self)
		sizer.Add(self.__pdfTitlesBox, flag=wx.EXPAND, proportion=1)

	def __createControlsButtons(self, sizer: wx.BoxSizer) -> None:
		size = (150, 30)
		botTopFlags = wx.BOTTOM | wx.TOP

		btnSizer = wx.BoxSizer(wx.VERTICAL)

		self.__addBtn = wx.Button(self, label="Add", size=size)
		self.Bind(wx.EVT_BUTTON, self.OnAddBtn, self.__addBtn)
		btnSizer.Add(self.__addBtn, flag=wx.BOTTOM, border=self.__margin)

		self.__rmBtn = wx.Button(self, label="Remove", size=size)
		self.Bind(wx.EVT_BUTTON, self.OnRemoveBtn, self.__rmBtn)
		btnSizer.Add(self.__rmBtn, flag=wx.BOTTOM, border=self.__margin)

		self.__clearBtn = wx.Button(self, label="Clear", size=size)
		self.Bind(wx.EVT_BUTTON, self.OnClearBtn, self.__clearBtn)
		btnSizer.Add(self.__clearBtn, flag=wx.BOTTOM, border=self.__margin)

		Utils.addSeparator(self, btnSizer)

		self.__moveUpBtn = wx.Button(self, label="Move Up", size=size)
		self.Bind(wx.EVT_BUTTON, self.OnMoveUpBtn, self.__moveUpBtn)
		btnSizer.Add(self.__moveUpBtn, flag=botTopFlags, border=self.__margin)

		self.__moveDownBtn = wx.Button(self, label="Move Down", size=size)
		self.Bind(wx.EVT_BUTTON, self.OnMoveDownBtn, self.__moveDownBtn)
		btnSizer.Add(self.__moveDownBtn, flag=wx.BOTTOM, border=self.__margin)

		Utils.addSeparator(self, btnSizer)

		self.__saveBtn = wx.Button(self, label="Merge", size=size)
		self.Bind(wx.EVT_BUTTON, self.OnSaveBtn, self.__saveBtn)
		btnSizer.Add(self.__saveBtn, flag=botTopFlags, border=self.__margin)

		flags = wx.LEFT | wx.ALIGN_CENTER
		sizer.Add(btnSizer, flag=flags, border=self.__margin)

	def __addPathToListBox(self, paths: list) -> None:
		fileNames = self.__getNameListFromPaths(paths)
		self.__pdfTitlesBox.InsertItems(fileNames, 0)

	def __getNameListFromPaths(self, paths: list) -> list:
		return list(map(self.__getFileNameFromPath, paths))

	def __getFileNameFromPath(self, path: str) -> str:
		return Path(path).stem