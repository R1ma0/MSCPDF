import wx

def getAppImagesList(width: int, height: int) -> dict:
	imgList = wx.ImageList(width, height)
	iconsFolder = r"icons"

	imgList.Add(wx.Bitmap(iconsFolder + r"\add.png"))       # 0
	imgList.Add(wx.Bitmap(iconsFolder + r"\remove.png"))    # 1
	imgList.Add(wx.Bitmap(iconsFolder + r"\clear.png"))     # 2
	imgList.Add(wx.Bitmap(iconsFolder + r"\process.png"))   # 3
	imgList.Add(wx.Bitmap(iconsFolder + r"\move_up.png"))   # 4
	imgList.Add(wx.Bitmap(iconsFolder + r"\move_down.png")) # 5
	imgList.Add(wx.Bitmap(iconsFolder + r"\metadata.png"))  # 6
	imgList.Add(wx.Bitmap(iconsFolder + r"\split.png"))     # 7
	imgList.Add(wx.Bitmap(iconsFolder + r"\merge.png"))     # 8
	imgList.Add(wx.Bitmap(iconsFolder + r"\app.png"))	    # 9

	return imgList