import wx
from constants import *



class PdfInfoItem:

	def __init__(self, parent, label="None", data="Empty"):
		self.__parent = parent
		self.__label = label
		self.__data = data

		self.__fontBold = wx.Font(12, wx.DEFAULT, wx.BOLD, wx.NORMAL)
		self.__fontNormal = wx.Font(12, wx.DEFAULT, wx.ITALIC, wx.NORMAL)

		self.__staticTextWrapWidth = WINDOW_WIDTH - 125

		self.__labelST = None
		self.__dataST = None
		self.__createStaticText()

	@property
	def labelStatic(self) -> wx.StaticText:
		return self.__labelST

	@property
	def dataStatic(self) -> wx.StaticText:
		return self.__dataST

	@property
	def label(self) -> str:
		return self.__label

	@label.setter
	def label(self, value) -> None:
		self.__label = value
		self.__updateStaticText()

	@property
	def data(self) -> str:
		return self.__data

	@data.setter
	def data(self, value) -> None:
		self.__data = value
		self.__updateStaticText()
	
	def __createStaticText(self) -> None:
		self.__labelST = wx.StaticText(
			self.__parent, label=self.__label, size=(100, 30)
		)
		self.__labelST.SetFont(self.__fontBold)
		self.__labelST.Wrap(self.__staticTextWrapWidth)

		self.__dataST = wx.StaticText(self.__parent, label=self.__data)
		self.__dataST.SetFont(self.__fontNormal)
		self.__dataST.Wrap(self.__staticTextWrapWidth)

	def __updateStaticText(self) -> None:
		self.__labelST.SetLabel(self.__label)
		self.__dataST.SetLabel(self.__data)

		self.__labelST.Wrap(self.__staticTextWrapWidth)
		self.__dataST.Wrap(self.__staticTextWrapWidth)