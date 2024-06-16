import wx



class CustomFilepicker:

	def __init__(
		self, 
		parent, 
		orientation=wx.VERTICAL, 
		size=wx.DefaultSize, 
		label="", 
		msg="", 
		wildcard="",
		pickerStyle=wx.FLP_DEFAULT_STYLE 
	):
		self.__parent = parent
		self.__orientation = orientation
		self.__size = size
		self.__label = label
		self.__pickerMessage = msg
		self.__pickerWildcard = wildcard
		self.__pickerStyle = pickerStyle

		self.__mainSizer = wx.BoxSizer(orientation)
		self.__alignValue = wx.ALIGN_CENTRE_VERTICAL if orientation is wx.HORIZONTAL else 0

		self.__createWidgets()

	def __createWidgets(self) -> None:
		filePickerLabel = wx.StaticText(
			self.__parent, 
			label=self.__label
		)
		self.__mainSizer.Add(filePickerLabel, flag=self.__alignValue | wx.EXPAND)

		self.__filePicker = wx.FilePickerCtrl(
			self.__parent, 
			wildcard=self.__pickerWildcard,
			message=self.__pickerMessage,
			size=self.__size,
			style=self.__pickerStyle
		)
		self.__mainSizer.Add(self.__filePicker, flag=wx.EXPAND)

	def getSizer(self) -> wx.BoxSizer:
		return self.__mainSizer

	def getPicker(self) -> wx.FilePickerCtrl:
		return self.__filePicker