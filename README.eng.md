# PDFSmartRename

PDFSmartRename is a tool that automatically renames PDF files using OCR and AI technology.

## Features

- Extracts text from the first page of a PDF using PyMuPDF.
- Uses Tesseract OCR to extract text from images if necessary.
- Generates a new file name using the Gemini API based on the extracted text.
- Renames the PDF file with the generated title.

## Installation

1. Install the required Python libraries:
   ```bash
   pip install fitz pillow pytesseract requests
   ```

2. Install Tesseract-OCR on your system. If it's not installed in the default path, you may need to specify its path in the script:
   ```python
   pytesseract.pytesseract.tesseract_cmd = r'<full_path_to_your_tesseract_executable>'
   ```

3. Obtain an API key for the Gemini API.

## Usage

1. Set the `directory_path` variable in the script to the directory containing your PDF files.
2. Set the `your_api_key` variable to your Gemini API key.
3. Run the script to rename all PDF files in the specified directory.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more information.
