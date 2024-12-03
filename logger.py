import logging
import sys
from logging.handlers import RotatingFileHandler
from typing import Optional
from config import config

class PDFRenameLogger:
    _instance: Optional['PDFRenameLogger'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PDFRenameLogger, cls).__new__(cls)
            cls._instance._initialize_logger()
        return cls._instance
    
    def _initialize_logger(self):
        """Initialize the logger with both file and console handlers"""
        self.logger = logging.getLogger('PDFRename')
        self.logger.setLevel(getattr(logging, config.LOG_LEVEL.upper()))
        
        # Clear any existing handlers
        self.logger.handlers = []
        
        # Create formatters
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_formatter = logging.Formatter(
            '%(levelname)s: %(message)s'
        )
        
        # File handler (with rotation)
        file_handler = RotatingFileHandler(
            config.LOG_FILE,
            maxBytes=1024 * 1024,  # 1MB
            backupCount=5
        )
        file_handler.setFormatter(file_formatter)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(console_formatter)
        
        # Add handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    @classmethod
    def get_logger(cls) -> logging.Logger:
        """Get the logger instance"""
        return cls().logger
    
    def __getattr__(self, name):
        """Delegate all unknown attributes to the logger instance"""
        return getattr(self.logger, name)

# Create a global logger instance
logger = PDFRenameLogger.get_logger()

# Convenience functions
def log_info(message: str):
    """Log an info message"""
    logger.info(message)

def log_error(message: str, exc_info: bool = True):
    """Log an error message with optional exception info"""
    logger.error(message, exc_info=exc_info)

def log_warning(message: str):
    """Log a warning message"""
    logger.warning(message)

def log_debug(message: str):
    """Log a debug message"""
    logger.debug(message)