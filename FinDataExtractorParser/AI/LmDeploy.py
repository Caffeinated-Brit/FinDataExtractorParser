import time

from lmdeploy import pipeline, PytorchEngineConfig
import torch
from torch.distributed._composable.replicate import DDP
from torch.nn import DataParallel
from lmdeploy import pipeline, GenerationConfig, TurbomindEngineConfig
from openai import OpenAI
import openai
import requests
import json



torch.cuda.empty_cache()
torch.cuda.memory_summary()
#pipe = pipeline('Qwen/Qwen2.5-Coder-3B-Instruct', device='cpu')

#lmdeploy serve api_server Qwen/Qwen2.5-Coder-3B-Instruct --server-port 23333 --tp 2 --cache-max-entry-count 0.2


print("Number of GPUs available:", torch.cuda.device_count())
for i in range(torch.cuda.device_count()):
    print(f"GPU {i}: {torch.cuda.get_device_name(i)}")


#LLM_MODEL="Qwen/Qwen2.5-7B-Instruct-1M"
LLM_MODEL="Qwen/Qwen2.5-Coder-3B-Instruct"

def process_text_with_llm_OLD(prompt):
    print("Starting LmDeploy extraction with " + LLM_MODEL)
    pipe = pipeline(LLM_MODEL,
                    backend_config=PytorchEngineConfig(
                        max_batch_size=32,
                        enable_prefix_caching=True,
                        #cache_max_entry_count=0.5,
                        session_len=10000,
                    ),
                    device="cuda"
                    )


    pipe.model.to("cuda")

    pipe.model = DDP(pipe.model, device_ids=[0, 1])

    response = pipe([{"role": "user", "content": prompt}])
    # print(response)
    #This returns just the message from the LLM nothing else but there are other neat things to return
    #print(response.text)
    return response.text

def process_text_with_llm_OLD(prompt):
    print("Starting LmDeploy extraction with " + LLM_MODEL)

    backend_config = TurbomindEngineConfig(cache_max_entry_count=0.2, enable_prefix_caching=False, max_batch_size=4, session_len=20000, tp=2)

    gen_config = GenerationConfig(top_p=0.1,
                                  top_k=40,
                                  temperature=0,
                                  max_new_tokens=18000)

    pipe = pipeline(LLM_MODEL, backend_config=backend_config)

    response = pipe([prompt],
                    gen_config=gen_config)

    print("Generated token length: " + response[0].generate_token_len)
    print("Input token length: " + response[0].input_token_len)
    return response[0].text

def process_text_with_llm(prompt, server_url="http://localhost:23333/v1/chat/completions"):
    start_time = time.time()
    response = requests.post(
        server_url,
        json={"model": "Qwen/Qwen2.5-Coder-3B-Instruct",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 10000,  # Increase for longer output
            #"min_tokens": 900,
            "top_k": 40,
            "temperature": 0.9,  # Adjust for randomness
            "top_p": 0.9,
            "n": 1,
            "stop": ["User:", "\n\n"]
            }
    )
    end_time = time.time()
    elapsed_time = end_time - start_time


    generated_tokens = response.json().get("usage", {}).get("completion_tokens", 0)

    tokens_per_second = generated_tokens / elapsed_time
    print(f"Generated tokens per second: {tokens_per_second}")

    content = response.json()["choices"][0]["message"]["content"]
    #print(response.json())
    return content


for i in range(1):
    print(f"Run {i+1}:")
    print(process_text_with_llm("Give me a recipe for cake."))
    print("-" * 50)  # Separator for readability

#print(process_text_with_llm("Give me a cake recipe"))
