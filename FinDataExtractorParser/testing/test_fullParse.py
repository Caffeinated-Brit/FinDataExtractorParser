import pytest
from unittest.mock import patch
import json
from parse import fullParse

#moved all of these to conftest.py
# @pytest.fixture
# def mock_pdf_parsing():
#     """Mock the PDF parsing function."""
#     with patch('PDFparsers.pdfPlumber.extract_text_from_pdf') as mock:
#         yield mock
#
# @pytest.fixture
# def mock_ai_processing():
#     """Mock the AI processing function."""
#     with patch('AI.Ollama.process_text_with_llm') as mock:
#         yield mock
#
# @pytest.fixture
# def mock_json_fixing():
#     """Mock the JSON fixing function (its not really used anymore...)"""
#     with patch('extractJSON.fix_truncated_json') as mock:
#         yield mock
#
# @pytest.fixture
# def mock_encoding_detection():
#     """Mock the chardet encoding detection"""
#     with patch('chardet.detect') as mock:
#         yield mock

def test_fullParse(mock_pdf_parsing, mock_ai_processing, mock_json_fixing, mock_encoding_detection, tmp_path):
    """Test the fullParse function with mocks."""

    # Setup the mocks, no longer needed as they are setup in conftest.py now
    # mock_pdf_parsing.return_value = "Extracted PDF content"
    # mock_ai_processing.return_value = [{"key": "value"}]  # Mock AI output as structured data
    # mock_json_fixing.return_value = [{"key": "value"}]  # Mock fixed JSON
    # mock_encoding_detection.return_value = {"encoding": "utf-8"}

    # Create a temp file to simulate a PDF
    test_pdf = tmp_path / "test.pdf"
    test_pdf.write_bytes(b"%PDF-1.4 Test PDF Content")

    # Run fullParse with mocked functions
    structured_data = fullParse(str(test_pdf))

    assert isinstance(structured_data, list), "AI did not return a valid JSON array"
    assert all(isinstance(item, dict) for item in structured_data), "JSON elements must be dictionaries"

    output_json_file = test_pdf.with_suffix(".json")
    assert output_json_file.exists(), "JSON output file was not created"

    with open(output_json_file, "r", encoding="utf-8") as f:
        json_content = json.load(f)
        assert isinstance(json_content, list), "Saved JSON file does not contain a valid JSON array"

    # testing if the mocked functions were called correctly, this was used when the mocks were setup in this file
    # mock_pdf_parsing.assert_called_once_with(str(test_pdf))
    # mock_ai_processing.assert_called_once()
    # mock_json_fixing.assert_called_once()
    # mock_encoding_detection.assert_called_once()
