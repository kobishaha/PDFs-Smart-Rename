"""
Title generation service using the Gemini API.
Handles the generation of file titles based on document content.
"""

import requests
from typing import Optional, Dict, Any
from functools import wraps
import time

from src.config.settings import settings
from src.utils.logger import get_logger
from src.utils.text_processor import sanitize_filename

logger = get_logger(__name__)

def retry_on_api_error(func):
    """Decorator to retry API calls on failure."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        retries = 0
        while retries < settings.api.MAX_RETRIES:
            try:
                return func(*args, **kwargs)
            except requests.RequestException as e:
                retries += 1
                if retries == settings.api.MAX_RETRIES:
                    logger.error(f"API call failed after {retries} retries: {str(e)}")
                    raise
                logger.warning(f"API call failed, retrying ({retries}/{settings.api.MAX_RETRIES})")
                time.sleep(settings.api.RETRY_DELAY)
    return wrapper

class TitleGenerator:
    """Service for generating titles using the Gemini API."""

    def __init__(self):
        """Initialize the title generator service."""
        self.api_key = settings.api.GEMINI_API_KEY
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
        self.headers = {'Content-Type': 'application/json'}

    def _create_prompt(self, text: str, template_name: str = None) -> str:
        """
        Create a prompt for the Gemini API based on the template.
        
        Args:
            text: The document text to generate a title for
            template_name: Optional template name to use
            
        Returns:
            str: The formatted prompt
        """
        template = settings.get_naming_template(template_name)
        return (
            f"Suggest a title for the following document content in its original language using "
            f"the template: {template}. For research papers, extract author names, year, and title. "
            f"For multiple authors, use 'et.al' after the first author:\n\n{text}"
        )

    def _parse_response(self, response_data: Dict[str, Any]) -> Optional[str]:
        """
        Parse the API response to extract the generated title.
        
        Args:
            response_data: The API response data
            
        Returns:
            Optional[str]: The generated title, or None if parsing fails
        """
        try:
            if 'candidates' in response_data and response_data['candidates']:
                title = response_data['candidates'][0]['content']['parts'][0]['text'].strip()
                return sanitize_filename(title)
        except Exception as e:
            logger.error(f"Error parsing API response: {str(e)}")
        return None

    @retry_on_api_error
    def generate_title(self, text: str, template_name: str = None) -> Optional[str]:
        """
        Generate a title for the given text using the Gemini API.
        
        Args:
            text: The document text to generate a title for
            template_name: Optional template name to use
            
        Returns:
            Optional[str]: The generated title, or None if generation fails
            
        Raises:
            ValueError: If the API key is not configured
            requests.RequestException: If the API request fails
        """
        if not self.api_key:
            raise ValueError("Gemini API key not configured")

        prompt = self._create_prompt(text, template_name)
        data = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }]
        }

        response = requests.post(
            f"{self.base_url}?key={self.api_key}",
            json=data,
            headers=self.headers
        )

        if response.status_code != 200:
            raise requests.RequestException(
                f"API request failed with status {response.status_code}"
            )

        title = self._parse_response(response.json())
        if title:
            logger.debug(f"Generated title: {title}")
            return title

        logger.warning("Failed to generate title from API response")
        return None

# Create a global title generator instance
title_generator = TitleGenerator()