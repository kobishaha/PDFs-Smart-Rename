"""
Centralized logging configuration for the application.
Provides consistent logging across all modules.
"""

import logging
import os
from typing import Optional
from logging.handlers import RotatingFileHandler

from src.config.settings import settings

# Constants for logging
MAX_LOG_SIZE = 5 * 1024 * 1024  # 5MB
BACKUP_COUNT = 3

def setup_logger(name: str, log_file: Optional[str] = None) -> logging.Logger:
    """
    Set up and configure a logger instance.
    
    Args:
        name: The name of the logger (typically __name__)
        log_file: Optional path to the log file
        
    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Skip if logger is already configured
    if logger.handlers:
        return logger
        
    # Set log level from settings
    logger.setLevel(getattr(logging, settings.logging.LEVEL.upper()))
    
    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_formatter = logging.Formatter(
        '%(levelname)s - %(message)s'
    )
    
    # Add console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # Add file handler if log file is specified
    if log_file:
        # Ensure log directory exists
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        # Create rotating file handler
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=MAX_LOG_SIZE,
            backupCount=BACKUP_COUNT
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    return logger

def get_logger(name: str) -> logging.Logger:
    """
    Get or create a logger instance.
    
    Args:
        name: The name of the logger (typically __name__)
        
    Returns:
        logging.Logger: Configured logger instance
    """
    return setup_logger(name, settings.logging.FILE)

# Create default logger
logger = get_logger(__name__)