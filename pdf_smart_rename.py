import os
import fitz  # PyMuPDF
import pytesseract
import requests  # Import requests
from PIL import Image

# Configure the path to Tesseract, if needed
# pytesseract.pytesseract.tesseract_cmd = r'<full_path_to_your_tesseract_executable>'


def extract_text_from_first_page(pdf_path):
    """
    Extract text from the first page of a PDF file.
    """
    with fitz.open(pdf_path) as doc:
        if len(doc) > 0:
            page = doc[0]  # Get the first page
            text = page.get_text()
            if len(text) < 50:  # Assume valid text has at least 50 characters
                # Try OCR
                pix = page.get_pixmap()  # Get a pixmap (image) from the page
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                text = pytesseract.image_to_string(img)
            return text
    return ""

def generate_title_with_gemini(pdf_text, api_key):
    """Generate a file title using the Gemini API based on PDF text content."""
    headers = {'Content-Type': 'application/json'}
    prompt = "Suggest a title for the following document content in its original language, if it's a research or science paper, just extract the relevant information and name it like: author&author-publishyear-originaltitle. show el.al for multiple authors:"
    # 将提示和PDF文本内容结合
    full_text = prompt + "\n" + pdf_text
    data = {
        "contents": [{"parts": [{"text": full_text}]}]
    }
    response = requests.post(
        f'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}', # Replace with the domain you want to proxy access
        json=data,
        headers=headers
    )
    print("Original response:", response.text)  # Debug output

    if response.status_code != 200:
        print(f"Request failed, status code: {response.status_code}")
        return ""

    try:
        response_data = response.json()
        if 'candidates' in response_data and len(response_data['candidates']) > 0:
            # Directly extract the text content from the API response
            text_content = response_data['candidates'][0]['content']['parts'][0]['text']
            # Since the response may contain the original prompt information, you may need to further process the returned text format to extract the actual title
            # Here, we simply return the entire response text, you may need to adjust according to the actual situation
            return text_content.strip()
        return ""
    except Exception as e:
        print(f"Error occurred while processing API response: {e}")
        return ""


def rename_pdf(pdf_path, api_key):
    """
    Extract PDF text, generate a title using Gemini, and rename the PDF file.
    """
    pdf_text = extract_text_from_first_page(pdf_path)
    new_title = generate_title_with_gemini(pdf_text, api_key) + ".pdf"
    new_path = os.path.join(os.path.dirname(pdf_path), new_title)
    
    if not os.path.exists(new_path):  # Ensure not to overwrite existing files
        os.rename(pdf_path, new_path)
        print(f"File has been renamed to: {new_path}")
    else:
        print("A file with the same name already exists, renaming not performed.")

def rename_pdfs_in_directory(directory_path, api_key):
    """
    Traverse all PDF files in the specified directory and attempt to rename them.
    """
    for filename in os.listdir(directory_path):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(directory_path, filename)
            print(f"Processing file: {pdf_path}")
            try:
                rename_pdf(pdf_path, api_key)
            except Exception as e:
                print(f"Error occurred while processing file {pdf_path}: {e}")

# Batch rename PDF files in the directory
# Please replace the placeholders in the following variables

directory_path = "/Users/summer/Downloads/1"  # Replace with your PDF file directory
your_api_key = "YOUR_API_KEY_HERE"  # Replace with your API key

rename_pdfs_in_directory(directory_path, your_api_key)
