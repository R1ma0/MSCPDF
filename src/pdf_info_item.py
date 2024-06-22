import wx
from constants import *



class PdfInfoItem:
	"""
	Creating a title and description for a metadata item from a PDF file
	"""

	def __init__(
		self, 
		parent: wx.Window, 
		label: str = "None", 
		text: str = "Empty"
	):
		"""
		Parameters
		----------
		parent : wx.Window
		label : str (default is "None")
			Metadata item title
		text : str (default is "None")
			Metadata item text
		"""
		self.__parent = parent
		self.__label = label
		self.__text = text

		self.__fontBold = wx.Font(12, wx.DEFAULT, wx.BOLD, wx.NORMAL)
		self.__fontNormal = wx.Font(12, wx.DEFAULT, wx.ITALIC, wx.NORMAL)

		self.__staticTextWrapWidth = WINDOW_WIDTH - 125

		self.__labelST = None
		self.__textST = None

		self.__createStaticText()

	@property
	def labelStatic(self) -> wx.StaticText:
		return self.__labelST

	@property
	def textStatic(self) -> wx.StaticText:
		return self.__textST

	@property
	def label(self) -> str:
		return self.__label

	@label.setter
	def label(self, value: str) -> None:
		self.__label = value
		self.__updateStaticText()

	@property
	def text(self) -> str:
		return self.__text

	@text.setter
	def text(self, value: str) -> None:
		self.__text = value
		self.__updateStaticText()

	def show(self, state: bool = True) -> None:
		self.__labelST.Show(state)
		self.__textST.Show(state)
	
	def __createStaticText(self) -> None:
		self.__labelST = wx.StaticText(
			self.__parent, label=self.__label, size=(100, 30)
		)
		self.__labelST.SetFont(self.__fontBold)
		self.__labelST.Wrap(self.__staticTextWrapWidth)

		self.__textST = wx.StaticText(self.__parent, label=self.__text)
		self.__textST.SetFont(self.__fontNormal)
		self.__textST.Wrap(self.__staticTextWrapWidth)

	def __updateStaticText(self) -> None:
		self.__labelST.SetLabel(self.__label)
		self.__textST.SetLabel(self.__text)

		self.__labelST.Wrap(self.__staticTextWrapWidth)
		self.__textST.Wrap(self.__staticTextWrapWidth)