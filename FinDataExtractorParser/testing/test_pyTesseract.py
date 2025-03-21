from PDFparsers import pyTesseract

def test_convert_pdf_to_images(image_pdf_path):
    """Test converting an image-based pdf into images"""
    images = pyTesseract.convert_pdf_to_images(image_pdf_path)

    assert isinstance(images, list), "Expected a list of images"
    assert len(images) > 0, "Expected at least one extracted image"
    assert isinstance(images[0], dict), "Each item should be a dictionary"
    assert 0 in images[0], "Each dictionary should have a page number as a key"
    assert isinstance(images[0][0], bytes), "Extracted image should be in bytes format"

def test_extract_text_from_img(image_pdf_path):
    """test ocr extraction from images"""
    images = pyTesseract.convert_pdf_to_images(image_pdf_path)
    extracted_text = pyTesseract.extract_text_from_img(images)

    assert isinstance(extracted_text, str), "Extracted text should be a string"
    assert len(extracted_text.strip()) > 0, "Expected extracted text to contain content"

    expected_text_snippet = "DocuSign"
    assert expected_text_snippet in extracted_text, f"Expected '{expected_text_snippet}' in extracted text"

def test_extract_content(image_pdf_path):
    """Test full ocr pipeline."""
    extracted_text = pyTesseract.extract_content(image_pdf_path)

    assert isinstance(extracted_text, str), "Extracted text should be a string"
    assert len(extracted_text.strip()) > 0, "Expected extracted text to contain content"

    expected_text_snippet = "DocuSign"
    assert expected_text_snippet in extracted_text, f"Expected '{expected_text_snippet}' in extracted text"
