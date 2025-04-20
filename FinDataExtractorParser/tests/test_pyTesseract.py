import pytest
from PDFparsers import pyTesseract

@pytest.fixture
def image_pdf_path():
    return "uploads/Simple_Mock_Data.pdf"

def test_convert_pdf_to_images(image_pdf_path):
    images = pyTesseract.convert_pdf_to_images(image_pdf_path)

    assert isinstance(images, list)
    assert images and isinstance(images[0], dict)
    assert 0 in images[0]
    assert isinstance(images[0][0], bytes)

def test_extract_text_from_img(image_pdf_path):
    images = pyTesseract.convert_pdf_to_images(image_pdf_path)
    text = pyTesseract.extract_text_from_img(images)

    assert isinstance(text, str)
    assert len(text.strip()) > 0

def test_extract_content(image_pdf_path):
    text = pyTesseract.extract_content(image_pdf_path)

    assert isinstance(text, str)
    assert len(text.strip()) > 0
