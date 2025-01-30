import subprocess

input_pdf = "FinDataExtractorParser/examplePDFs/fromCameron/2021_2_Statement_removed.pdf"
output_txt = "FinDataExtractorParser/PDFparsers/linux/output.txt"

command = ["pdftotext", "-layout", input_pdf, output_txt]

# Execute the command
try:
    subprocess.run(command, check=True)
    print(f"Text extracted to: {output_txt}")
except subprocess.CalledProcessError as e:
    print(f"An error occurred: {e}")

