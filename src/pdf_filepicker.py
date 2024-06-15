import wx



class PdfFilepicker:

	def __init__(self, parent, orientation=wx.VERTICAL, size=wx.DefaultSize):
		self.__parent = parent
		self.__orientation = orientation
		self.__size = size

		self.__mainSizer = wx.BoxSizer(orientation)
		self.__alignValue = wx.ALIGN_CENTRE_VERTICAL if orientation is wx.HORIZONTAL else 0

		self.__createWidgets()

	def __createWidgets(self) -> None:
		filePickerLabel = wx.StaticText(
			self.__parent, 
			label="Select PDF file:"
		)
		self.__mainSizer.Add(filePickerLabel, flag=self.__alignValue)

		self.__filePicker = wx.FilePickerCtrl(
			self.__parent, 
			wildcard="PDF files (*.pdf)|*.pdf",
			message="Select PDF file",
			size=self.__size
		)
		self.__mainSizer.Add(self.__filePicker)

	def getSizer(self) -> wx.BoxSizer:
		return self.__mainSizer

	def getPdfPicker(self) -> wx.FilePickerCtrl:
		return self.__filePicker