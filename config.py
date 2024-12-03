import os
from dataclasses import dataclass
from typing import Optional, List
from enum import Enum

class NamingStyle(Enum):
    SNAKE_CASE = "snake_case"  # example_file_name
    KEBAB_CASE = "kebab-case"  # example-file-name
    CAMEL_CASE = "camelCase"   # exampleFileName
    PASCAL_CASE = "PascalCase" # ExampleFileName
    SPACE_SEPARATED = "space"  # example file name

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
    
    # File Type Configuration
    ALLOWED_FILE_TYPES: List[str] = [".pdf"]  # List of allowed file extensions
    PROCESS_HIDDEN_FILES: bool = False  # Whether to process hidden files
    
    # Naming Configuration
    NAMING_STYLE: NamingStyle = NamingStyle.KEBAB_CASE
    NAMING_TEMPLATES: dict = {
        "research": "{authors}-{year}-{title}",  # Default for research papers
        "document": "{date}-{title}",            # For general documents
        "report": "{category}-{date}-{title}",   # For reports
        "custom": "{title}"                      # Simple title only
    }
    DEFAULT_TEMPLATE: str = "research"
    
    # Title Processing
    TITLE_MAX_LENGTH: int = 200
    TITLE_MIN_LENGTH: int = 10
    REMOVE_SPECIAL_CHARS: bool = True
    PRESERVE_CHARS: str = "-_."  # Special characters to preserve
    
    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "pdf_rename.log"
    
    # Retry Configuration
    MAX_RETRIES: int = 3
    RETRY_DELAY: int = 1  # seconds
    
    @classmethod
    def load(cls) -> 'Config':
        """Load configuration from environment variables or use defaults"""
        naming_style = os.getenv("NAMING_STYLE", cls.NAMING_STYLE.value)
        try:
            naming_style = NamingStyle(naming_style)
        except ValueError:
            naming_style = cls.NAMING_STYLE

        allowed_types = os.getenv("ALLOWED_FILE_TYPES")
        if allowed_types:
            allowed_types = allowed_types.split(",")
        else:
            allowed_types = cls.ALLOWED_FILE_TYPES

        return cls(
            GEMINI_API_KEY=os.getenv("GEMINI_API_KEY", cls.GEMINI_API_KEY),
            TESSERACT_CMD=os.getenv("TESSERACT_CMD", cls.TESSERACT_CMD),
            LOG_LEVEL=os.getenv("LOG_LEVEL", cls.LOG_LEVEL),
            ALLOWED_FILE_TYPES=allowed_types,
            NAMING_STYLE=naming_style,
        )

    def get_naming_template(self, template_name: str = None) -> str:
        """Get the naming template based on the template name"""
        template_name = template_name or self.DEFAULT_TEMPLATE
        return self.NAMING_TEMPLATES.get(template_name, self.NAMING_TEMPLATES["custom"])

# Create a global config instance
config = Config.load()