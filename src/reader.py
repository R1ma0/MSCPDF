from pypdf import PdfReader
from pdf_info import PdfInfo



class Reader:

	def __init__(self, pdfPath):
		self.__pdfPath = pdfPath
		self.__pdfMetadata = self.__getPdfMetadata(pdfPath)

	@property
	def getMetadata(self):
		return self.__pdfMetadata

	def __getPdfMetadata(self, path) -> PdfInfo:
		reader = PdfReader(path)
		meta = reader.metadata

		pages = str(len(reader.pages))
		author = "Empty" if meta is None else meta.author
		creator = "Empty" if meta is None else meta.creator
		producer = "Empty" if meta is None else meta.producer
		subject = "Empty" if meta is None else meta.subject
		title = "Empty" if meta is None else meta.title

		return PdfInfo(pages, author, creator, producer, subject, title)