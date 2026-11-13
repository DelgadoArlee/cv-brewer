from core.errors import InvalidFileTypeError

PDF_SIGNATURE = b"%PDF-"


def verify_pdf_signature(content: bytes) -> None:
    if not content.startswith(PDF_SIGNATURE):
        raise InvalidFileTypeError("File content does not have a valid PDF signature.")
