import wx
import os
import sys



class Utils:

	@staticmethod
	def addSeparator(
		parent: wx.Window, sizer: wx.BoxSizer, border: int = 0, flags=wx.EXPAND
	) -> None:
		separator = wx.StaticLine(parent)
		sizer.Add(separator, flag=flags, border=border)

	@staticmethod
	def clearListBox(listBox: wx.ListBox) -> wx.ListBox:
		for i in range(listBox.GetCount()):
			idx = listBox.GetTopItem()
			listBox.Delete(idx)

	@staticmethod
	def isDirExist(path: str) -> bool:
		dirname = os.path.dirname(path)
		return os.path.isdir(dirname)

	@staticmethod
	def showSucsessfulSaveDialog(parent: wx.Window) -> None:
		dialogMessage = "File successfully saved!"
		dialogCaption = "PDF Read & Write Information!"
		dialogStyle = wx.OK_DEFAULT | wx.ICON_INFORMATION

		msgDialog = wx.MessageDialog(
			parent, 
			message=dialogMessage, 
			caption=dialogCaption,
			style=dialogStyle
		)
		msgDialog.ShowModal()

	@staticmethod
	def isListBoxItemSelect(listBox: wx.ListBox) -> bool:
		if listBox.GetSelection() == -1:
			return False

		return True

	@staticmethod
	def getResourcePath(relativePath: str) -> str:
		try:
			basePath = sys._MEIPAS
		except Exception:
			basePath = os.path.abspath(".")

		return os.path.join(basePath, relativePath)