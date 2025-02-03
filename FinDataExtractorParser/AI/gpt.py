from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnableSequence
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# loads the .env file api key
load_dotenv()

# Structure into JSON given text with an LLM (currently chatgpt model:"gpt-3.5-turbo-1106")
def extract_structured_data(prompt, page_number=None):
    # print("Throwing to gpt api...")
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-1106")

    # Handle the template properly based on whether page_number is provided
    if page_number is not None:
        prompt_text = f"Page {page_number}: {prompt}"
    else:
        prompt_text = prompt

    prompt_template = PromptTemplate(
        input_variables=["input"],
        template="{input}"
    )

    sequence = RunnableSequence(first=prompt_template, last=llm)

    # Invoke with appropriate input
    return sequence.invoke({"input": prompt_text})
