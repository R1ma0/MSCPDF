from dataclasses import dataclass

@dataclass
class PdfInfo:
	pages: int
	author: str
	creator: str
	producer: str
	subject: str
	title: str