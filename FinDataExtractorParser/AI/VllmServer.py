import signal
import subprocess
import threading
import time
import torch
import os

os.environ['VLLM_USE_V1'] = '1'

num_gpus = torch.cuda.device_count()

def start_vllm_server(shutdown_event):
    try:
        command = [
            'nohup', 'vllm', 'serve', 'Qwen/Qwen2.5-7B-Instruct-GPTQ-Int8',
            '--gpu_memory_utilization=0.9',
            '--tensor_parallel_size=' + str(num_gpus),
            '--enforce_eager',
            '--max_num_seqs=80',
            '--max_model_len=11000',
        ]
        print("Starting vLLM server...")
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        while not shutdown_event.is_set():
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())


        if shutdown_event.is_set():
            print("Shutdown event triggered, stopping vLLM server...")
            process.send_signal(signal.SIGINT)  # Gracefully stop the process
            stdout, stderr = process.communicate()
            if stdout:
                print(stdout.strip())
            if stderr:
                print(stderr.strip())

        return process
    except Exception as e:
        print(f"Error starting vLLM server: {e}")
        return None

def stop_vllm_server(process):
    if process:
        print("Stopping vLLM server...")
        process.send_signal(signal.SIGINT)
        stdout, stderr = process.communicate()
        print("vLLM server stopped.")
        if stderr:
            print(f"Error during shutdown: {stderr.strip()}")
    else:
        print("No running vLLM server to stop.")

if __name__ == "__main__":
    shutdown_event = threading.Event()

    try:
        server_thread = threading.Thread(target=start_vllm_server, args=(shutdown_event,))
        server_thread.start()
        time.sleep(60)
        print("vLLM server is running. Press Ctrl+C to stop.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nCtrl+C received. Shutting down...")
        shutdown_event.set()
        server_thread.join()
        print("Server has been shut down.")