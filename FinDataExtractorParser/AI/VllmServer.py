import subprocess
import time
import torch
import os

os.environ['VLLM_USE_V1'] = '1'

LLM_MODEL = 'Qwen/Qwen2.5-Coder-3B-Instruct'
# LLM_MODEL = 'deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B'
num_gpus = torch.cuda.device_count()

def start_vllm_server():
    try:
        command = [
            'nohup', 'vllm', 'serve', 'Qwen/Qwen2.5-Coder-3B-Instruct',
            '--gpu_memory_utilization=0.9',
            '--tensor_parallel_size=' + str(num_gpus),
            '--enforce_eager',
            '--max_model_len=10000',
        ]

        command2 = [
            'nohup', 'vllm', 'serve', 'Qwen/Qwen2.5-7B-Instruct-GPTQ-Int8',
            '--gpu_memory_utilization=0.9',
            '--tensor_parallel_size=' + str(num_gpus),
            '--enforce_eager',
            '--max_num_seqs=80',
            '--max_model_len=10000',
        ]

        command3 = [
            'nohup', 'vllm', 'serve', 'deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B',
            '--gpu_memory_utilization=0.9',
            '--tensor_parallel_size=' + str(num_gpus),
            '--enforce_eager',
            '--max_num_seqs=80',
            '--max_model_len=10000',
        ]

        print("Starting vLLM server...")
        process = subprocess.Popen(
            command2,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Print output in real-time
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())

        # Capture any remaining output after the process ends
        stdout, stderr = process.communicate()
        if stdout:
            print(stdout.strip())
        if stderr:
            print(stderr.strip())

        return process
    except Exception as e:
        print(f"Error starting vLLM server: {e}")
        return None

start_vllm_server()