import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
import requests
# from vllm import LLM, SamplingParams
import os
from FinDataExtractorParser.AI.VllmServer import start_vllm_server
os.environ ['VLLM_USE_V1'] ='1'

shutdown_event = threading.Event()
llm_server_thread = threading.Thread(target=start_vllm_server, args=(shutdown_event,))


def process_text_with_llm(prompt, server_url="http://localhost:8000/v1/chat/completions"):
    start_time = time.time()
    response = requests.post(
        server_url,
        json={"model": "Qwen/Qwen2.5-7B-Instruct-GPTQ-Int8",
            #"messages": [{"role": "system", "content": "You are a helpful financial pdf parsing assistant. You respond with only json."}, {"role": "user", "content": prompt}],
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 5000,  # Increase for longer output
            #"min_tokens": 900,
            #"top_k": 20,
            "temperature": 0.15,
            #"top_p": 0.1,
            #"n": 1,
            #"stop": ["User:", "\n\n"]
            }
    )
    end_time = time.time()
    elapsed_time = end_time - start_time


    generated_tokens = response.json().get("usage", {}).get("completion_tokens", 0)


    #print(f"Generated tokens per second: {tokens_per_second}")
    #print(response.json())
    content = response.json()['choices'][0]['message']['content']
    #print(response.json()['choices'][0])
    return content, elapsed_time, generated_tokens


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


def run_benchmarking(num_requests, prompt):
    start_time = time.time()
    print(f"Running {num_requests} parallel requests:")
    results = run_parallel_requests(num_requests, prompt)
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Total time for {num_requests} requests: {end_time - start_time} seconds")
    stop_llm_server()
    return results, total_time

def stop_llm_server():
    """Trigger the shutdown event to stop the server."""
    print("Triggering server shutdown...")
    shutdown_event.set()  # Set the shutdown event to stop the server
    llm_server_thread.join()

def start_llm_server():
    llm_server_thread.start()
    time.sleep(60) # Allow time for the server to start, this could be handled better and may cause crashes if it takes longer to start

#start_llm_server()
