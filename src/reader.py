from pypdf import PdfReader
from pdf_info import PdfInfo



class Reader:

	def __init__(self, pdfPath=None):
		self.__pdfPath = pdfPath

	@property
	def path(self) -> str:
		return self.__pdfPath
	
	@path.setter
	def path(self, value) -> None:
		self.__pdfPath = value

	def getMetadata(self) -> PdfInfo:
		meta = None
		reader = None

		if self.__pdfPath is not None:
			reader = PdfReader(self.__pdfPath)
			meta = reader.metadata

		pages = None if reader is None else str(len(reader.pages))
		author = None if meta is None else meta.author
		creator = None if meta is None else meta.creator
		producer = None if meta is None else meta.producer
		subject = None if meta is None else meta.subject
		title = None if meta is None else meta.title

		return PdfInfo(pages, author, creator, producer, subject, title)