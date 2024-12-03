"""
OCR service for extracting text from PDF files and images.
Handles both direct text extraction and OCR processing.
"""

import fitz
import pytesseract
from PIL import Image
from typing import Optional

from src.config.settings import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)

class OCRService:
    """Service for handling text extraction from PDFs and images."""
    
    def __init__(self):
        """Initialize OCR service with configured settings."""
        if settings.ocr.TESSERACT_CMD:
            pytesseract.pytesseract.tesseract_cmd = settings.ocr.TESSERACT_CMD
            logger.debug(f"Tesseract path set to: {settings.ocr.TESSERACT_CMD}")

    def extract_text_from_pdf_page(self, page: fitz.Page) -> str:
        """
        Extract text from a PDF page using direct extraction.
        
        Args:
            page: A PyMuPDF page object
            
        Returns:
            str: Extracted text from the page
        """
        return page.get_text().strip()

    def extract_text_from_image(self, image: Image.Image) -> str:
        """
        Extract text from an image using OCR.
        
        Args:
            image: A PIL Image object
            
        Returns:
            str: Extracted text from the image
        """
        try:
            text = pytesseract.image_to_string(image)
            return text.strip()
        except Exception as e:
            logger.error(f"OCR processing failed: {str(e)}")
            return ""

    def extract_text_from_page(self, page: fitz.Page) -> str:
        """
        Extract text from a page, falling back to OCR if necessary.
        
        Args:
            page: A PyMuPDF page object
            
        Returns:
            str: Extracted text from the page
        """
        # Try direct text extraction first
        text = self.extract_text_from_pdf_page(page)
        
        # If text is too short, try OCR
        if len(text) < settings.ocr.MIN_TEXT_LENGTH:
            logger.info(f"Text too short ({len(text)} chars), attempting OCR")
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            text = self.extract_text_from_image(img)
            
        return text

    def extract_text_from_first_page(self, pdf_path: str) -> Optional[str]:
        """
        Extract text from the first page of a PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Optional[str]: Extracted text from the first page, or None if extraction fails
        """
        try:
            with fitz.open(pdf_path) as doc:
                if len(doc) > 0:
                    page = doc[0]  # Get the first page
                    return self.extract_text_from_page(page)
                    
            logger.warning(f"PDF file is empty: {pdf_path}")
            return None
            
        except Exception as e:
            logger.error(f"Failed to extract text from PDF: {str(e)}")
            return None

# Create a global OCR service instance
ocr_service = OCRService()