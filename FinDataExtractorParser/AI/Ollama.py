# go to the ollama github page download for windows
# to download the model find it on ollama's site(https://ollama.com/search) and in the command line run "ollama run "name of model""
# example of getting a model "ollama run llama3.1:8b"
# dont forget to type the size of the model in addition to the name
import json

#tested models
#llama3.1:8b works well
#qwen2.5:14b works very very well giving basically only valid json on its own
#llama3.2:3b sucks
#qwen2.5-coder:3b great amazing, as far as tested as good as qwen2.5:14b though I dont expect it to keep up with more advanced pdfs

#LLM_MODEL="llama3.1:8b"
#LLM_MODEL="qwen2.5:14b"
# LLM_MODEL="qwen2.5-coder:7b"
# LLM_MODEL="qwen2.5-coder:3b"
import configparser

import ollama

config = configparser.ConfigParser()
config.read("config.ini")
LLM_MODEL =  config.get("Ollama Model", "model", fallback="qwen2.5-coder:3b")

# LLM_MODEL="qwen2.5-coder:3b" # for lukas' backpack brick
# #LLM_MODEL="qwen2.5-coder:7b" # for spencers spacestation

# should probably move this to a different file
def schema_json_convertion(schema):
    """ schema_json_convertion converts a schema to a useable (dict) json schema.

    Args:
        schema(many): schema to convert, either string, dict or pydantic model.

    Returns:
        (dict) string of json schema.
    """
    try:
        if isinstance(schema, str):
            return json.loads(schema)
        elif isinstance(schema, dict):
            return schema
        else:
            # Assume it's a Pydantic model and get its JSON schema
            return schema.model_json_schema()
    except json.JSONDecodeError as e:
        print("Failed to decode JSON:", e)
        return None
    except Exception as e:
        print("Error processing schema:", e)
        return None

def process_text_with_llm_and_schema(user_prompt, schema):
    """ process_text_with_llm_and_schema runs a prompt through the ollama model with a json schema.

            Args:
                user_prompt(str): prompt to run through the model.
                schema(many): Json schema to convert, either string, dict or pydantic model.

            Returns:
                (str) response from the model.
        """
    schema_json = schema_json_convertion(schema)

    print("Starting Ollama extraction with a json schema...")
    try:
        response = ollama.chat(
            model=LLM_MODEL,
            messages=[{"role": "user", "content": user_prompt}],
            options={"seed": 1, "temperature":0.1, "top_k":1},
            # auto formats output into json, going to keep messing with this and other parameters
            #format=FinancialData.model_json_schema()
            format = schema_json
        )
    except Exception as e:
        print("Error processing schema, schema may be invalid:", e)
        raise e
    return response.message.content

def process_text_with_llm(user_prompt):
    """ process_text_with_llm runs a prompt through the ollama model.

        Args:
            user_prompt(str): prompt to run through the model.

        Returns:
            (str) response from the model.
    """
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

# def run_parallel_requests(num_requests, prompt):
#     results = []
#     with ThreadPoolExecutor(max_workers=num_requests) as executor:
#         futures = []
#         for i in range(num_requests):
#             futures.append(executor.submit(process_text_with_llm, prompt))
#
#         for future in futures:
#             print(future.result())
#             print("-" * 50)
#             results.append(future.result())
#     return results
#
# def run_parallel_requests_with_schema(num_requests, prompt, schema):
#     results = []
#     with ThreadPoolExecutor(max_workers=num_requests) as executor:
#         futures = []
#         for i in range(num_requests):
#             futures.append(executor.submit(process_text_with_llm_and_schema, prompt, schema))
#
#         for future in futures:
#             print(future.result())
#             print("-" * 50)
#             results.append(future.result())
#     return results

if __name__ == "__main__":
    prompt = (
        f"The following text was extracted from a PDF.\n"
        "Extract and categorize the data from the text. Return as JSON.\n"
        f"Text:\n")

    # print(prompt)
    # # print(process_text_with_llm(prompt +""" test text here """))