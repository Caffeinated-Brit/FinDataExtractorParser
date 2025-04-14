# go to the ollama github page download for windows
# to download the model find it on ollama's site(https://ollama.com/search) and in the command line run "ollama run "name of model""
# example of getting a model "ollama run llama3.1:8b"
# dont forget to type the size of the model in addition to the name
import difflib
import time
from concurrent.futures import ThreadPoolExecutor

#tested models
#llama3.1:8b works well
#qwen2.5:14b works very very well giving basically only valid json on its own
#llama3.2:3b sucks
#qwen2.5-coder:3b great amazing, as far as tested as good as qwen2.5:14b though I dont expect it to keep up with more advanced pdfs

import ollama
from pydantic import BaseModel, Extra, Field

#LLM_MODEL="llama3.1:8b"
#LLM_MODEL="qwen2.5:14b"
#LLM_MODEL="qwen2.5-coder:3b" # for lukas' backpack brick
LLM_MODEL="qwen2.5-coder:7b" # for spencers spacestation

class CompanyInfo(BaseModel):
    name: str
    address: str
    phone_number: str
    email: str
    website: str

class PersonalInfo(BaseModel):
    name: str
    address: str
    phone_number: str
    email: str
    bank_account_number: str

class FinancialData(BaseModel):
    personal_Info: PersonalInfo
    company_Info: CompanyInfo
    financial_info: dict = Field(..., description="This is where the financial data will go")

    class Config:
        extra = 'allow'  # Allow extra fields to be added by Ollama

def process_text_with_llm_OLD(user_prompt):
    print("Starting Ollama extraction...")
    response = ollama.chat(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": user_prompt}],
        options={"seed": 1, "temperature":0},
        # auto formats output into json, going to keep messing with this and other parameters
        format="json"
    )
    #This returns just the message from the LLM nothing else
    return response.message.content

def process_text_with_llm_and_schema(user_prompt):
    print("Starting Ollama extraction with a json schema...")
    start_time = time.time()
    response = ollama.chat(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": user_prompt}],
        options={"seed": 1, "temperature":0, "top_k":1},
        # auto formats output into json, going to keep messing with this and other parameters
        format=FinancialData.model_json_schema()
    )
    #This returns just the message from the LLM nothing else
    #print(response.message.content)
    #return response.message.content

    end_time = time.time()
    elapsed_time = end_time - start_time

    generated_tokens = response['eval_count']
    content = response['message']['content']

    return content, generated_tokens, elapsed_time

def process_text_with_llm(prompt, keep_alive=True, retries=3, threshold=0.95):
    print("Starting Ollama extraction")
    start_time = time.time()

    response = ollama.chat(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        options={"seed": 42, "temperature":0.9, "top_p":1},
        keep_alive=keep_alive
    )
    end_time = time.time()
    elapsed_time = end_time - start_time

    generated_tokens = response['eval_count']
    content = response['message']['content']

    return content, generated_tokens, elapsed_time


# Not Currently in use
def generate_checked_text3(prompt, retries=3, threshold=0.50):
    results = []
    for r in range(retries):
        output = process_text_with_llm_and_schema(prompt)
        results.append(output)

    print(results)
    # Compare pairwise similarity
    for i in range(len(results)):
        #print(results[0][i])
        for j in range(i + 1, len(results)):
            ratio = difflib.SequenceMatcher(None, results[i], results[j]).ratio()
            print("RATIO: ")
            print(ratio)
            if ratio > threshold:
                print(f"Matched outputs with similarity {ratio:.2f}")
                return results[i]

    print("No sufficiently similar outputs found, defaulting to first.")
    return results[0]


def run_parallel_requests(num_requests, prompt):
    results = []
    with ThreadPoolExecutor(max_workers=num_requests) as executor:
        futures = []
        for i in range(num_requests):
            futures.append(executor.submit(process_text_with_llm_and_schema, prompt))

        for future in futures:
            print(future.result())
            print("-" * 50)
            results.append(future.result())

    return results

def run_benchmarking(num_requests, prompt, keep_alive=False):
    loaded = process_text_with_llm("Load model into memory before benchmarking.", keep_alive)
    start_time = time.time()
    print(f"Running {num_requests} parallel requests:")
    results = run_parallel_requests(num_requests, prompt)
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Total time for {num_requests} requests: {end_time - start_time} seconds")
    return results, total_time

#run_benchmarking(30)

if __name__ == "__main__":
    prompt = (
        f"The following text was extracted from a PDF.\n"
        "Extract and categorize the data from the text. Return as JSON.\n"
        f"Text:\n"
    )
    print(prompt)
    print(process_text_with_llm(prompt +""" test text here """))