import io

import pdfplumber
from pypdf import PdfReader

from core.errors import InvalidFileTypeError, InvalidPdfError, UnreadableContentError

PDF_SIGNATURE = b"%PDF-"


def _open_pdf_reader(content: bytes) -> PdfReader:
    return PdfReader(io.BytesIO(content))


def _validate_encryption(reader: PdfReader) -> None:
    if reader.is_encrypted:
        raise InvalidPdfError("PDF is encrypted or password-protected.")


def _validate_pages(reader: PdfReader) -> None:
    try:
        page_count = len(reader.pages)
    except Exception as exc:
        raise InvalidPdfError("PDF page structure is invalid.") from exc

    if page_count == 0:
        raise InvalidPdfError("PDF does not contain any pages.")


def _extract_page_texts(content: bytes) -> list[str]:
    with pdfplumber.open(io.BytesIO(content)) as pdf:
        return [page.extract_text() or "" for page in pdf.pages]


def verify_pdf_signature(content: bytes) -> None:
    if not content.startswith(PDF_SIGNATURE):
        raise InvalidFileTypeError("File content does not have a valid PDF signature.")


def validate_pdf(content: bytes) -> None:
    try:
        reader = _open_pdf_reader(content)
    except Exception as exc:
        raise InvalidPdfError("PDF structure is invalid.") from exc

    _validate_encryption(reader)
    _validate_pages(reader)


def extract_pdf_text(content: bytes) -> str:
    try:
        page_texts = _extract_page_texts(content)
    except Exception as exc:
        raise UnreadableContentError("PDF text could not be extracted.") from exc

    text = "\n".join(page_texts).strip()
    if not text:
        raise UnreadableContentError("PDF does not contain readable text.")

    return text
