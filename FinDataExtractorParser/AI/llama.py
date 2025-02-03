# pip install llama-cpp-python
# use the download_llm.py file to download the LLM that is listed in LLAMA_MODEL_PATH

from llama_cpp import Llama

# Constants
# LLAMA_MODEL_PATH = "LLMs/Meta-Llama-3.1-8B-Instruct-Q5_K_L.gguf"
# LLAMA_MODEL_PATH = "LLMs/Meta-Llama-3.1-8B-Instruct-Q8_0.gguf"
LLAMA_MODEL_PATH = "LLMs/mistral-7b-instruct-v0.2.Q6_K.gguf"
# "FinDataExtractorParser\LLMs\mistral-7b-instruct-v0.2.Q6_K.gguf"

# Initialize the Llama model
llm = Llama(
    model_path=LLAMA_MODEL_PATH,
    n_ctx=2048,  # Maximum context size for the model
    n_threads=8,  # Number of CPU threads
    n_gpu_layers=15  # Layers to assign to GPU. Start small (10), increase until approaching VRAM limit
)

def process_text_with_llm(prompt):
    # Add temperature and top_p for controlled, non-hallucinatory output
    print("Starting llama extraction")
    response = llm(
        prompt,
        max_tokens=1024,  # More tokens = longer outputs capability
        temperature=0.1,
        top_p=1,
        top_k=1
        # All these variables aim to reduce randomness
        # For a visualization, refer to https://artefact2.github.io/llm-sampling/index.xhtml
    )
    return response["choices"][0]["text"].strip()
