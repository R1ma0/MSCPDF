import wx



class NotebookPanel:

	def __init__(self, statusBar: wx.StatusBar = None):
		self.__statusBar = statusBar

	def SetStatusBar(self, statusBar: wx.StatusBar) -> None:
		self.__statusBar = statusBar

	def SetStatusBarText(self, text: str) -> None:
		if self.__statusBar is not None:
			self.__statusBar.SetStatusText(text)

	def IsStatusBarSet(self) -> bool:
		return False if self.__statusBar is None else True