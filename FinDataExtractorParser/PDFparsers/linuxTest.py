# Ensure that you have a Linux environment setup in WSL
# apt install poppler-utils (run this in WSL)

import subprocess

def linuxParse(input_pdf):
    command = ["pdftotext", "-layout", input_pdf]

    # Execute the command
    try:
        subprocess.run(command, check=True)
        outputfile = input_pdf.replace(".pdf",".txt")
        print(f"Text extracted to: {outputfile}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")