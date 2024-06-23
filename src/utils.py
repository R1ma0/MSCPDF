import wx
import os



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