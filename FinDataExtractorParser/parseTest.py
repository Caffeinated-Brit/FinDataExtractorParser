import json
import pytest
import chardet
from unittest.mock import patch, MagicMock

from AI import Ollama
from PDFparsers import pdfPlumber, pyTesseract, linuxTest
import extractJSON
from parse import fullParse

TEST_PDF_PATH = "FinDataExtractorParser/testing/Simple Mock Data.pdf"

# Sample extracted text from PDF for testing
MOCK_EXTRACTED_TEXT = """Simple Mock Data
Name: Lukas Maynard
Date: 11/29/2024
Address: 1234 whocare lane"""

# Sample AI-generated JSON output
MOCK_AI_JSON = """[
    {
        "name": "Lukas Maynard",
        "date": "11/29/2024",
        "address": "1234 whocare lane"
    }
]"""

# Mocked JSON output after fixing truncated JSON
MOCK_FIXED_JSON = json.loads(MOCK_AI_JSON)

@pytest.fixture
def mock_pdf_parsing():
    """Mock different PDF parsing methods."""
    with patch.object(pdfPlumber, "extract_text_from_pdf", return_value=MOCK_EXTRACTED_TEXT), \
         patch.object(pyTesseract, "extract_content", return_value=MOCK_EXTRACTED_TEXT), \
         patch.object(linuxTest, "linuxParse", return_value=MOCK_EXTRACTED_TEXT):
        yield

@pytest.fixture
def mock_ai_processing():
    """Mock AI text processing method."""
    with patch.object(Ollama, "process_text_with_llm", return_value=MOCK_AI_JSON):
        yield

@pytest.fixture
def mock_json_fixing():
    """Mock JSON extraction and fixing."""
    with patch.object(extractJSON, "fix_truncated_json", return_value=MOCK_FIXED_JSON):
        yield

@pytest.fixture
def mock_encoding_detection():
    """Mock file encoding detection."""
    with patch.object(chardet, "detect", return_value={"encoding": "utf-8"}):
        yield

def test_fullParse(mock_pdf_parsing, mock_ai_processing, mock_json_fixing, mock_encoding_detection, tmp_path):
    """Test the fullParse function end-to-end with mocks."""

    # Create a temporary test file to simulate a PDF
    test_pdf = tmp_path / "test.pdf"
    test_pdf.write_bytes(b"%PDF-1.4 Test PDF Content")

    # Run fullParse with the mocked functions
    structured_data = fullParse(str(test_pdf))

    # Validate structured_data is correctly parsed as a list (JSON array)
    assert isinstance(structured_data, list), "AI did not return a valid JSON array"
    assert all(isinstance(item, dict) for item in structured_data), "JSON elements must be dictionaries"

    # Ensure JSON output file was created
    output_json_file = test_pdf.with_suffix(".json")
    assert output_json_file.exists(), "JSON output file was not created"

    # Ensure JSON file content is valid
    with open(output_json_file, "r", encoding="utf-8") as f:
        json_content = json.load(f)
        assert isinstance(json_content, list), "Saved JSON file does not contain a valid JSON array"

# testing pdf plumber
def test_valid_pdf_extraction():
    """Test extracting text from a valid PDF."""
    # this for some reason has to be the full file path, or this complex os.path.join? dont know why
    pdf_path = "testing/Simple_Mock_Data.pdf"
    extracted_text = pdfPlumber.extract_text_from_pdf(pdf_path)
    print("\nExtracted Text:\n", extracted_text)  # Debugging step

    assert "Lukas Maynard" in extracted_text

def test_missing_pdf():
    """Test behavior when the PDF file is missing."""
    non_existent_file = "nonexistent.pdf"
    extracted_text = pdfPlumber.extract_text_from_pdf(non_existent_file)

    assert extracted_text == "", "Expected empty string when file does not exist"

@patch("pdfplumber.open")
def test_empty_pdf(mock_pdfplumber):
    """Test extracting text from an empty PDF."""
    mock_pdf = MagicMock()
    mock_pdf.pages = []
    mock_pdfplumber.return_value.__enter__.return_value = mock_pdf

    extracted_text = pdfPlumber.extract_text_from_pdf("testing/dummy.pdf")

    assert extracted_text == "", "Expected empty string for an empty PDF"


# tests pytesseract
@pytest.fixture
def image_pdf_path():
    """Provide the path to a real image-based PDF for testing."""
    return "testing/loan_statement.pdf"  # actual file path

def test_convert_pdf_to_images(image_pdf_path):
    """Test converting an image-based PDF into images."""
    images = pyTesseract.convert_pdf_to_images(image_pdf_path)
    
    assert isinstance(images, list), "Expected a list of images"
    assert len(images) > 0, "Expected at least one extracted image"
    assert isinstance(images[0], dict), "Each item should be a dictionary"
    assert 0 in images[0], "Each dictionary should have a page number as a key"
    assert isinstance(images[0][0], bytes), "Extracted image should be in bytes format"

def test_extract_text_from_img(image_pdf_path):
    """Test OCR text extraction from images."""
    images = pyTesseract.convert_pdf_to_images(image_pdf_path)
    extracted_text = pyTesseract.extract_text_from_img(images)

    assert isinstance(extracted_text, str), "Extracted text should be a string"
    assert len(extracted_text.strip()) > 0, "Expected extracted text to contain content"
    
    # Adjust the expected text based on your sample PDF
    expected_text_snippet = "DocuSign"  # Replace with actual text you expect
    assert expected_text_snippet in extracted_text, f"Expected '{expected_text_snippet}' in extracted text"

def test_extract_content(image_pdf_path):
    """Test full OCR extraction pipeline."""
    extracted_text = pyTesseract.extract_content(image_pdf_path)

    assert isinstance(extracted_text, str), "Extracted text should be a string"
    assert len(extracted_text.strip()) > 0, "Expected extracted text to contain content"
    
    expected_text_snippet = "DocuSign"  # Adjust to match your PDF text
    assert expected_text_snippet in extracted_text, f"Expected '{expected_text_snippet}' in extracted text"
