import os
from enum import Enum
from pypdf import PdfReader, PdfWriter
from pdf_info import PdfInfo



class SplitMode(Enum):
	SINGLE = 0
	MULTIPLE = 1



class PdfRW:
	"""
	A class for reading, writing and processing PDF file
	"""
	def __init__(self, pdfPath: str = None):
		"""
		Parameters
		----------
		pdfPath : str (default is None)
			Path to PDF file
		"""
		self.__pdfPath = pdfPath

	@property
	def path(self) -> str:
		"""
		Return the path to PDF file
		"""
		return self.__pdfPath
	
	@path.setter
	def path(self, value: str) -> None:
		"""
		Sets the path to PDF file

		Parameters
		----------
		value : str
			Path to PDF file

		"""
		self.__pdfPath = value

	def getMetadata(self) -> PdfInfo:
		"""
		Returns object of class PdfInfo with PDF metadata
		"""
		meta = None
		reader = None

		if self.__pdfPath is not None:
			try:
				reader = PdfReader(self.__pdfPath)
			except FileNotFoundError:
				raise
			else:
				meta = reader.metadata

		pages = None if reader is None else str(len(reader.pages))
		author = None if meta is None else meta.author
		creator = None if meta is None else meta.creator
		producer = None if meta is None else meta.producer
		subject = None if meta is None else meta.subject
		title = None if meta is None else meta.title

		return PdfInfo(pages, author, creator, producer, subject, title)

	def writePagesToPDF(
		self, path: str, pageRanges: list, mode: SplitMode
	) -> None:
		if mode == SplitMode.SINGLE:
			self.writePagesToSinglePDF(path, pageRanges)

		if mode == SplitMode.MULTIPLE:
			self.writePagesToMultiplePDF(path, pageRanges)

	def writePagesToSinglePDF(self, path: str, pageRanges: list) -> None:
		"""
		Writing selected ranges to a single PDF file
		"""
		writer = PdfWriter()

		for pages in pageRanges:
			self.__addRangesToWriter(writer, pages)			
		
		writer.write(path)
		writer.close()

	def writePagesToMultiplePDF(self, path: str, pageRanges: list) -> None:
		"""
		Writing selected ranges to multiple PDF files
		"""
		for idx, pages in enumerate(pageRanges):
			srcPath = os.path.dirname(path)
			srcFileName, srcSuffix = os.path.splitext(path)
			saveFileName = srcFileName + f"_{idx + 1}" + srcSuffix
			pathToSave = os.path.join(srcPath, saveFileName)

			writer = PdfWriter()

			self.__addRangesToWriter(writer, pages)

			writer.write(pathToSave)
			writer.close()

	def mergePDFFiles(self, paths: list) -> None:
		merger = PdfWriter()

		for path in paths:
			merger.append(path)

		merger.write(self.__pdfPath)
		merger.close()

	def __addRangesToWriter(self, writer: PdfWriter, pages: list) -> None:
		pageIdx1 = pages[0] - 1
		pageIdx2 = pages[1] - 1

		pageRange = [pageIdx1] if pageIdx1 == pageIdx2 else [pageIdx1, pageIdx2]

		writer.append(self.__pdfPath, pageRange)