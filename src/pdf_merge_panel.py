import wx
import os
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
		self.__pathToSavePdf = None
		self.__pdfList = []
		self.__margin = 15

		self.__createWidgets()

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
		sizer.Add(pdfWritePicker.getSizer(), flag=flags, border=self.__margin) 

	def __createPdfTitlesListBox(self, sizer: wx.BoxSizer) -> None:
		self.__pdfTitlesBox = wx.ListBox(self)
		sizer.Add(self.__pdfTitlesBox, flag=wx.EXPAND, proportion=1)

	def __createControlsButtons(self, sizer: wx.BoxSizer) -> None:
		size = (150, 30)

		btnSizer = wx.BoxSizer(wx.VERTICAL)

		addBtn = wx.Button(self, label="Add", size=size)
		btnSizer.Add(addBtn, flag=wx.BOTTOM, border=self.__margin)

		rmBtn = wx.Button(self, label="Remove", size=size)
		btnSizer.Add(rmBtn, flag=wx.BOTTOM, border=self.__margin)

		clearBtn = wx.Button(self, label="Clear", size=size)
		btnSizer.Add(clearBtn, flag=wx.BOTTOM, border=self.__margin)

		Utils.addSeparator(self, btnSizer)

		moveUpBtn = wx.Button(self, label="Move Up", size=size)
		btnSizer.Add(moveUpBtn, flag=wx.BOTTOM | wx.TOP, border=self.__margin)

		moveDownBtn = wx.Button(self, label="Move Down", size=size)
		btnSizer.Add(moveDownBtn, flag=wx.BOTTOM, border=self.__margin)

		Utils.addSeparator(self, btnSizer)

		saveBtn = wx.Button(self, label="Merge", size=size)
		btnSizer.Add(saveBtn, flag=wx.BOTTOM | wx.TOP, border=self.__margin)

		flags = wx.LEFT | wx.ALIGN_CENTER
		sizer.Add(btnSizer, flag=flags, border=self.__margin)