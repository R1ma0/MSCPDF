import wx



class Utils:

	@staticmethod
	def addSeparator(
		parent: wx.Window, sizer: wx.BoxSizer, border: int = 0, flags=wx.EXPAND
	) -> None:
		separator = wx.StaticLine(parent)
		sizer.Add(separator, flag=flags, border=border)