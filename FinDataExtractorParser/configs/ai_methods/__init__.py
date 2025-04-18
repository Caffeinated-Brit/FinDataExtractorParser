from AI import Ollama, gpt
from benchmarks import Ollama_verification

# from AI import Vllm, gpt  # Future extensions
# outdated/worse methods: llama

ai_methods = {
    "Ollama": Ollama.process_text_with_llm,
    "Ollama/Schema": Ollama.process_text_with_llm_and_schema,
    "gpt": gpt.extract_structured_data,
    "Ollama/Verification": Ollama.process_text_with_llm_and_verification,
    # "vllm": Vllm.process_text_with_llm,
    # "llama": llama.process_text_with_llm,
}
