import os
from unittest.mock import patch, MagicMock
from PDFparsers import pdfPlumber

TEST_PDF_PATH = os.path.join(os.path.dirname(__file__), "Simple_Mock_Data.pdf")

def test_valid_pdf_extraction():
    """test extracting text from a valid pdf"""
    extracted_text = pdfPlumber.extract_text_from_pdf(TEST_PDF_PATH)
    assert "Lukas Maynard" in extracted_text

# removed this and put it in parse.py to cover more bases
# def test_missing_pdf():
#     """test when the PDF file is missing"""
#     extracted_text = pdfPlumber.extract_text_from_pdf("nonexistent.pdf")
#     assert extracted_text == "", "Expected empty string when file does not exist"

@patch("pdfplumber.open")
def test_empty_pdf(mock_pdfplumber):
    """test extracting text from an empty pdf"""
    mock_pdf = MagicMock()
    mock_pdf.pages = []
    mock_pdfplumber.return_value.__enter__.return_value = mock_pdf

    extracted_text = pdfPlumber.extract_text_from_pdf(os.path.join(os.path.dirname(__file__), "dummy.pdf"))
    assert extracted_text == "", "Expected empty string for an empty PDF"
