"""
Configuration settings for the PDF Smart Rename tool.
Handles all configuration parameters and environment variables.
"""

import os
from dataclasses import dataclass
from typing import Optional, List
from enum import Enum

class NamingStyle(Enum):
    """Available naming styles for file renaming."""
    SNAKE_CASE = "snake_case"  # example_file_name
    KEBAB_CASE = "kebab-case"  # example-file-name
    CAMEL_CASE = "camelCase"   # exampleFileName
    PASCAL_CASE = "PascalCase" # ExampleFileName
    SPACE_SEPARATED = "space"  # example file name

@dataclass
class FileConfig:
    """File processing configuration."""
    ALLOWED_FILE_TYPES: List[str] = None
    PROCESS_HIDDEN_FILES: bool = False
    DEFAULT_INPUT_DIR: str = "./examples/test_pdfs"
    BACKUP_ENABLED: bool = True
    BACKUP_DIR: str = ".backup"

    def __post_init__(self):
        if self.ALLOWED_FILE_TYPES is None:
            self.ALLOWED_FILE_TYPES = [".pdf"]

@dataclass
class OCRConfig:
    """OCR processing configuration."""
    TESSERACT_CMD: Optional[str] = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    MIN_TEXT_LENGTH: int = 50

@dataclass
class APIConfig:
    """API configuration for title generation."""
    GEMINI_API_KEY: str = ""
    MAX_RETRIES: int = 3
    RETRY_DELAY: int = 1

@dataclass
class NamingConfig:
    """File naming configuration."""
    STYLE: NamingStyle = NamingStyle.KEBAB_CASE
    TEMPLATES: dict = None
    DEFAULT_TEMPLATE: str = "research"
    TITLE_MAX_LENGTH: int = 200
    TITLE_MIN_LENGTH: int = 10
    REMOVE_SPECIAL_CHARS: bool = True
    PRESERVE_CHARS: str = "-_."

    def __post_init__(self):
        if self.TEMPLATES is None:
            self.TEMPLATES = {
                "research": "{authors}-{year}-{title}",
                "document": "{date}-{title}",
                "report": "{category}-{date}-{title}",
                "custom": "{title}"
            }

@dataclass
class LoggingConfig:
    """Logging configuration."""
    LEVEL: str = "INFO"
    FILE: str = "pdf_rename.log"

class Settings:
    """Global settings container."""
    def __init__(self):
        self.file = FileConfig(
            ALLOWED_FILE_TYPES=self._parse_list_env("ALLOWED_FILE_TYPES", [".pdf"]),
            PROCESS_HIDDEN_FILES=self._parse_bool_env("PROCESS_HIDDEN_FILES", False),
            DEFAULT_INPUT_DIR=os.getenv("DEFAULT_INPUT_DIR", "./examples/test_pdfs"),
            BACKUP_ENABLED=self._parse_bool_env("BACKUP_ENABLED", True),
            BACKUP_DIR=os.getenv("BACKUP_DIR", ".backup")
        )

        self.ocr = OCRConfig(
            TESSERACT_CMD=os.getenv("TESSERACT_CMD", r"C:\Program Files\Tesseract-OCR\tesseract.exe"),
            MIN_TEXT_LENGTH=int(os.getenv("MIN_TEXT_LENGTH", "50"))
        )

        self.api = APIConfig(
            GEMINI_API_KEY=os.getenv("GEMINI_API_KEY", ""),
            MAX_RETRIES=int(os.getenv("MAX_RETRIES", "3")),
            RETRY_DELAY=int(os.getenv("RETRY_DELAY", "1"))
        )

        self.naming = NamingConfig(
            STYLE=self._parse_naming_style(os.getenv("NAMING_STYLE", "kebab-case")),
            DEFAULT_TEMPLATE=os.getenv("DEFAULT_TEMPLATE", "research"),
            TITLE_MAX_LENGTH=int(os.getenv("TITLE_MAX_LENGTH", "200")),
            TITLE_MIN_LENGTH=int(os.getenv("TITLE_MIN_LENGTH", "10")),
            REMOVE_SPECIAL_CHARS=self._parse_bool_env("REMOVE_SPECIAL_CHARS", True),
            PRESERVE_CHARS=os.getenv("PRESERVE_CHARS", "-_.")
        )

        self.logging = LoggingConfig(
            LEVEL=os.getenv("LOG_LEVEL", "INFO"),
            FILE=os.getenv("LOG_FILE", "pdf_rename.log")
        )

    @staticmethod
    def _parse_bool_env(key: str, default: bool) -> bool:
        """Parse boolean environment variables."""
        value = os.getenv(key, str(default)).lower()
        return value in ("true", "1", "yes", "y", "t")

    @staticmethod
    def _parse_list_env(key: str, default: List[str]) -> List[str]:
        """Parse list environment variables."""
        value = os.getenv(key)
        if value:
            return [item.strip() for item in value.split(",")]
        return default

    @staticmethod
    def _parse_naming_style(value: str) -> NamingStyle:
        """Parse naming style from environment variable."""
        try:
            return NamingStyle(value)
        except ValueError:
            return NamingStyle.KEBAB_CASE

    def get_naming_template(self, template_name: str = None) -> str:
        """Get the naming template based on the template name."""
        template_name = template_name or self.naming.DEFAULT_TEMPLATE
        return self.naming.TEMPLATES.get(template_name, self.naming.TEMPLATES["custom"])

# Create a global settings instance
settings = Settings()