import subprocess

from unittest.mock import patch
from PDFparsers.linuxTest import linuxParse

def test_linuxParse_success(tmp_path):
    # temp pdf file for test
    test_pdf = tmp_path / "test.pdf"
    test_pdf.write_bytes(b"%PDF-1.4 Test PDF Content")

    # mock subprocess.run to get a success
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = None  # good run without error

        linuxParse(str(test_pdf))

        # subprocess.run called with correct command
        mock_run.assert_called_once_with(
            ["pdftotext", "-layout", str(test_pdf)], check=True
        )

def test_linuxParse_error(tmp_path):
    # temp pdf file for test
    test_pdf = tmp_path / "test.pdf"
    test_pdf.write_bytes(b"%PDF-1.4 Test PDF Content")

    # mock subprocess.run to get an error
    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = subprocess.CalledProcessError(1, "pdftotext")

        linuxParse(str(test_pdf))

        # subprocess.run called with correct command
        mock_run.assert_called_once_with(
            ["pdftotext", "-layout", str(test_pdf)], check=True
        )
