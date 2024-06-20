import wx



class CustomFilePicker:
	"""
	Implementation of the file picker with label

	"""
	def __init__(
		self, 
		parent: wx.Window, 
		orientation: int = wx.VERTICAL, 
		size: wx.Size = wx.DefaultSize, 
		label: str = "", 
		msg: str = "", 
		wildcard: str = "",
		pickerStyle: int = wx.FLP_DEFAULT_STYLE 
	):
		"""
		Parameters
		----------
		parent: wx.Window
		orientation: int (default is wx.VERTICAL)
		size: wx.Size (default is wx.DefaultSize)
			Size of the picker
		label: str (default is "")
			Postscript to picker (default is "")
		msg: str (default is "")
			File picker window message
		wildcard: str (default is "")
		pickerStyle: int (default is wx.FLP_DEFAULT_STYLE)
		"""
		self.__parent = parent
		self.__orientation = orientation
		self.__size = size
		self.__label = label
		self.__pickerMessage = msg
		self.__pickerWildcard = wildcard
		self.__pickerStyle = pickerStyle

		self.__createWidgets()

	def getSizer(self) -> wx.BoxSizer:
		"""
		Returns sizer for storage file picker and label
		"""
		return self.__mainSizer

	def getPicker(self) -> wx.FilePickerCtrl:
		"""
		Returns FilePickerCtrl object
		"""
		return self.__filePicker

	def __createWidgets(self) -> None:
		"""
		Creates interface elements
		"""
		self.__mainSizer = wx.BoxSizer(self.__orientation)

		isHorizontal = self.__orientation is wx.HORIZONTAL
		alignValue = wx.ALIGN_CENTRE_VERTICAL if isHorizontal else 0

		self.__createFilePickerLabel(alignValue)
		self.__createFilePicker()

	def __createFilePickerLabel(self, align: int) -> None:
		"""
		Creates label for file picker

		Parameters
		----------
		alig: int
			Label alignment
		"""
		filePickerLabel = wx.StaticText(
			self.__parent, 
			label=self.__label
		)
		self.__mainSizer.Add(filePickerLabel, flag=align | wx.EXPAND)

	def __createFilePicker(self) -> None:
		self.__filePicker = wx.FilePickerCtrl(
			self.__parent, 
			wildcard=self.__pickerWildcard,
			message=self.__pickerMessage,
			size=self.__size,
			style=self.__pickerStyle
		)
		self.__mainSizer.Add(self.__filePicker, flag=wx.EXPAND)