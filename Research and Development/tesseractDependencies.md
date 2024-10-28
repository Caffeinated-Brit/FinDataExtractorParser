# Tesseract Dependencies
Following instructions are for windows

# Install Poppler and Tesseract

## Poppler
- Go to https://github.com/oschwartz10612/poppler-windows/releases/
- Download latest versions zip file
    - Version tested: `Release 24.08.0-0.zip`
- Unzip/Extract All onto your local machine in a permanent location.
    - Ex. I unziped to: `C:\Users\lukas\poppler`
    - Naviagate to the bin folder
        - Ex. My bin folder: `C:\Users\lukas\poppler\poppler-24.08.0\Library\bin`
    - Copy your file path to the bin folder
- Add as PATH enviornment variable
    - Paste this file path into your systems enviornment variables as a new path
        - See end of page on how to add enviornment variables
- Ensure install
    - Close/Restart IDE and terminals
    - Run `pdfinfo -v` in a new terminal
        - This should show installation information 


## Tesseract
- Go to https://github.com/UB-Mannheim/tesseract
- Download latest Release (in the right column)
    - Version tested: `v5.4.0.20240606`
- Follow the installer
- Copy the installation file path
    - Default file path: `C:\Program Files\Tesseract-OCR`
- Add as PATH enviornment variable
    - Paste this file path into your systems enviornment variables as a new path
        - See end of page on how to add enviornment variables
- Ensure install
    - Close/Restart IDE and terminals
    - Run `tesseract -v` in a new terminal
        - This should show installation information 

<br>

## How to add PATH enviornment variables
- Open start menu
- Type: `enviornment variables` and choose `Edit the system enviornment variables`
- Choose `Enviornment Variables...`
- Select `Path` row in the top section
- Select `Edit...` in the top section
- Select `New`
- Paste or type your file path
- Choose `OK`

<br>

