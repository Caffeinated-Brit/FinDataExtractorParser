# https://pypi.org/project/llama-parse/
# pip install -U llama-index --upgrade --no-cache-dir --force-reinstall
# pip install llama-cloud-services

import nest_asyncio
from dotenv import load_dotenv
load_dotenv()


nest_asyncio.apply()

from llama_cloud_services import LlamaParse

parser = LlamaParse(
    # api_key='LLAMA_CLOUD_API_KEY',  # can also be set in your env as LLAMA_CLOUD_API_KEY
        # NOTE
        # llamaParse service uses credits, you get 10000 free a month. Takes about 1 credit a page parsed.
    result_type="text",  # "markdown" and "text" are available
    num_workers=4,  # if multiple files passed, split in `num_workers` API calls
    verbose=True,
    language="en",  # Optionally you can define a language, default=en
)

# sync
# documents = parser.load_data("./2021_2_Statement_removed.pdf")
#
# print(documents)


file_name = "2021_2_Statement_removed.pdf"
extra_info = {"file_name": file_name}

with open(f"./{file_name}", "rb") as f:
    # must provide extra_info with file_name key with passing file object
    documents = parser.load_data(f, extra_info=extra_info)

# # you can also pass file bytes directly
# with open(f"./{file_name}", "rb") as f:
#     file_bytes = f.read()
#     # must provide extra_info with file_name key with passing file bytes
#     documents = parser.load_data(file_bytes, extra_info=extra_info)

with open("llamaParseOutput.txt", "w") as f:
    for doc in documents:
        f.write(doc.text + "\n")
    print("output to llamaParseOutput.txt")
