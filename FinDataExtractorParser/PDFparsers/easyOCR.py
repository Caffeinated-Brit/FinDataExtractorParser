# have not gotten this one to work
import easyocr

def easyocr_text_extract(file_path):
    reader = easyocr.Reader(['ch_sim','en']) # this needs to run only once to load the model into memory
    result = reader.readtext(file_path, detail=0)
    return result

if __name__ == "__main__":
    print(easyocr_text_extract("C:/Users/lukas/Desktop/Capstone/FinDataExtractorParser/FinDataExtractorParser/examplePDFs/fromCameron/loan_statement.pdf"))