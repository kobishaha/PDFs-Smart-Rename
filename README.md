# PDFs-Smart-Rename
PDFSmartRename is a tool that automatically renames PDF files using OCR and AI technology. It extracts text from the first page of a PDF file, generates an appropriate file title using the Gemini API, and renames the PDF for easier identification and management.

## Features

- **Text Extraction**: Extracts text from the first page of a PDF file to determine the main content of the file.
- **OCR Support**: If the extracted text is not clear or too little, OCR technology will be used to convert images to text.
- **AI Title Generation**: Automatically generates file titles based on the extracted text content using Google's Gemini API.
- **Batch Processing**: Supports traversing all PDF files in the specified directory and automatically renaming them.

## Obtain Gemini API Key

- Open [https://makersuite.google.com/](https://makersuite.google.com/)
- Log in with a Google account
- Click `Get API Key` -> `Create API key in new project` to save the key

**Notes**

- Currently, this service does not support Hong Kong IPs, [check supported regions](https://ai.google.dev/available_regions)
- Due to IP (e.g., shared IPs) or frequency, it may be judged as abuse by Google Cloud, leading to the API Key or Google Cloud account being disabled. Please use it cautiously or use a secondary account.

**Anti-Control Measures**
- 2024-04-01 Updated anti-control measures, no longer accessed through the `google-generativeai` library, trying to access by setting the address yourself (using the default address of CF Worker)

## Installation
This tool relies on several key Python libraries: `fitz` (PyMuPDF), `PIL`, `pytesseract`, and `google.generativeai`. You can install these dependencies with the following command:
```
pip install PyMuPDF Pillow pytesseract google-generativeai-sdk
```
Please note that `pytesseract` may also require you to install the Tesseract-OCR engine on your system.

## Usage

1. Clone this repository locally.
2. Ensure you have obtained the necessary API key and installed all dependencies.
3. Modify the `directory_path` and `your_api_key` variables in the script to set your PDF file directory and API key, respectively.
4. Run the script.

```
python pdf_smart_rename.py
```

## Precautions
Before using PDF-Smart-Rename to rename files, it is strongly recommended to back up all PDF files to be processed.

## Configuration
If your Tesseract-OCR is not installed in the default path, you may need to specify the path for `pytesseract` in the script:

```python
# Configure the path to Tesseract, if needed
pytesseract.pytesseract.tesseract_cmd = r'<full_path_to_your_tesseract_executable>'
```

## Contribution

Contributions and bug reports are welcome through Pull Requests or Issues.

## License

This project is licensed under the MIT License. For more information, please refer to the LICENSE file.
