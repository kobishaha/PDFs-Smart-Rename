"""
Main entry point for the PDF Smart Rename tool.
Provides command-line interface and handles program execution.
"""

import sys
import argparse
import os
from typing import List, Optional

from src.config.settings import settings
from src.core.processor import file_processor
from src.utils.logger import get_logger

logger = get_logger(__name__)

def parse_arguments() -> argparse.Namespace:
    """
    Parse command line arguments.
    
    Returns:
        argparse.Namespace: Parsed command line arguments
    """
    parser = argparse.ArgumentParser(
        description="Smart PDF renaming tool using OCR and AI title generation"
    )
    
    parser.add_argument(
        "-d", "--directory",
        help="Directory containing files to process (default: ./examples/test_pdfs)",
        default=settings.file.DEFAULT_INPUT_DIR
    )
    
    parser.add_argument(
        "-t", "--template",
        help="Naming template to use (default: research)",
        choices=list(settings.naming.TEMPLATES.keys()),
        default=settings.naming.DEFAULT_TEMPLATE
    )
    
    parser.add_argument(
        "-s", "--style",
        help="Naming style to use (default: kebab-case)",
        choices=[style.value for style in settings.NamingStyle],
        default=settings.naming.STYLE.value
    )
    
    parser.add_argument(
        "-f", "--file-types",
        help="Comma-separated list of file extensions to process (default: .pdf)",
        default=",".join(settings.file.ALLOWED_FILE_TYPES)
    )
    
    parser.add_argument(
        "--no-backup",
        help="Disable file backup before renaming",
        action="store_true"
    )
    
    parser.add_argument(
        "--hidden",
        help="Process hidden files",
        action="store_true"
    )
    
    return parser.parse_args()

def update_settings(args: argparse.Namespace) -> None:
    """
    Update settings based on command line arguments.
    
    Args:
        args: Parsed command line arguments
    """
    # Update file types
    settings.file.ALLOWED_FILE_TYPES = [
        ext.strip() for ext in args.file_types.split(",")
    ]
    
    # Update backup setting
    settings.file.BACKUP_ENABLED = not args.no_backup
    
    # Update hidden files setting
    settings.file.PROCESS_HIDDEN_FILES = args.hidden
    
    # Update naming style
    for style in settings.NamingStyle:
        if style.value == args.style:
            settings.naming.STYLE = style
            break

def process_files(directory: str, template: str) -> bool:
    """
    Process files in the specified directory.
    
    Args:
        directory: Directory containing files to process
        template: Naming template to use
        
    Returns:
        bool: True if processing was successful, False otherwise
    """
    try:
        # Validate directory
        if not os.path.exists(directory):
            logger.error(f"Directory not found: {directory}")
            return False
            
        # Process files
        renamed_files = file_processor.process_directory(directory, template)
        
        # Report results
        if renamed_files:
            logger.info("\nSuccessfully renamed files:")
            for old_path, new_path in renamed_files.items():
                logger.info(f"{old_path} -> {new_path}")
            return True
        else:
            logger.warning("No files were renamed")
            return False
            
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return False

def main() -> int:
    """
    Main program entry point.
    
    Returns:
        int: Exit code (0 for success, 1 for failure)
    """
    try:
        # Parse arguments and update settings
        args = parse_arguments()
        update_settings(args)
        
        # Process files
        success = process_files(args.directory, args.template)
        return 0 if success else 1
        
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())