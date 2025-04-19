from AI import Ollama, gpt, Vllm

# from AI import Vllm, gpt  # Future extensions
# outdated/worse methods: llama

ai_methods = {
    "Ollama": Ollama.run_parallel_requests,
    "Ollama/Schema": Ollama.run_parallel_requests_with_schema,
    "gpt": gpt.extract_structured_data,
    "vllm": Vllm.process_text_with_llm,
    # "llama": llama.process_text_with_llm,
}
