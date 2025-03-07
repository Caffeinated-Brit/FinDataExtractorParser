# https://github.com/nlmatics/llmsherpa
# pip install llmsherpa
# NOTE
# does not support OCR, requires text layer to operate

from llmsherpa.readers import LayoutPDFReader

# llmsherpa_api_url = "https://readers.llmsherpa.com/api/document/developer/parseDocument?renderFormat=all"
llmsherpa_api_url = "http://localhost:5010/api/parseDocument?renderFormat=all"
pdf_url = "2021_2_Statement_removed.pdf" # also allowed is a file path e.g. /home/downloads/xyz.pdf
pdf_reader = LayoutPDFReader(llmsherpa_api_url)
doc = pdf_reader.read_pdf(pdf_url)
# print(doc.to_html())
# print(doc.to_text())
# print(doc.json)

with open("sherpaOutput.txt", "w") as f:
    f.write(doc.to_text() + "\n")
    print("output to sherpaOutput.txt")
