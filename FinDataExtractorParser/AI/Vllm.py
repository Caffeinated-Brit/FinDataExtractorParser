import threading
import time
from concurrent.futures import ThreadPoolExecutor
import requests
from vllm import LLM, SamplingParams
import os
import torch
os.environ ['VLLM_USE_V1'] ='1'


#from FinDataExtractorParser.AI.VllmServer import start_vllm_server

#llm_server_thread = threading.Thread(target=start_vllm_server)
#llm_server_thread.start()
#time.sleep(60)


def process_text_with_llm(prompt, server_url="http://localhost:8000/v1/chat/completions"):
    start_time = time.time()
    response = requests.post(
        server_url,
        json={"model": "Qwen/Qwen2.5-7B-Instruct-GPTQ-Int8",
            "messages": [{"role": "user", "content": prompt}],
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

    #content = response.json()['choices'][0]['message']['content']
    content = response.json()
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


start_time = time.time()
num_requests = 20  # Adjust this to the number of parallel requests you want
print(f"Running {num_requests} parallel requests:")
run_parallel_requests(num_requests)
end_time = time.time()
print(f"Total time for {num_requests} requests: {end_time - start_time} seconds")

'''
start_time = time.time()
for i in range(1):
    print(f"Run {i+1}:")
    print(process_text_with_llm("Give me an essay about bees with at least 10 talking points."))
    print("-" * 50)
end_time = time.time()
print((end_time - start_time))
'''


'''
num_gpus = torch.cuda.device_count()
print("GPUs: " + str(num_gpus))

prompts = [[{"role": "user", "content": "Give me a recipe for bread."}], [{"role": "user", "content": "Give me a recipe"}], [{"role": "user", "content": "Tell me a story"}]]

sampling_params = SamplingParams(temperature=0.8, top_p=0.95, max_tokens=1000)
#llm = LLM(model="Qwen/Qwen2.5-3B-Instruct", tensor_parallel_size=2, gpu_memory_utilization=0.97, max_model_len=1000)
#llm = LLM(model="Qwen/Qwen2.5-7B-Instruct-1M", tensor_parallel_size=2, quantization="bitsandbytes", load_format="bitsandbytes", enforce_eager=True, gpu_memory_utilization=0.9, max_model_len=10000)
llm = LLM(model="Qwen/Qwen2.5-7B-Instruct-GPTQ-Int8", tensor_parallel_size=num_gpus, enforce_eager=True, gpu_memory_utilization=0.90, max_model_len=10000)
#llm = LLM(model="deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B", tensor_parallel_size=2, gpu_memory_utilization=0.80, max_model_len=10000)

outputs = llm.chat(prompts, sampling_params)

for output in outputs:
    generated_text = output.outputs[0].text
    print(generated_text)




#llm = LLM(model="Qwen/Qwen2.5-Coder-3B-Instruct", tensor_parallel_size=2, dtype="float16", quantization="fp8", enforce_eager=True, max_num_seqs=2, gpu_memory_utilization=0.8, swap_space=4)
#llm = LLM(model="Qwen/Qwen2.5-Coder-3B-Instruct", tensor_parallel_size=2, enforce_eager=True, max_num_seqs=2, gpu_memory_utilization=0.8, swap_space=4, cpu_offload_gb=0, quantization="bitsandbytes", load_format="bitsandbytes",)

'''

