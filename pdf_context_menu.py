
import os
import sys
from pdf_smart_rename import PDFProcessor
from config import config
from logger import log_info, log_error

def main():
    """Entry point for the context menu PDF renaming tool."""
    try:
        # Check if a file path was provided as argument
        if len(sys.argv) != 2:
            log_error("Please provide a PDF file path as argument")
            return

        pdf_path = sys.argv[1]
        
        # Check if the file exists and is a PDF
        if not os.path.exists(pdf_path):
            log_error(f"File not found: {pdf_path}")
            return
            
        if not pdf_path.lower().endswith('.pdf'):
            log_error(f"File is not a PDF: {pdf_path}")
            return

        # Initialize the PDF processor and rename the file
        processor = PDFProcessor()
        new_path = processor.rename_pdf(pdf_path)
        
        if new_path:
            log_info(f"Successfully renamed:\n{pdf_path} ->\n{new_path}")
        else:
            log_error("Failed to rename the file")

    except Exception as e:
        log_error(f"An error occurred: {e}")
        
    # Keep the window open for a few seconds so user can see the result
    input("\nPress Enter to close...")

if __name__ == "__main__":
    main()
