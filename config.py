import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class Config:
    # API Configuration
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    # OCR Configuration
    TESSERACT_CMD: Optional[str] = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    MIN_TEXT_LENGTH: int = 50  # Minimum characters to consider valid text
    
    # File Processing
    DEFAULT_INPUT_DIR: str = "./test_pdfs"  # Use local test_pdfs directory
    BACKUP_ENABLED: bool = True
    BACKUP_DIR: str = ".backup"
    
    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "pdf_rename.log"
    
    # Retry Configuration
    MAX_RETRIES: int = 3
    RETRY_DELAY: int = 1  # seconds
    
    # Title Generation
    TITLE_MAX_LENGTH: int = 200
    TITLE_TEMPLATE: str = "{authors}-{year}-{title}"  # Default template for research papers
    
    @classmethod
    def load(cls) -> 'Config':
        """Load configuration from environment variables or use defaults"""
        return cls(
            GEMINI_API_KEY=os.getenv("GEMINI_API_KEY", cls.GEMINI_API_KEY),
            TESSERACT_CMD=os.getenv("TESSERACT_CMD", cls.TESSERACT_CMD),
            LOG_LEVEL=os.getenv("LOG_LEVEL", cls.LOG_LEVEL),
        )

# Create a global config instance
config = Config.load()