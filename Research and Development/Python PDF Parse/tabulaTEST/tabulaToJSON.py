# FIRST INSTALL DEPENDENCIES:
#   pip install tabula-py
#   pip install JPype1
 
# Can convert a pdf strait to json
    # delete output file before testing to ensure new output file

# This is the newest top contender to start our extraction with then use more json tools such as: jsonschema, jsonpath-ng, and others
    # could use 

import tabula

file_path = "Research and Development/Python PDF Parse/examplePDFs/f1040.pdf"

output_path = "Research and Development/Python PDF Parse/tabulaTEST/outputs/tabulaToJsonOutput.json"

# Convert PDF tables directly into JSON
tabula.convert_into(file_path, output_path, output_format="json", pages="all")

print(f"Data extracted to {output_path} in JSON format.")
