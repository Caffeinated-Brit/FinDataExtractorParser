# Ensure that you have a Linux environment setup in WSL
# run this in WSL: "apt install poppler-utils"

import subprocess

def linuxParse(input_pdf):
    command = ["pdftotext", "-layout", input_pdf]

    # Execute the command
    try:
        subprocess.run(command, check=True)
        outputfile = input_pdf.replace(".pdf",".txt")
        print(f"Text extracted to: {outputfile}")
        # return outputfile
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    linuxParse("C:/Users/lukas/Desktop/Capstone/FinDataExtractorParser/FinDataExtractorParser/examplePDFs/fromCameron/schwab.pdf")
    # linuxParse("examplePDFs/fromCameron/2021_2_Statement_removed.pdf")