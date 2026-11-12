import pytest

from core.errors import InvalidFileTypeError
from core.validation.file_validation import verify_pdf_signature


def test_verify_pdf_signature_accepts_pdf_bytes() -> None:
    verify_pdf_signature(b"%PDF-1.7\ncontent")


def test_verify_pdf_signature_rejects_non_pdf_bytes() -> None:
    with pytest.raises(InvalidFileTypeError, match="PDF signature"):
        verify_pdf_signature(b"plain text")


def test_verify_pdf_signature_rejects_empty_content() -> None:
    with pytest.raises(InvalidFileTypeError):
        verify_pdf_signature(b"")
