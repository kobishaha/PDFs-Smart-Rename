"""
Text processing utilities for handling file names and content.
Provides functions for text sanitization and formatting.
"""

import re
import unicodedata
from typing import Dict

from src.config.settings import settings

def sanitize_filename(text: str) -> str:
    """
    Sanitize text for use as a filename.
    
    Args:
        text: The text to sanitize
        
    Returns:
        str: Sanitized text safe for use as a filename
    """
    # Normalize unicode characters
    text = unicodedata.normalize('NFKD', text)
    
    # Remove or replace special characters based on settings
    if settings.naming.REMOVE_SPECIAL_CHARS:
        # Keep specified special characters
        pattern = f"[^a-zA-Z0-9{re.escape(settings.naming.PRESERVE_CHARS)}]+"
        text = re.sub(pattern, ' ', text)
    
    # Remove multiple spaces and trim
    text = ' '.join(text.split())
    
    # Truncate to maximum length while preserving words
    if len(text) > settings.naming.TITLE_MAX_LENGTH:
        words = text[:settings.naming.TITLE_MAX_LENGTH].rsplit(' ', 1)[0]
        text = words.strip()
    
    # Ensure minimum length
    if len(text) < settings.naming.TITLE_MIN_LENGTH:
        text = text.ljust(settings.naming.TITLE_MIN_LENGTH, '_')
    
    return text

def parse_title_template(template: str, data: Dict[str, str]) -> str:
    """
    Parse a title template with provided data.
    
    Args:
        template: The template string with placeholders
        data: Dictionary of values to fill the template
        
    Returns:
        str: The parsed template with placeholders replaced
    """
    try:
        return template.format(**data)
    except KeyError as e:
        # If a placeholder is missing, return a simplified version
        return data.get('title', 'untitled')

def extract_metadata(text: str) -> Dict[str, str]:
    """
    Extract metadata from text for use in title templates.
    
    Args:
        text: The text to extract metadata from
        
    Returns:
        Dict[str, str]: Dictionary containing extracted metadata
    """
    metadata = {
        'title': text.split('\n')[0][:100],  # Use first line as default title
        'date': '',
        'category': '',
        'authors': '',
        'year': ''
    }
    
    # Extract year (YYYY format)
    year_match = re.search(r'\b(19|20)\d{2}\b', text)
    if year_match:
        metadata['year'] = year_match.group(0)
    
    # Extract potential author names (simplified)
    author_pattern = r'(?:Author|By|Written by)[s]?[:]\s*([A-Za-z\s,\.]+)'
    author_match = re.search(author_pattern, text, re.IGNORECASE)
    if author_match:
        metadata['authors'] = author_match.group(1).strip()
    
    return metadata

def format_text_by_style(text: str) -> str:
    """
    Format text according to the configured naming style.
    
    Args:
        text: The text to format
        
    Returns:
        str: Formatted text according to the naming style
    """
    # Split the text into parts
    parts = text.replace('-', ' ').replace('_', ' ').replace('.', ' ').split()
    
    # Format according to the selected style
    style = settings.naming.STYLE
    style_name = style.value if hasattr(style, 'value') else str(style)
    
    if style_name == "snake_case":
        return '_'.join(parts).lower()
    elif style_name == "kebab-case":
        return '-'.join(parts).lower()
    elif style_name == "camelCase":
        return parts[0].lower() + ''.join(word.capitalize() for word in parts[1:])
    elif style_name == "PascalCase":
        return ''.join(word.capitalize() for word in parts)
    else:  # space separated
        return ' '.join(parts)

def clean_text(text: str) -> str:
    """
    Clean and normalize text content.
    
    Args:
        text: The text to clean
        
    Returns:
        str: Cleaned and normalized text
    """
    # Normalize unicode characters
    text = unicodedata.normalize('NFKD', text)
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Remove control characters
    text = ''.join(char for char in text if unicodedata.category(char)[0] != 'C')
    
    return text.strip()