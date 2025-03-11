import threading
import time
from concurrent.futures import ThreadPoolExecutor
import requests
from vllm import LLM, SamplingParams
import os
import torch
os.environ ['VLLM_USE_V1'] ='1'


from FinDataExtractorParser.AI.VllmServer import start_vllm_server

llm_server_thread = threading.Thread(target=start_vllm_server)
llm_server_thread.start()
time.sleep(60)


def process_text_with_llm(prompt, server_url="http://localhost:8000/v1/chat/completions"):
    start_time = time.time()
    response = requests.post(
        server_url,
        json={"model": "Qwen/Qwen2.5-7B-Instruct-GPTQ-Int8",
            "messages": [{"role": "system", "content": "You are a helpful financial pdf parsing assistant."}, {"role": "user", "content": prompt}],
            #"messages": [{"role": "user", "content": prompt}],
            "max_tokens": 5000,  # Increase for longer output
            #"min_tokens": 900,
            #"top_k": 20,
            "temperature": 0.1,  # Adjust for randomness
            "top_p": 0.1,
            #"n": 1,
            #"stop": ["User:", "\n\n"]
            }
    )
    end_time = time.time()
    elapsed_time = end_time - start_time


    generated_tokens = response.json().get("usage", {}).get("completion_tokens", 0)

    tokens_per_second = generated_tokens / elapsed_time

    print(f"Generated tokens per second: {tokens_per_second}")
    #return "bees"
    content = response.json()['choices'][0]['message']['content']
    #content = response.json()["choices"][0]["message"]
    #print(content)
    return content


def run_parallel_requests(num_requests):
    with ThreadPoolExecutor(max_workers=num_requests) as executor:
        futures = []
        for i in range(num_requests):
            futures.append(
                executor.submit(process_text_with_llm, "Give me an essay about bees with at least 10 talking points."))

        # Wait for all futures to complete
        for future in futures:
            print(future.result())
            print("-" * 50)


def run_benchmarking(num_requests):
    start_time = time.time()
    print(f"Running {num_requests} parallel requests:")
    run_parallel_requests(num_requests)
    end_time = time.time()
    print(f"Total time for {num_requests} requests: {end_time - start_time} seconds")




