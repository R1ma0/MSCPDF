import wx



def listItemsSwap(lst: list, idxOne: int, idxTwo: int) -> list:
	lst[idxOne], lst[idxTwo] = lst[idxTwo], lst[idxOne]

	return lst

def listBoxItemsSwap(lstBox: wx.ListBox, idxOne: int, idxTwo: int) -> wx.ListBox:
	strOne = lstBox.GetString(idxOne)
	strTwo = lstBox.GetString(idxTwo)

	lstBox.SetString(idxOne, strTwo)
	lstBox.SetString(idxTwo, strOne)

	return lstBox

def swapListsItems(
	lst: list, lstBox: wx.ListBox, idxOne: int, idxTwo: int
) -> (list, wx.ListBox):
	lst = listItemsSwap(lst, idxOne, idxTwo)
	lstBox = listBoxItemsSwap(lstBox, idxOne, idxTwo)

	return lst, lstBox