import pytest

from core.errors import InvalidPdfError, UnreadableContentError
from core.modules.pdf_processing import extract_pdf_text, validate_pdf
from tests.fixtures.resumes.pdf_factory import build_pdf, encrypt_pdf


def test_validate_pdf_accepts_valid_pdf() -> None:
    validate_pdf(build_pdf("Jane Doe"))


def test_validate_pdf_rejects_invalid_structure() -> None:
    with pytest.raises(InvalidPdfError):
        validate_pdf(b"%PDF-1.4\nnot a real document")


def test_validate_pdf_rejects_encrypted_pdf() -> None:
    with pytest.raises(InvalidPdfError, match="encrypted"):
        validate_pdf(encrypt_pdf(build_pdf("Jane Doe")))


def test_extract_pdf_text_returns_readable_text() -> None:
    text = extract_pdf_text(build_pdf("Jane Doe\njane@example.com"))

    assert "Jane Doe" in text
    assert "jane@example.com" in text


def test_extract_pdf_text_rejects_blank_pdf() -> None:
    with pytest.raises(UnreadableContentError, match="readable text"):
        extract_pdf_text(build_pdf(""))


def test_extract_pdf_text_rejects_whitespace_only_text() -> None:
    with pytest.raises(UnreadableContentError):
        extract_pdf_text(build_pdf("   "))
