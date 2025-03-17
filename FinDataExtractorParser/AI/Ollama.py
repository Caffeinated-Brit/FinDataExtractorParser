# go to the ollama github page download for windows
# to download the model find it on ollama's site(https://ollama.com/search) and in the command line run "ollama run "name of model""
# example of getting a model "ollama run llama3.1:8b"
# dont forget to type the size of the model in addition to the name
import time
from concurrent.futures import ThreadPoolExecutor

#tested models
#llama3.1:8b works well
#qwen2.5:14b works very very well giving basically only valid json on its own
#llama3.2:3b sucks
#qwen2.5-coder:3b great amazing, as far as tested as good as qwen2.5:14b though I dont expect it to keep up with more advanced pdfs

import ollama

#LLM_MODEL="llama3.1:8b"
#LLM_MODEL="qwen2.5:14b"
LLM_MODEL="qwen2.5-coder:3b" # for lukas' backpack brick
#LLM_MODEL="qwen2.5-coder:7b" # for spencers spacestation

def process_text_with_llm(prompt, keep_alive=True):
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
    #return response.message.content

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

def run_benchmarking(num_requests, prompt, keep_alive=False):
    loaded = process_text_with_llm("Load model into memory before benchmarking.", keep_alive)
    start_time = time.time()
    print(f"Running {num_requests} parallel requests:")
    results = run_parallel_requests(num_requests, prompt)
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Total time for {num_requests} requests: {end_time - start_time} seconds")
    return results, total_time

#run_benchmarking(30)