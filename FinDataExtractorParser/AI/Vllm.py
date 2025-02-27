import os
os.environ ['VLLM_USE_V1'] ='1'

from vllm import LLM, SamplingParams
import torch.distributed as dist
import os
os.environ ['VLLM_USE_V1'] ='1'



prompts = [[{"role": "user", "content": "Give me a recipe for bread."}], [{"role": "user", "content": "Give me a recipe"}], [{"role": "user", "content": "Tell me a story"}]]

sampling_params = SamplingParams(temperature=0.8, top_p=0.95, max_tokens=1000)
#llm = LLM(model="Qwen/Qwen2.5-3B-Instruct", tensor_parallel_size=2, gpu_memory_utilization=0.97, max_model_len=1000)
#llm = LLM(model="Qwen/Qwen2.5-7B-Instruct-1M", tensor_parallel_size=2, quantization="bitsandbytes", load_format="bitsandbytes", enforce_eager=True, gpu_memory_utilization=0.9, max_model_len=10000)
llm = LLM(model="Qwen/Qwen2.5-7B-Instruct-GPTQ-Int8", tensor_parallel_size=2, enforce_eager=True, gpu_memory_utilization=0.90, max_model_len=10000)
#llm = LLM(model="deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B", tensor_parallel_size=2, gpu_memory_utilization=0.80, max_model_len=10000)

outputs = llm.chat(prompts, sampling_params)

for output in outputs:
    generated_text = output.outputs[0].text
    print(generated_text)

'''
from vllm import LLM, SamplingParams

import os
os.environ ['CUDA_LAUNCH_BLOCKING'] ='1'


#prompts = [[{"role": "user", "content": "Who are you?"}]]
prompts = ["Who are you?"]

sampling_params = SamplingParams(temperature=0.8, top_p=0.95)

#llm = LLM(model="Qwen/Qwen2.5-Coder-3B-Instruct", tensor_parallel_size=2, dtype="float16", quantization="fp8", enforce_eager=True, max_num_seqs=2, gpu_memory_utilization=0.8, swap_space=4)
#llm = LLM(model="Qwen/Qwen2.5-Coder-3B-Instruct", tensor_parallel_size=2, enforce_eager=True, max_num_seqs=2, gpu_memory_utilization=0.8, swap_space=4, cpu_offload_gb=0, quantization="bitsandbytes", load_format="bitsandbytes",)
llm = LLM(model="facebook/opt-125m")
#outputs = llm.chat(prompts, sampling_params)
outputs = llm.generate(prompts, sampling_params)

for output in outputs:
    prompt = output.prompt
    generated_text = output.outputs[0].text
    print(f"Prompt: {prompt!r}, Generated text: {generated_text!r}")


-----------------------------------------------------------------------------------------------------------------------
from vllm import LLM, SamplingParams
import torch.distributed as dist
import os
os.environ ['VLLM_USE_V1'] ='1'

prompts = [
    "Hello, my name is",
    "The president of the United States is",
    "The capital of France is",
    "The future of AI is",
]
sampling_params = SamplingParams(temperature=0.8, top_p=0.95)
llm = LLM(model="Qwen/Qwen2.5-3B-Instruct", tensor_parallel_size=2, enforce_eager=True, gpu_memory_utilization=0.9, max_model_len=10000)
outputs = llm.generate(prompts, sampling_params)

for output in outputs:
    prompt = output.prompt
    generated_text = output.outputs[0].text
    print(f"Prompt: {prompt!r}, Generated text: {generated_text!r}")

if dist.is_initialized():
    dist.destroy_process_group()
    
'''