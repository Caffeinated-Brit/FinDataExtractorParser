# pip install paddleocr
# pip install paddlepaddle
# more trouble than it is worth, tesseract is better.

from paddleocr import PaddleOCR

def paddleOCR_OCR(img_path):
    ocr = PaddleOCR(use_angle_cls=True, lang='en') # need to run only once to download and load model into memory
    result = ocr.ocr(img_path, cls=True)
    # for line in result:
    #     print(line)

    return result

if __name__ == "__main__":
    print(paddleOCR_OCR("C:/Users/lukas/Desktop/Capstone/FinDataExtractorParser/FinDataExtractorParser/examplePDFs/fromCameron/loan_statement.pdf"))