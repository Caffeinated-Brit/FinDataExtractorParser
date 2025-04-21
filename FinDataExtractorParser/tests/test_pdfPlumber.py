import os
import pytest
from unittest.mock import patch, MagicMock
from PDFparsers import pdfPlumber

# Path to a real test file you expect to be in your repo
TEST_PDF_PATH = "../tests/uploads/Simple_Mock_Data.pdf"


def test_valid_pdf_extraction():
    """Test extracting text from a real PDF"""
    extracted_text = pdfPlumber.extract_text_from_pdf(TEST_PDF_PATH)

    assert isinstance(extracted_text, str)
    assert "Lukas Maynard" in extracted_text
    assert len(extracted_text.strip()) > 0


@patch("pdfplumber.open")
def test_empty_pdf_returns_empty_string(mock_pdfplumber):
    """Test behavior when PDF has no pages"""
    mock_pdf = MagicMock()
    mock_pdf.pages = []  # Simulate no pages in PDF
    mock_pdfplumber.return_value.__enter__.return_value = mock_pdf

    dummy_path = os.path.join(os.path.dirname(__file__), "dummy.pdf")
    result = pdfPlumber.extract_text_from_pdf(dummy_path)

    assert result == "", "Expected empty string for a PDF with no pages"


@patch("pdfplumber.open")
def test_pdf_with_page_no_text(mock_pdfplumber):
    """Test behavior when pages exist but contain no text"""
    mock_page = MagicMock()
    mock_page.extract_text.return_value = None  # simulate blank page
    mock_pdf = MagicMock()
    mock_pdf.pages = [mock_page, mock_page]

    mock_pdfplumber.return_value.__enter__.return_value = mock_pdf

    result = pdfPlumber.extract_text_from_pdf("fake_path.pdf")
    assert result == "", "Expected empty string when no text is extracted from any pages"
