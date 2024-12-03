import os
import fitz  # PyMuPDF 1.23.8
import pytesseract
import requests
from PIL import Image
from typing import Optional, Dict
from tqdm import tqdm

from config import config
from logger import log_info, log_error, log_debug, log_warning
from utils import retry_on_exception, sanitize_filename, create_backup, parse_title_template

class PDFProcessor:
    def __init__(self):
        if config.TESSERACT_CMD:
            pytesseract.pytesseract.tesseract_cmd = config.TESSERACT_CMD
            
    @retry_on_exception(exceptions=(fitz.FileDataError, IOError))
    def extract_text_from_first_page(self, pdf_path: str) -> str:
        """
        Extract text from the first page of a PDF file with retry capability.
        """
        log_debug(f"Extracting text from {pdf_path}")
        
        with fitz.open(pdf_path) as doc:
            if len(doc) > 0:
                page = doc[0]  # Get the first page
                text = page.get_text()
                
                if len(text) < config.MIN_TEXT_LENGTH:
                    log_info(f"Text too short ({len(text)} chars), attempting OCR")
                    pix = page.get_pixmap()
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    text = pytesseract.image_to_string(img)
                    
                return text.strip()
                
        return ""

    @retry_on_exception(exceptions=(requests.RequestException,))
    def generate_title_with_gemini(self, pdf_text: str) -> str:
        """
        Generate a file title using the Gemini API with retry capability.
        """
        if not config.GEMINI_API_KEY:
            raise ValueError("Gemini API key not configured")
            
        headers = {'Content-Type': 'application/json'}
        prompt = ("Suggest a title for the following document content in its original language, "
                 "if it's a research or science paper, just extract the relevant information and "
                 "name it like: author&author-publishyear-originaltitle. show el.al for multiple authors:")
                 
        data = {
            "contents": [{"parts": [{"text": f"{prompt}\n{pdf_text}"}]}]
        }
        
        response = requests.post(
            f'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={config.GEMINI_API_KEY}',
            json=data,
            headers=headers
        )
        
        if response.status_code != 200:
            raise requests.RequestException(f"API request failed with status {response.status_code}")
            
        try:
            response_data = response.json()
            if 'candidates' in response_data and response_data['candidates']:
                title = response_data['candidates'][0]['content']['parts'][0]['text'].strip()
                return sanitize_filename(title)
        except Exception as e:
            log_error(f"Error processing API response: {e}")
            raise
            
        return ""

    def rename_pdf(self, pdf_path: str) -> Optional[str]:
        """
        Extract PDF text, generate a title, and rename the PDF file with backup support.
        """
        try:
            log_info(f"Processing file: {pdf_path}")
            
            # Create backup if enabled
            if config.BACKUP_ENABLED:
                backup_path = create_backup(pdf_path)
                log_info(f"Backup created at: {backup_path}")
            
            # Extract text and generate title
            pdf_text = self.extract_text_from_first_page(pdf_path)
            if not pdf_text:
                log_warning(f"No text could be extracted from {pdf_path}")
                return None
                
            new_title = self.generate_title_with_gemini(pdf_text)
            if not new_title:
                log_warning(f"Could not generate title for {pdf_path}")
                return None
                
            new_title = f"{new_title}.pdf"
            new_path = os.path.join(os.path.dirname(pdf_path), new_title)
            
            # Rename file if new path doesn't exist
            if os.path.exists(new_path):
                log_warning(f"File already exists: {new_path}")
                return None
                
            os.rename(pdf_path, new_path)
            log_info(f"File renamed to: {new_path}")
            return new_path
            
        except Exception as e:
            log_error(f"Error processing {pdf_path}: {e}")
            return None

    def rename_pdfs_in_directory(self, directory_path: str) -> Dict[str, str]:
        """
        Traverse all PDF files in the specified directory and rename them with progress tracking.
        """
        renamed_files = {}
        pdf_files = [f for f in os.listdir(directory_path) if f.lower().endswith('.pdf')]
        
        if not pdf_files:
            log_warning(f"No PDF files found in {directory_path}")
            return renamed_files
            
        log_info(f"Found {len(pdf_files)} PDF files to process")
        
        with tqdm(pdf_files, desc="Processing PDFs") as pbar:
            for filename in pbar:
                pdf_path = os.path.join(directory_path, filename)
                pbar.set_description(f"Processing {filename}")
                
                new_path = self.rename_pdf(pdf_path)
                if new_path:
                    renamed_files[pdf_path] = new_path
                    
        log_info(f"Successfully renamed {len(renamed_files)} files")
        return renamed_files

def main():
    """Main entry point for the PDF renaming tool."""
    try:
        processor = PDFProcessor()
        directory_path = config.DEFAULT_INPUT_DIR
        
        if not os.path.exists(directory_path):
            log_error(f"Directory not found: {directory_path}")
            return
            
        renamed_files = processor.rename_pdfs_in_directory(directory_path)
        
        if renamed_files:
            log_info("\nSuccessfully renamed files:")
            for old_path, new_path in renamed_files.items():
                log_info(f"{old_path} -> {new_path}")
        else:
            log_warning("No files were renamed")
            
    except Exception as e:
        log_error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()