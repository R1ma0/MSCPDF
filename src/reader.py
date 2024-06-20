from pypdf import PdfReader
from pdf_info import PdfInfo



class Reader:
	"""
	A class for reading and processing PDF file
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