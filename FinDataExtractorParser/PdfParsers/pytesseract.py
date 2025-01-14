from pytesseract import image_to_string
from io import BytesIO
import pypdfium2 as pdfium
from PIL import Image

# Convert PDF file into images with pypdfium2
def convert_pdf_to_images(file_path, scale=300/72):
    print("converting pdf to images")
    pdf_file = pdfium.PdfDocument(file_path)
    page_indices = [i for i in range(len(pdf_file))]
    renderer = pdf_file.render(
        pdfium.PdfBitmap.to_pil,
        page_indices=page_indices,
        scale=scale,
    )

    final_images = []
    for i, image in zip(page_indices, renderer):
        image_byte_array = BytesIO()
        image.save(image_byte_array, format='jpeg', optimize=True)
        image_byte_array = image_byte_array.getvalue()
        final_images.append(dict({i: image_byte_array}))

    return final_images

# Extract text from images with pytesseract
def extract_text_from_img(list_dict_final_images):
    print("Extracting text from images")
    image_list = [list(data.values())[0] for data in list_dict_final_images]
    image_content = []

    for index, image_bytes in enumerate(image_list):
        image = Image.open(BytesIO(image_bytes))
        raw_text = str(image_to_string(image))
        image_content.append(raw_text)

    return "\n".join(image_content)

# calls other functions to extract all text, given the file path
def extract_content(file_path):
    images_list = convert_pdf_to_images(file_path)
    extracted_data = extract_text_from_img(images_list)

    return extracted_data