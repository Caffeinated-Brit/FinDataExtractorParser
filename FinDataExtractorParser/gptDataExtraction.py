# MAIN DEPENDENCIES - need added to requirements.txt
# pip install langchain
# pip install langchain_community
# pip install openai 
# pip install python-dotenv
# pip install pypdfium2

from langchain_community.chat_models import ChatOpenAI
# from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
from pytesseract import image_to_string
from PIL import Image
from io import BytesIO
import pypdfium2 as pdfium
# import streamlit as st
# import multiprocessing
from tempfile import NamedTemporaryFile
import pandas as pd
import json
# import requests

# loads the .env file api key
load_dotenv()

# Convert PDF file into images with pypdfium2
def convert_pdf_to_images(file_path, scale=300/72):

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

    image_list = [list(data.values())[0] for data in list_dict_final_images]
    image_content = []

    for index, image_bytes in enumerate(image_list):

        image = Image.open(BytesIO(image_bytes))
        raw_text = str(image_to_string(image))
        image_content.append(raw_text)

    return "\n".join(image_content)

# calls other functions to extract all text, given the file path
def extract_content_from_url(url: str):
    images_list = convert_pdf_to_images(url)
    text_with_pytesseract = extract_text_from_img(images_list)

    return text_with_pytesseract


# Structure into JSON given text with an LLM (currently chatgpt model:"gpt-3.5-turbo-1106")
# --------------------------------------------------------------------------------------------
# NOTE THIS DOES COST a small amount of MONEY!!! DO NOT RUN IN A LOOP OR LIKE A MANIAC!!! THANKS! -lukas
# --------------------------------------------------------------------------------------------
def extract_structured_data(content: str, data_points):
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-1106")
    template = """
    You are an expert admin people who will extract core information from documents

    {content}

    Above is the content; please try to extract all data points from the content above 
    and export in a JSON array format:
    {data_points}

    Now please extract details from the content  and export in a JSON array format, 
    return ONLY the JSON array:
    """

    prompt = PromptTemplate(
        input_variables=["content", "data_points"],
        template=template,
    )

    chain = LLMChain(llm=llm, prompt=prompt)
    results = chain.run(content=content, data_points=data_points)
    return results


# this is used for an JSON example in the prompt maybe keep and make a better example?? or potentially remove later??? - lukas
default_data_points = """{
        "Name": "Persons name",
        "Date": "Date of document submission",
        "Address": "Where user is located",
    }"""


# maybe put in main function, needs cleaned up :)
text = extract_content_from_url("examplePDFs/Simple Mock Data.pdf")
print(extract_structured_data(text, default_data_points))