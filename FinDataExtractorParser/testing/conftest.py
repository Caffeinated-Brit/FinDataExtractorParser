import json
import pytest
import chardet
import sys
import os
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from AI import Ollama
from PDFparsers import pdfPlumber, pyTesseract, linux_pdftotext
import extractJSON

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

MOCK_FIXED_JSON = json.loads(MOCK_AI_JSON)


@pytest.fixture
def mock_pdf_parsing():
    """Mock different PDF parsing methods."""
    with patch.object(pdfPlumber, "extract_text_from_pdf", return_value=MOCK_EXTRACTED_TEXT), \
         patch.object(pyTesseract, "extract_content", return_value=MOCK_EXTRACTED_TEXT), \
         patch.object(linux_pdftotext, "linuxParse", return_value=MOCK_EXTRACTED_TEXT):
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


@pytest.fixture
def image_pdf_path():
    """Provide the path to a real image-based PDF for testing."""
    return os.path.join(os.path.dirname(__file__), "loan_statement.pdf")
