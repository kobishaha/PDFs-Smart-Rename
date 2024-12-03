"""
Core file processing module that coordinates the renaming process.
Integrates OCR, title generation, and file operations.
"""

import os
import shutil
from typing import Dict, Optional
from tqdm import tqdm

from src.config.settings import settings
from src.services.ocr import ocr_service
from src.services.title_generator import title_generator
from src.utils.logger import get_logger
from src.utils.text_processor import format_text_by_style

logger = get_logger(__name__)

class FileProcessor:
    """Core processor for handling file operations and coordinating services."""

    def __init__(self):
        """Initialize the file processor."""
        self.ocr = ocr_service
        self.title_generator = title_generator

    def is_allowed_file(self, filename: str) -> bool:
        """
        Check if the file is allowed to be processed.
        
        Args:
            filename: Name of the file to check
            
        Returns:
            bool: True if file is allowed, False otherwise
        """
        if filename.startswith('.') and not settings.file.PROCESS_HIDDEN_FILES:
            return False
            
        ext = os.path.splitext(filename)[1].lower()
        return ext in settings.file.ALLOWED_FILE_TYPES

    def create_backup(self, file_path: str) -> Optional[str]:
        """
        Create a backup of the file.
        
        Args:
            file_path: Path to the file to backup
            
        Returns:
            Optional[str]: Path to the backup file if successful, None otherwise
        """
        try:
            if not settings.file.BACKUP_ENABLED:
                return None

            backup_dir = os.path.join(os.path.dirname(file_path), settings.file.BACKUP_DIR)
            os.makedirs(backup_dir, exist_ok=True)

            backup_path = os.path.join(backup_dir, os.path.basename(file_path))
            shutil.copy2(file_path, backup_path)
            logger.debug(f"Created backup at: {backup_path}")
            return backup_path

        except Exception as e:
            logger.error(f"Failed to create backup for {file_path}: {str(e)}")
            return None

    def rename_file(self, file_path: str, template_name: str = None) -> Optional[str]:
        """
        Process and rename a single file.
        
        Args:
            file_path: Path to the file to rename
            template_name: Optional template name for title generation
            
        Returns:
            Optional[str]: New file path if successful, None otherwise
        """
        try:
            logger.info(f"Processing file: {file_path}")
            
            # Create backup if enabled
            if settings.file.BACKUP_ENABLED:
                backup_path = self.create_backup(file_path)
                if backup_path:
                    logger.info(f"Backup created at: {backup_path}")
            
            # Extract text from file
            text = self.ocr.extract_text_from_first_page(file_path)
            if not text:
                logger.warning(f"No text could be extracted from {file_path}")
                return None
                
            # Generate new title
            new_title = self.title_generator.generate_title(text, template_name)
            if not new_title:
                logger.warning(f"Could not generate title for {file_path}")
                return None
                
            # Format title according to naming style
            new_title = format_text_by_style(new_title)
            
            # Add original extension
            ext = os.path.splitext(file_path)[1]
            new_title = f"{new_title}{ext}"
            new_path = os.path.join(os.path.dirname(file_path), new_title)
            
            # Rename file if new path doesn't exist
            if os.path.exists(new_path):
                logger.warning(f"File already exists: {new_path}")
                return None
                
            os.rename(file_path, new_path)
            logger.info(f"File renamed to: {new_path}")
            return new_path
            
        except Exception as e:
            logger.error(f"Error processing {file_path}: {str(e)}")
            return None

    def process_directory(self, directory_path: str, template_name: str = None) -> Dict[str, str]:
        """
        Process all allowed files in a directory.
        
        Args:
            directory_path: Path to the directory to process
            template_name: Optional template name for title generation
            
        Returns:
            Dict[str, str]: Dictionary mapping original paths to new paths
        """
        renamed_files = {}
        
        # Validate directory
        if not os.path.exists(directory_path):
            logger.error(f"Directory not found: {directory_path}")
            return renamed_files
            
        # Get list of allowed files
        all_files = [f for f in os.listdir(directory_path) if self.is_allowed_file(f)]
        
        if not all_files:
            logger.warning(f"No processable files found in {directory_path}")
            return renamed_files
            
        logger.info(f"Found {len(all_files)} files to process")
        
        # Process files with progress bar
        with tqdm(all_files, desc="Processing Files") as pbar:
            for filename in pbar:
                file_path = os.path.join(directory_path, filename)
                pbar.set_description(f"Processing {filename}")
                
                new_path = self.rename_file(file_path, template_name)
                if new_path:
                    renamed_files[file_path] = new_path
                    
        logger.info(f"Successfully renamed {len(renamed_files)} files")
        return renamed_files

# Create a global file processor instance
file_processor = FileProcessor()