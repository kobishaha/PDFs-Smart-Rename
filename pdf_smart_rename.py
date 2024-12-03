import os
import fitz  # PyMuPDF 1.23.8
import pytesseract
import requests
from PIL import Image
from typing import Optional, Dict
from tqdm import tqdm

from config import config, NamingStyle
from logger import log_info, log_error, log_debug, log_warning
from utils import retry_on_exception, sanitize_filename, create_backup, parse_title_template

class FileProcessor:
    def __init__(self):
        if config.TESSERACT_CMD:
            pytesseract.pytesseract.tesseract_cmd = config.TESSERACT_CMD
            
    @retry_on_exception(exceptions=(fitz.FileDataError, IOError))
    def extract_text_from_first_page(self, file_path: str) -> str:
        """
        Extract text from the first page of a PDF file with retry capability.
        """
        log_debug(f"Extracting text from {file_path}")
        
        with fitz.open(file_path) as doc:
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
    def generate_title_with_gemini(self, text: str, template_name: str = None) -> str:
        """
        Generate a file title using the Gemini API with retry capability.
        """
        if not config.GEMINI_API_KEY:
            raise ValueError("Gemini API key not configured")
            
        headers = {'Content-Type': 'application/json'}
        template = config.get_naming_template(template_name)
        prompt = (f"Suggest a title for the following document content in its original language using "
                 f"the template: {template}. For research papers, extract author names, year, and title. "
                 f"For multiple authors, use 'et.al' after the first author:")
                 
        data = {
            "contents": [{"parts": [{"text": f"{prompt}\n{text}"}]}]
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
                return self.format_title(title)
        except Exception as e:
            log_error(f"Error processing API response: {e}")
            raise
            
        return ""

    def format_title(self, title: str) -> str:
        """
        Format the title according to the configured naming style.
        """
        # First sanitize the filename
        title = sanitize_filename(title)
        
        # Split the title into parts
        parts = title.replace('-', ' ').replace('_', ' ').replace('.', ' ').split()
        
        # Format according to the selected style
        if config.NAMING_STYLE == NamingStyle.SNAKE_CASE:
            return '_'.join(parts).lower()
        elif config.NAMING_STYLE == NamingStyle.KEBAB_CASE:
            return '-'.join(parts).lower()
        elif config.NAMING_STYLE == NamingStyle.CAMEL_CASE:
            return parts[0].lower() + ''.join(word.capitalize() for word in parts[1:])
        elif config.NAMING_STYLE == NamingStyle.PASCAL_CASE:
            return ''.join(word.capitalize() for word in parts)
        else:  # SPACE_SEPARATED
            return ' '.join(parts)

    def is_allowed_file(self, filename: str) -> bool:
        """
        Check if the file is allowed to be processed based on configuration.
        """
        if filename.startswith('.') and not config.PROCESS_HIDDEN_FILES:
            return False
            
        ext = os.path.splitext(filename)[1].lower()
        return ext in config.ALLOWED_FILE_TYPES

    def rename_file(self, file_path: str, template_name: str = None) -> Optional[str]:
        """
        Extract file text, generate a title, and rename the file with backup support.
        """
        try:
            log_info(f"Processing file: {file_path}")
            
            # Create backup if enabled
            if config.BACKUP_ENABLED:
                backup_path = create_backup(file_path)
                log_info(f"Backup created at: {backup_path}")
            
            # Extract text and generate title
            file_text = self.extract_text_from_first_page(file_path)
            if not file_text:
                log_warning(f"No text could be extracted from {file_path}")
                return None
                
            new_title = self.generate_title_with_gemini(file_text, template_name)
            if not new_title:
                log_warning(f"Could not generate title for {file_path}")
                return None
                
            # Add original extension
            ext = os.path.splitext(file_path)[1]
            new_title = f"{new_title}{ext}"
            new_path = os.path.join(os.path.dirname(file_path), new_title)
            
            # Rename file if new path doesn't exist
            if os.path.exists(new_path):
                log_warning(f"File already exists: {new_path}")
                return None
                
            os.rename(file_path, new_path)
            log_info(f"File renamed to: {new_path}")
            return new_path
            
        except Exception as e:
            log_error(f"Error processing {file_path}: {e}")
            return None

    def rename_files_in_directory(self, directory_path: str, template_name: str = None) -> Dict[str, str]:
        """
        Traverse all allowed files in the specified directory and rename them with progress tracking.
        """
        renamed_files = {}
        all_files = [f for f in os.listdir(directory_path) if self.is_allowed_file(f)]
        
        if not all_files:
            log_warning(f"No processable files found in {directory_path}")
            return renamed_files
            
        log_info(f"Found {len(all_files)} files to process")
        
        with tqdm(all_files, desc="Processing Files") as pbar:
            for filename in pbar:
                file_path = os.path.join(directory_path, filename)
                pbar.set_description(f"Processing {filename}")
                
                new_path = self.rename_file(file_path, template_name)
                if new_path:
                    renamed_files[file_path] = new_path
                    
        log_info(f"Successfully renamed {len(renamed_files)} files")
        return renamed_files

def main():
    """Main entry point for the file renaming tool."""
    try:
        processor = FileProcessor()
        directory_path = config.DEFAULT_INPUT_DIR
        
        if not os.path.exists(directory_path):
            log_error(f"Directory not found: {directory_path}")
            return
            
        renamed_files = processor.rename_files_in_directory(directory_path)
        
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