# FIRST INSTALL DEPENDENCIES:
#   pip install tabula-py
 
# essentually parses everything as a table\
    # uses dataframes, could be usefull with pandas or other libraries to further clense

import tabula

tables = tabula.read_pdf("Research and Development/Python PDF Parse/examplePDFs/f1040.pdf", pages="all", multiple_tables=True)
for table in tables:
    print(table)  # Each table is a DataFrame
