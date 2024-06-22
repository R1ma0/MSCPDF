from dataclasses import dataclass



@dataclass
class PdfInfo:
	pages: str
	author: str
	creator: str
	producer: str
	subject: str
	title: str