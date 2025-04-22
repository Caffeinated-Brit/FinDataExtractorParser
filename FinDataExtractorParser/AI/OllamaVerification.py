# go to the ollama github page download for windows
# to download the model find it on ollama's site(https://ollama.com/search) and in the command line run "ollama run "name of model""
# example of getting a model "ollama run llama3.1:8b"
# dont forget to type the size of the model in addition to the name
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

#Do not call except for run_parallel_requests_with_schema
def process_text_with_llm_and_schema_verification(user_prompt):
    print("Starting Ollama extraction with a json schema...")
    start_time = time.time()
    response = ollama.chat(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": user_prompt}],
        options={"seed": 1, "temperature":0.1, "top_k":1},
        # auto formats output into json, going to keep messing with this and other parameters
        format=FinancialData.model_json_schema()
    )
    end_time = time.time()
    elapsed_time = end_time - start_time

    generated_tokens = response['eval_count']
    content = response['message']['content']
    return content, generated_tokens, elapsed_time

#Do not call except for run_parallel_requests
def process_text_with_llm_verification(prompt, keep_alive=True):
    print("Starting Ollama extraction")
    start_time = time.time()

    response = ollama.chat(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        options={"seed": 42, "temperature":0.1, "top_p":0.1},
        keep_alive=keep_alive
    )
    end_time = time.time()
    elapsed_time = end_time - start_time

    generated_tokens = response['eval_count']
    content = response['message']['content']
    return content, generated_tokens, elapsed_time

def run_parallel_requests(num_requests, prompt):
    results = []
    with ThreadPoolExecutor(max_workers=num_requests) as executor:
        futures = []
        for i in range(num_requests):
            futures.append(executor.submit(process_text_with_llm_verification, prompt))

        for future in futures:
            print(future.result())
            print("-" * 50)
            results.append(future.result())
    return results

def run_parallel_requests_with_schema(num_requests, prompt):
    results = []
    with ThreadPoolExecutor(max_workers=num_requests) as executor:
        futures = []
        for i in range(num_requests):
            futures.append(executor.submit(process_text_with_llm_and_schema_verification, prompt))

        for future in futures:
            print(future.result())
            print("-" * 50)
            results.append(future.result())
    return results

# Use only for benchmarking
def run_benchmarking(num_requests, prompt, keep_alive=False):
    process_text_with_llm_verification("Load model into memory before benchmarking.", keep_alive)
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
