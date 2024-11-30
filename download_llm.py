import os
import requests
from tqdm import tqdm

BASE_DIR = "FinDataExtractorParser/LLMs"
MODEL_URL = "https://huggingface.co/TheBloke/finance-llm-gguf/resolve/main/finance-llm.Q4_K_M.gguf"
MODEL_FILE = "finance-llm.Q4_K_M.gguf"


def create_directory(path): # If it doesn't already exist
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")
    else:
        print(f"Directory already exists: {path}")


def download_file(url, output_path): # Uses a pretty progress bar lol
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        total_size = int(response.headers.get('content-length', 0))
        with open(output_path, "wb") as file, tqdm(
                desc=f"Downloading {os.path.basename(output_path)}",
                total=total_size,
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
        ) as progress:
            for data in response.iter_content(chunk_size=1024):
                file.write(data)
                progress.update(len(data))
        print(f"File downloaded successfully: {output_path}")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")


def main():
    print("Starting LLM setup...")

    create_directory(BASE_DIR)

    output_path = os.path.join(BASE_DIR, MODEL_FILE)
    if not os.path.exists(output_path):
        print(f"Downloading model from {MODEL_URL}")
        download_file(MODEL_URL, output_path)
    else:
        print(f"Model already exists at {output_path}")


if __name__ == "__main__":
    main()
