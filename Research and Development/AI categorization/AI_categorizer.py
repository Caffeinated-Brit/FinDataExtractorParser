# FIRST INSTALL DEPENDENCIES:
    # pip install transformers
    # pip install spacy
    # pip install pandas
    # pip install pydantic

from transformers import pipeline
import spacy
import pandas as pd

# Load a classification pipeline (for example, DistilBERT)
classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")

# Load spaCy model for named entity recognition
nlp = spacy.load("en_core_web_sm")

def categorize_text(text):
    return classifier(text)

def extract_entities(text):
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]

# Example Data Processing
def process_and_categorize_data(extracted_data):
    df = pd.DataFrame(extracted_data)
    df['category'] = df['text'].apply(lambda x: categorize_text(x))
    df['entities'] = df['text'].apply(lambda x: extract_entities(x))
    return df.to_dict(orient="records")
