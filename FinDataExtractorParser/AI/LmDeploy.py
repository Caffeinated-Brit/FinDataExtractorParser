from lmdeploy import pipeline, PytorchEngineConfig
import torch
from torch.distributed._composable.replicate import DDP
from torch.nn import DataParallel
from lmdeploy import pipeline, TurbomindEngineConfig
torch.cuda.empty_cache()
torch.cuda.memory_summary()
#pipe = pipeline('Qwen/Qwen2.5-Coder-3B-Instruct', device='cpu')

print("Number of GPUs available:", torch.cuda.device_count())
for i in range(torch.cuda.device_count()):
    print(f"GPU {i}: {torch.cuda.get_device_name(i)}")

#LLM_MODEL="Qwen/Qwen2.5-7B-Instruct-1M"
LLM_MODEL="Qwen/Qwen2.5-Coder-3B-Instruct"

def process_text_with_llm(prompt):
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

def process_text_with_llm2(prompt):
    print("Starting LmDeploy extraction with " + LLM_MODEL)
    pipe = pipeline(LLM_MODEL,
                    backend_config=TurbomindEngineConfig(
                        max_batch_size=4,
                        enable_prefix_caching=False,
                        cache_max_entry_count=0.8,
                        session_len=512,
                        tp=1
                    ),
                    device = "cuda"
                    )
    response = pipe([prompt])
    #print(response[0].text)
    return response[0].text

#print(process_text_with_llm("Please write me an essay about bees."))
