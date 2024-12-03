import os
import sys
import fitz
import pytesseract
import requests
from PIL import Image



def extract_text_from_first_page(pdf_path):
    with fitz.open(pdf_path) as doc:
        if len(doc) > 0:
            page = doc[0]
            text = page.get_text()
            if len(text) < 50:
                pix = page.get_pixmap()
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                text = pytesseract.image_to_string(img)
            return text.strip()
    return ""

def generate_title_with_gemini(pdf_text, api_key):
    if not api_key:
        print("Error: Gemini API key is required")
        return ""

    headers = {'Content-Type': 'application/json'}
    prompt = "Suggest a title for the following document content in its original language, if it's a research or science paper, just extract the relevant information and name it like: author&author-publishyear-originaltitle. show el.al for multiple authors:"
    data = {"contents": [{"parts": [{"text": f"{prompt}\n{pdf_text}"}]}]}
    
    try:
        response = requests.post(
            f'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}',
            json=data,
            headers=headers
        )
        if response.status_code != 200:
            print(f"Request failed, status code: {response.status_code}")
            return ""
        response_data = response.json()
        if 'candidates' in response_data and response_data['candidates']:
            return response_data['candidates'][0]['content']['parts'][0]['text'].strip()
    except Exception as e:
        print(f"Error occurred while processing API response: {e}")
    return ""

def rename_pdf(pdf_path, api_key):
    if not os.path.exists(pdf_path):
        print(f"Error: File not found: {pdf_path}")
        return False
    
    print(f"Processing file: {pdf_path}")
    pdf_text = extract_text_from_first_page(pdf_path)
    if not pdf_text:
        print("Error: Could not extract text from PDF")
        return False
    
    print("Extracted text length:", len(pdf_text))
    print("First 200 characters:", pdf_text[:200])
    
    new_title = generate_title_with_gemini(pdf_text, api_key)
    if not new_title:
        print("Error: Could not generate title")
        return False
    
    print("Generated title:", new_title)
    new_title = new_title.strip() + ".pdf"
    new_path = os.path.join(os.path.dirname(pdf_path), new_title)
    
    if os.path.exists(new_path):
        print(f"Error: File already exists: {new_path}")
        return False
    
    os.rename(pdf_path, new_path)
    print(f"Success: File renamed to: {new_path}")
    return True

# Command line usage
if len(sys.argv) != 3:
    print("Usage: python pdf_smart_rename_singlefile.py <pdf_path> <api_key>")
    sys.exit(1)

pdf_path = sys.argv[1]
api_key = sys.argv[2]
rename_pdf(pdf_
        return False
        
    os.rename(pdf_path, new_path)
    print(f"Success: File renamed to: {new_path}")
    return True

# Simple command-line execution
if len(sys.argv) < 3:
    print("Usage: python pdf_smart_rename_singlefile.py <pdf_path> <api_key>")
    sys.exit(1)

pdf_path = sys.argv[1]
api_key = sys.argv[2]
rename_pdf(pdf_path, api_key)
    
    success = rename_pdf(pdf_file_path,