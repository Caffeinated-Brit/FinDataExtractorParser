'''
from vllm import LLM, SamplingParams

import os
os.environ ['CUDA_LAUNCH_BLOCKING'] ='1'


#prompts = [[{"role": "user", "content": "Who are you?"}]]
prompts = ["Who are you?"]

sampling_params = SamplingParams(temperature=0.8, top_p=0.95)

#llm = LLM(model="Qwen/Qwen2.5-Coder-3B-Instruct", tensor_parallel_size=2, dtype="float16", quantization="fp8", enforce_eager=True, max_num_seqs=2, gpu_memory_utilization=0.8, swap_space=4)
#llm = LLM(model="Qwen/Qwen2.5-Coder-3B-Instruct", tensor_parallel_size=2, enforce_eager=True, max_num_seqs=2, gpu_memory_utilization=0.8, swap_space=4, cpu_offload_gb=0)
llm = LLM(model="facebook/opt-125m")
#outputs = llm.chat(prompts, sampling_params)
outputs = llm.generate(prompts, sampling_params)

for output in outputs:
    prompt = output.prompt
    generated_text = output.outputs[0].text
    print(f"Prompt: {prompt!r}, Generated text: {generated_text!r}")
'''
from vllm import LLM, SamplingParams
import torch.distributed as dist
prompts = [
    "Hello, my name is",
    "The president of the United States is",
    "The capital of France is",
    "The future of AI is",
]
sampling_params = SamplingParams(temperature=0.8, top_p=0.95)
llm = LLM(model="Qwen/Qwen2.5-3B-Instruct", quantization="bitsandbytes", load_format="bitsandbytes")
outputs = llm.generate(prompts, sampling_params)

for output in outputs:
    prompt = output.prompt
    generated_text = output.outputs[0].text
    print(f"Prompt: {prompt!r}, Generated text: {generated_text!r}")

if dist.is_initialized():
    dist.destroy_process_group()