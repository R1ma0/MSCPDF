import wx
from utils import Utils



def getAppImagesList(width: int, height: int) -> dict:

	def getPath(path) -> wx.Bitmap:
		return wx.Bitmap(Utils.getResourcePath(path))

	imgList = wx.ImageList(width, height)
	iconsFolder = r"icons"

	imgList.Add(getPath(iconsFolder + r"\add.png"))       # 0
	imgList.Add(getPath(iconsFolder + r"\remove.png"))    # 1
	imgList.Add(getPath(iconsFolder + r"\clear.png"))     # 2
	imgList.Add(getPath(iconsFolder + r"\process.png"))   # 3
	imgList.Add(getPath(iconsFolder + r"\move_up.png"))   # 4
	imgList.Add(getPath(iconsFolder + r"\move_down.png")) # 5
	imgList.Add(getPath(iconsFolder + r"\metadata.png"))  # 6
	imgList.Add(getPath(iconsFolder + r"\split.png"))     # 7
	imgList.Add(getPath(iconsFolder + r"\merge.png"))     # 8
	imgList.Add(getPath(iconsFolder + r"\app.png"))	      # 9

	return imgList