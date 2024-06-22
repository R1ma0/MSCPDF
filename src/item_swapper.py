import wx
from enum import Enum



class IdxSwapType(Enum):
	LEFT = 0
	RIGHT = 1



class ItemSwapper:
	"""
	Class that implements algorithms for element swap
	"""

	def listItemsSwap(self, lst: list, idxOne: int, idxTwo: int) -> list:
		"""
		Swaps list items and returns updated list

		Parameters
		----------
		lst : list
			List of elements
		idxOne : int
			Index of the first element
		idxTwo : int
			Index of the second element
		"""
		lst[idxOne], lst[idxTwo] = lst[idxTwo], lst[idxOne]

		return lst

	def listBoxItemsSwap(
		self, listBox: wx.ListBox, idxOne: int, idxTwo: int
	) -> wx.ListBox:
		"""
		Swaps wx.ListBox items and return updated ListBox

		Parameters
		----------
		listBox : wx.ListBox
			ListBox with elements
		idxOne : int
			Index of the first element
		idxTwo : int
			Index of the second element
		"""
		strOne = listBox.GetString(idxOne)
		strTwo = listBox.GetString(idxTwo)

		listBox.SetString(idxOne, strTwo)
		listBox.SetString(idxTwo, strOne)

		return listBox

	def swapListsItems(
		self, listBox: wx.ListBox, listIdx: list, idxOne: int, idxTwo: int
	) -> (wx.ListBox, list):
		"""
		Swaps elements in wx.ListBox and list with the same indexes.
		Uses methods: 'listItemsSwap' and 'listBoxItemsSwap'

		Parameters
		----------
		listBox : wx.ListBox
			ListBox with elements
		listIdx : list
			List of elements
		idxOne : int
			Index of the first element
		idxTwo : int
			Index of the second element
		"""
		listIdx = self.listItemsSwap(listIdx, idxOne, idxTwo)
		listBox = self.listBoxItemsSwap(listBox, idxOne, idxTwo)

		return listBox, listIdx

	def listBoxAndListIdxSwap(
		self, idxType: IdxSwapType, listBox: wx.ListBox, listIdx: list
	) -> (wx.ListBox, list):
		"""
		Perform items swap with boundaries overstepping check.
		Returns updated ListBox and list. Uses 'swapListItems' method

		Parameters
		----------
		idxType : IdxSwapType
			Is used to prevent overstepping the boundaries
		listBox : wx.ListBox
			ListBox with elements
		listIdx : list
			List of elements
		"""
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