# go to the ollama github page download for windows
# to download the model find it on ollama's site(https://ollama.com/search) and in the command line run "ollama run "name of model""
# example of getting a model "ollama run llama3.1:8b"
# dont forget to type the size of the model in addition to the name


#tested models
#llama3.1:8b works well
#qwen2.5:14b works very very well giving basically only valid json on its own
#llama3.2:3b sucks
#qwen2.5-coder:3b great amazing, as far as tested as good as qwen2.5:14b though I dont expect it to keep up with more advanced pdfs

import ollama

#LLM_MODEL="llama3.1:8b"
#LLM_MODEL="qwen2.5:14b"
LLM_MODEL="qwen2.5-coder:7b"

def process_text_with_llm(prompt):
    print("Starting Ollama extraction")
    response = ollama.chat(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        options={"seed": 1, "temperature":0}
    )
    #This returns just the message from the LLM nothing else
    return response.message.content
