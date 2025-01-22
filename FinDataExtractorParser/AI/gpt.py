# MAIN DEPENDENCIES - need added to requirements.txt
# pip install langchain
# pip install langchain_community
# pip install openai 
# pip install python-dotenv
# pip install pypdfium2

from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv

# loads the .env file api key
load_dotenv()

# Structure into JSON given text with an LLM (currently chatgpt model:"gpt-3.5-turbo-1106")
def extract_structured_data(prompt):
    print("Throwing to gpt api...")
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-1106")

    promptTemplate = PromptTemplate(
        template=prompt,
    )

    chain = LLMChain(llm=llm, prompt=promptTemplate)
    return chain.run(content=promptTemplate) 

# def main():
#     print(extract_structured_data("give 3 random space facts"))

# if __name__ == "__main__":
#     main()
