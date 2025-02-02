import subprocess

def linuxParse(input_pdf, outputFile):
    # input_pdf = "FinDataExtractorParser/examplePDFs/fromCameron/2021_2_Statement_removed.pdf"
    output_txt = "FinDataExtractorParser/PDFparsers/linux/output.txt"
    command = ["pdftotext", "-layout", input_pdf, outputFile]

    # Execute the command
    try:
        subprocess.run(command, check=True)
        print(f"Text extracted to: {output_txt}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

