# Python PDF Stripping and AI Research and Development

## Python Version 3.10
Python version 3.10 provides for the most library compatablilty esspesially for the PDF and AI libraries useful to us.

3.10 still recieves occasional updates making this version incredibly stable.
    
# PDF 

## pdfplumber
* Strengths: Excellent for handling complex layouts, tables, and extracting both text and specific coordinates. It allows precise extraction of tables and structured information.
* Recommended Use: Parse structured elements like tables, fields, and labels in tax forms.
* Example (untested):
    ```python 
    import pdfplumber

    with pdfplumber.open("1040_tax_form.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        # Optionally, extract tables
        tables = page.extract_table()
        print(text)
        print(tables)
    ```

## Camelot or Tabula-py (for Advanced Table Extraction)

* Strengths: Specialized for table extraction, crucial for financial documents with well-structured tables.
* Recommended Use: Specifically for extracting tabular data, where data points are clearly separated.
* Example (untested):
    ```python
    import camelot

    tables = camelot.read_pdf("1040_tax_form.pdf", pages='all')
    for table in tables:
        print(table.df)  # Returns the table as a DataFrame

    ```
<br>

# *** Highly Recommended *** 
## PDFMiner.six (for Detailed Layout Parsing)
* Strengths: Good for understanding the layout, retrieving coordinates, and extracting specific fields from forms.
* Recommended Use: Targeted field extraction, especially when specific form field locations are known (like "Income" or "Taxable Income").
* Example (untested):
    ```python
    from pdfminer.high_level import extract_text

    text = extract_text("1040_tax_form.pdf")
    print(text)

    ```

## Tesseract OCR (with pdf2image for Scanned PDFs)
* Strengths: Necessary if the financial documents are scans or images rather than text-based PDFs.
* Recommended Use: Use in combination with pdfplumber for scanned documents to convert images into text.
* Example (untested):
    ```python
    from pdf2image import convert_from_path
    import pytesseract
    
    images = convert_from_path("1040_tax_form.pdf")
    text = ""
    for image in images:
        text += pytesseract.image_to_string(image)
    print(text)
    ```
### Potential library combination
* **pdfplumber**: Start with pdfplumber to extract both text and tables.
* **Camelot or Tabula-py**: Use alongside if tables require finer handling.
* **Tesseract**: For scanned documents, pair it with pdf2image to capture text from images.

Scanned documents will take longer to parse with tesseract. I suggest we look further into pdfminer.six as from our small tests it seems to parse in the most organized way. All of them should be considered and a deeper dive on eaches features is required.

# AI

## Scikit-Learn
* Use Case: A versatile library for building traditional machine learning models (e.g., classifiers, regressors) on structured data.
* Recommended Algorithms: Logistic Regression, Decision Trees, Support Vector Machines (SVM), and Gradient Boosting for structured data analysis and categorization.
* Example (untested):
    ```python
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split

    X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2)
    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    ```

## SpaCy
* Use Case: Ideal for processing natural language from PDFs, such as field names or descriptive fields.
* Features: Named Entity Recognition (NER), Part-of-Speech tagging, and dependency parsing.
* Example (untested):
    ```python
    import spacy

    nlp = spacy.load("en_core_web_sm")
    doc = nlp("Sample income data extracted from a form")
    for entity in doc.ents:
        print(entity.text, entity.label_)
    ```

## TensorFlow/Keras
* Use Case: Best for building and training deep learning models, especially if you want to experiment with neural networks.
* Recommended Models: Feedforward neural networks for structured data or BERT-based models if you have a lot of unstructured text data.
* Example (untested):
    ```python
    import tensorflow as tf

    model = tf.keras.Sequential([
        tf.keras.layers.Dense(128, activation='relu', input_shape=(input_shape,)),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(num_classes, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    model.fit(X_train, y_train, epochs=10)
    ```

## Hugging Face Transformers
* Use Case: Advanced NLP tasks, especially if you have a lot of text and need accurate semantic understanding.
* Recommended Models: BERT, RoBERTa, or DistilBERT models, pre-trained and fine-tuned for financial text.
* Example (untested):
    ```python
    from transformers import pipeline

    classifier = pipeline("text-classification", model="distilbert-base-uncased")
    result = classifier("Extracted text from 1040 form")
    print(result)

    ```
##  NLTK (Natural Language Toolkit)
* Use Case: Basic NLP tasks such as text cleaning, tokenization, and keyword extraction.
* Features: Good for preprocessing text data before classification or entity recognition.
* Example (untested):
    ```python
    from nltk.tokenize import word_tokenize
    text = "Sample text data"
    tokens = word_tokenize(text)
    ```

## PyTorch
* Use Case: Highly flexible for deep learning models and experimentation, especially with custom models.
* Recommended Models: BERT, GPT for text analysis, or CNNs/RNNs for structured and unstructured data.
* Example (untested):
    ```python
    import torch
    import torch.nn as nn
    
    class SimpleModel(nn.Module):
        def __init__(self):
            super(SimpleModel, self).__init__()
            self.fc = nn.Linear(input_size, num_classes)
    
        def forward(self, x):
            return self.fc(x)
    
    model = SimpleModel()

    ```
# Potential AI workflow
* **Preprocess** the data: Use NLTK and SpaCy to clean and organize text.
* **Classification Model**: Scikit-Learn for a quick traditional classifier or TensorFlow/PyTorch for deep learning approaches.
* **For complex text**: Hugging Face Transformers provides powerful pre-trained models for high accuracy on unstructured text data.

If all goes well with the PDF extraction not much preprocessing should be needed. The main AI task should be the classification model.
