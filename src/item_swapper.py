import wx
from enum import Enum



class IdxSwapType(Enum):
	LEFT = 0
	RIGHT = 1



class ItemSwapper:

	def listItemsSwap(self, lst: list, idxOne: int, idxTwo: int) -> list:
		lst[idxOne], lst[idxTwo] = lst[idxTwo], lst[idxOne]

		return lst

	def listBoxItemsSwap(
		self, listBox: wx.ListBox, idxOne: int, idxTwo: int
	) -> wx.ListBox:
		strOne = listBox.GetString(idxOne)
		strTwo = listBox.GetString(idxTwo)

		listBox.SetString(idxOne, strTwo)
		listBox.SetString(idxTwo, strOne)

		return listBox

	def swapListsItems(
		self, listBox: wx.ListBox, listIdx: list, idxOne: int, idxTwo: int
	) -> (wx.ListBox, list):
		listIdx = self.listItemsSwap(listIdx, idxOne, idxTwo)
		listBox = self.listBoxItemsSwap(listBox, idxOne, idxTwo)

		return listBox, listIdx

	def listBoxAndListIdxSwap(
		self, idxType: IdxSwapType, listBox: wx.ListBox, listIdx: list
	) -> (wx.ListBox, list):
		idxOne = listBox.GetSelection()

		if idxType == IdxSwapType.LEFT:
			idxTwo = idxOne - 1

			if idxTwo < 0:
				return
		elif idxType == IdxSwapType.RIGHT:
			idxTwo = idxOne + 1

			if idxTwo > listBox.GetCount() - 1:
				return
		else:
			return 

		listBox, listIdx = self.swapListsItems(listBox, listIdx, idxOne, idxTwo)

		listBox.SetSelection(idxTwo)

		return listBox, listIdx