import io
import easyocr
from PIL import Image
from PDFparsers.pyTesseract import convert_pdf_to_images

def easyocr_text_extract(file_path):
    reader = easyocr.Reader(['ch_sim','en']) # this needs to run only once to load the model into memory
    # result = reader.readtext(file_path, detail=0)

    my_images = convert_pdf_to_images(file_path)
    # print(my_images)

    text = []

    for page in my_images:
        image_bytes = list(page.values())[0]  # Extract byte data
        image = Image.open(io.BytesIO(image_bytes)) # Convert byte array to PIL image

        result = reader.readtext(image, detail=1)  # pass the PIL image to EasyOCR for text extraction
        # detail=0 is just text
        # detail=1 is text, position (bounding box), and confidence scores

        # you can somehow show bounding boxes, i have been unable to see this
        # image_with_boxes = reader.draw_boxes(image, result)
        # image_with_boxes.show()

        # for printing details for each item
        print("inner output -------------")
        for item in result:
            text, coords, confidence = item[1], item[0], item[2]
            print(f"Text: {text}\nPosition: {coords}\nConfidence: {confidence}")

        text.extend(result)

    return text

if __name__ == "__main__":
    print(easyocr_text_extract("C:/Users/lukas/Desktop/Capstone/FinDataExtractorParser/FinDataExtractorParser/examplePDFs/fromCameron/loan_statement.pdf"))