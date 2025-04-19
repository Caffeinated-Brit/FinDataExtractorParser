# go to the ollama github page download for windows
# to download the model find it on ollama's site(https://ollama.com/search) and in the command line run "ollama run "name of model""
# example of getting a model "ollama run llama3.1:8b"
# dont forget to type the size of the model in addition to the name
import json
import os
import difflib
import time
from concurrent.futures import ThreadPoolExecutor

#tested models
#llama3.1:8b works well
#qwen2.5:14b works very very well giving basically only valid json on its own
#llama3.2:3b sucks
#qwen2.5-coder:3b great amazing, as far as tested as good as qwen2.5:14b though I dont expect it to keep up with more advanced pdfs

#LLM_MODEL="llama3.1:8b"
#LLM_MODEL="qwen2.5:14b"
# LLM_MODEL="qwen2.5-coder:7b"
# LLM_MODEL="qwen2.5-coder:3b"

from concurrent.futures import ThreadPoolExecutor
import time
import configparser

import ollama
from pydantic import BaseModel, Extra, Field

from schemas.general_schema_basic import FinancialData

config = configparser.ConfigParser()
config.read("config.ini")
LLM_MODEL =  config.get("Ollama Model", "model", fallback="qwen2.5-coder:3b")

# LLM_MODEL="qwen2.5-coder:3b" # for lukas' backpack brick
# #LLM_MODEL="qwen2.5-coder:7b" # for spencers spacestation

def process_text_with_llm_and_schema(user_prompt):
    print("Starting Ollama extraction with a json schema...")
    response = ollama.chat(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": user_prompt}],
        options={"seed": 1, "temperature":0.1, "top_k":1},
        # auto formats output into json, going to keep messing with this and other parameters
        format=FinancialData.model_json_schema()
    )
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

if __name__ == "__main__":
    prompt = (
        f"The following text was extracted from a PDF.\n"
        "Extract and categorize the data from the text. Return as JSON.\n"
        f"Text:\n")

    # print(prompt)
    # # print(process_text_with_llm(prompt +""" test text here """))

    #print(prompt)
    #print(run_parallel_requests(5, "Ya Like bees"))
    # run_benchmarking(3, "Ya Like bees")

