import configparser

def load_config(config_path="config.ini"):
    config = configparser.ConfigParser()
    config.read(config_path)
    return {
        "parser": config.get("Parser", "method", fallback="pdfPlumber"),
        "ocrFallback": config.get("OCR", "fallback", fallback="pyTesseract"),
        "ai": config.get("AI", "method", fallback="Ollama/Schema"),
        "ollama_model": config.get("Ollama Model", "model", fallback="qwen2.5-coder:3b"),
        "reruns": config.get("Verification", "reruns", fallback=3),
        "threshold": float(config.get("Verification", "threshold", fallback=0.9))
    }
