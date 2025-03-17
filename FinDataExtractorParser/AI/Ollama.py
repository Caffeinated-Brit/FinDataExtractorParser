# go to the ollama github page download for windows
# to download the model find it on ollama's site(https://ollama.com/search) and in the command line run "ollama run "name of model""
# example of getting a model "ollama run llama3.1:8b"
# dont forget to type the size of the model in addition to the name


#tested models
#llama3.1:8b works well
#qwen2.5:14b works very very well giving basically only valid json on its own
#llama3.2:3b sucks
#qwen2.5-coder:3b great amazing, as far as tested as good as qwen2.5:14b though I dont expect it to keep up with more advanced pdfs

import ollama
from nltk.app.nemo_app import images
from pydantic import BaseModel, Extra
from PIL import Image
import io


#LLM_MODEL="llama3.1:8b"
#LLM_MODEL="qwen2.5:14b"
LLM_MODEL="qwen2.5-coder:3b"
# LLM_MODEL="qwen2.5-coder:7b"
LLM_VISION_MODEL="llava:7b"

class CompanyInfo(BaseModel):
    name: str
    address: str
    phone_number: str
    email: str
    website: str

class PersonalInfo(BaseModel):
    name: str
    address: str
    phone_number: str
    email: str
    bank_account_number: str

class FinancialData(BaseModel):
    personal_Info: PersonalInfo
    company_Info: CompanyInfo

    class Config:
        extra = 'allow'  # Allow extra fields to be added by Ollama

# requires matplotlib library
# Ensure this function handles raw image bytes or file paths properly
def process_text_with_llm_vision(user_prompt, user_images):
    print("Starting Ollama extraction with vision...")

    # Step 1: Convert the user_images (if necessary) to bytes
    processed_images = []
    for img in user_images:
        if isinstance(img, bytes):  # If already in raw bytes, no conversion needed
            processed_images.append(img)
        elif isinstance(img, str):  # If it's a file path, open and read the image
            with open(img, 'rb') as file:
                processed_images.append(file.read())
        elif isinstance(img, Image.Image):  # If it's a PIL Image, convert to bytes
            img_buffer = io.BytesIO()
            img.save(img_buffer, format='PNG')
            processed_images.append(img_buffer.getvalue())
        else:
            raise TypeError(f"Unsupported image type: {type(img)}")

    # Step 2: Pass the processed image data to Ollama chat
    response = ollama.chat(
        model=LLM_VISION_MODEL,
        messages=[
            {"role": "user", "content": user_prompt, "images": processed_images}
        ],
        options={"seed": 1, "temperature": 0}
    )
    # Return just the message content
    return response.message.content


def process_text_with_llm(user_prompt):
    print("Starting Ollama extraction...")
    response = ollama.chat(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": user_prompt}],
        options={"seed": 1, "temperature":0},
        # auto formats output into json, going to keep messing with this and other parameters
        format="json"
    )
    #This returns just the message from the LLM nothing else
    return response.message.content

def process_text_with_llm_and_schema(user_prompt):
    print("Starting Ollama extraction with a json schema...")
    response = ollama.chat(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": user_prompt}],
        options={"seed": 1, "temperature":0},
        # auto formats output into json, going to keep messing with this and other parameters
        format=FinancialData.model_json_schema()
    )
    #This returns just the message from the LLM nothing else
    return response.message.content

if __name__ == "__main__":

    file_path = r"C:\Users\lukas\Desktop\Capstone\FinDataExtractorParser\FinDataExtractorParser\examplePDFs\fromCameron\2021_2_Statement_removed.pdf"
    with open(file_path, 'r') as file:
        file_contents = file.read()

    prompt = (
        f"The following text was extracted from a PDF.\n"
        "Extract and categorize the data from the text. Return as JSON.\n"
        # "Ignore any terms and conditions, and only extract valuable financial data.\n"
        # "Categorize the extracted data into valid JSON format.\n"
        # "Ensure the JSON is fully valid and does not contain errors.\n"
        # "Return only the JSON array, with no extra text before or after.\n"
        f"Text:\n"
    )
    print(prompt + file_contents)
    # print(process_text_with_llm(prompt + file_contents))