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

# Only call from run_parallel_requests_with_schema
def process_text_with_llm_and_schema(user_prompt, schema):
    #print(type(FinancialData))
    #print(type(FinancialData.model_json_schema()))
    #print(FinancialData.model_json_schema())

    print(type(schema))
    print(schema)

    try:
        schema_json = json.loads(schema)  # parsed as dict
        print("Parsed Schema JSON:")
        print(json.dumps(schema_json, indent=2))
    except json.JSONDecodeError as e:
        print("Failed to decode JSON:", e)
        return "Invalid JSON", 400


    print("Starting Ollama extraction with a json schema...")
    response = ollama.chat(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": user_prompt}],
        options={"seed": 1, "temperature":0.1, "top_k":1},
        # auto formats output into json, going to keep messing with this and other parameters
        #format=FinancialData.model_json_schema()
        format = schema_json
    )
    return response.message.content

# Only call from run_parallel_requests
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

def run_parallel_requests(num_requests, prompt):

    results = []
    with ThreadPoolExecutor(max_workers=num_requests) as executor:
        futures = []
        for i in range(num_requests):
            futures.append(executor.submit(process_text_with_llm, prompt))

        for future in futures:
            print(future.result())
            print("-" * 50)
            results.append(future.result())

    return results

def run_parallel_requests_with_schema(num_requests, prompt, schema):

    results = []
    with ThreadPoolExecutor(max_workers=num_requests) as executor:
        futures = []
        for i in range(num_requests):
            futures.append(executor.submit(process_text_with_llm_and_schema, prompt, schema))

        for future in futures:
            print(future.result())
            print("-" * 50)
            results.append(future.result())

    return results


#Never call this outside of benchmarking
def run_benchmarking(num_requests, prompt, keep_alive=False):
    process_text_with_llm("Load model into memory before benchmarking.", keep_alive)
    start_time = time.time()
    print(f"Running {num_requests} parallel requests:")
    results = run_parallel_requests(num_requests, prompt)
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Total time for {num_requests} requests: {end_time - start_time} seconds")
    return results, total_time


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

