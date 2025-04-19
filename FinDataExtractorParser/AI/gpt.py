from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain.schema.runnable import RunnableSequence
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# loads the .env file api key
load_dotenv()

# Function to structure output as JSON using JsonOutputParser
def extract_structured_data(prompt, page_number=None):
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-1106")
    parser = JsonOutputParser()

    # Optional: prepend page number
    if page_number is not None:
        prompt_text = f"Page {page_number}: {prompt}"
    else:
        prompt_text = prompt

    prompt_template = PromptTemplate(
        template="{input}\n{format_instructions}",
        input_variables=["input"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    # sequence = RunnableSequence(first=prompt_template, last=llm)

    sequence = prompt_template | llm | parser
    return sequence.invoke({"input": prompt_text})

if __name__ == "__main__":
    print(extract_structured_data("Give me 3 space facts in JSON format."))
