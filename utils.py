import time
from functools import wraps
from typing import TypeVar, Callable, Any
from config import config
from logger import log_warning, log_error, log_debug

T = TypeVar('T')

def retry_on_exception(
    exceptions: tuple = (Exception,),
    max_retries: int = None,
    delay: int = None,
    backoff: int = 2,
    logger: Callable[[str], None] = log_warning
) -> Callable:
    """
    Retry decorator with exponential backoff
    
    Args:
        exceptions: Tuple of exceptions to catch
        max_retries: Maximum number of retries (defaults to config.MAX_RETRIES)
        delay: Initial delay between retries in seconds (defaults to config.RETRY_DELAY)
        backoff: Multiplier for delay after each retry
        logger: Logging function to use
    """
    max_retries = max_retries if max_retries is not None else config.MAX_RETRIES
    delay = delay if delay is not None else config.RETRY_DELAY

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            retries = 0
            current_delay = delay

            while True:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    retries += 1
                    if retries > max_retries:
                        log_error(f"Max retries ({max_retries}) exceeded for {func.__name__}")
                        raise e

                    logger(
                        f"Attempt {retries}/{max_retries} failed for {func.__name__}. "
                        f"Retrying in {current_delay} seconds... Error: {str(e)}"
                    )
                    time.sleep(current_delay)
                    current_delay *= backoff
                    log_debug(f"Retrying {func.__name__} with args: {args}, kwargs: {kwargs}")

        return wrapper
    return decorator

def sanitize_filename(filename: str, max_length: int = None) -> str:
    """
    Sanitize filename by removing invalid characters and truncating if necessary
    
    Args:
        filename: Original filename
        max_length: Maximum length for filename (defaults to config.TITLE_MAX_LENGTH)
    
    Returns:
        Sanitized filename
    """
    max_length = max_length if max_length is not None else config.TITLE_MAX_LENGTH
    
    # Replace invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Replace multiple spaces/underscores with single underscore
    filename = '_'.join(filter(None, filename.split()))
    
    # Handle Hebrew text direction
    # Split into words and reverse only if the text contains Hebrew
    if any('\u0590' <= c <= '\u05FF' for c in filename):
        words = filename.split('_')
        words.reverse()
        filename = '_'.join(words)
    
    # Truncate if necessary, ensuring we don't cut in the middle of a word
    if len(filename) > max_length:
        words = filename[:max_length].split('_')
        filename = '_'.join(words[:-1])
    
    return filename.strip('_')

def create_backup(file_path: str) -> str:
    """
    Create a backup of the file before renaming
    
    Args:
        file_path: Path to the file to backup
    
    Returns:
        Path to the backup file
    """
    import os
    import shutil
    from datetime import datetime
    
    if not config.BACKUP_ENABLED:
        return None
        
    # Create backup directory if it doesn't exist
    backup_dir = os.path.join(os.path.dirname(file_path), config.BACKUP_DIR)
    os.makedirs(backup_dir, exist_ok=True)
    
    # Generate backup filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_filename = f"{os.path.basename(file_path)}.{timestamp}.bak"
    backup_path = os.path.join(backup_dir, backup_filename)
    
    # Create backup
    shutil.copy2(file_path, backup_path)
    log_debug(f"Created backup at {backup_path}")
    
    return backup_path

def parse_title_template(template_str: str, **kwargs) -> str:
    """
    Parse title template string with provided values
    
    Args:
        template_str: Template string (e.g., "{authors}-{year}-{title}")
        **kwargs: Values to fill the template
    
    Returns:
        Formatted string
    """
    try:
        return template_str.format(**kwargs)
    except KeyError as e:
        log_warning(f"Missing template value: {e}")
        # Fall back to a simple concatenation of available values
        return '-'.join(str(v) for v in kwargs.valu