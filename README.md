# PDFs-Smart-Rename

PDFSmartRename is a robust tool that automatically renames PDF files using OCR and AI technology. It extracts text from PDF files, generates appropriate titles using the Gemini API, and handles batch processing with advanced error handling and logging capabilities.

## Features

- **Smart Text Extraction**: 
  - Extracts text from PDF files using PyMuPDF
  - Falls back to OCR for scanned documents or images
  - Configurable minimum text length threshold

- **AI-Powered Title Generation**:
  - Uses Google's Gemini API for intelligent title generation
  - Supports research paper naming format (author-year-title)
  - Customizable title templates
  - Handles multiple languages

- **Robust Processing**:
  - Automatic retry mechanism for API and file operations
  - Comprehensive error handling and logging
  - Progress tracking for batch operations
  - File backup functionality

- **Advanced Configuration**:
  - Customizable settings via configuration file
  - Environment variable support
  - Flexible logging options
  - Backup management

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/PDFs-Smart-Rename.git
   cd PDFs-Smart-Rename
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install Tesseract OCR:
   - Windows: Download and install from [Tesseract GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
   - Linux: `sudo apt-get install tesseract-ocr`
   - macOS: `brew install tesseract`

## Configuration

1. Create a `.env` file in the project root:
   ```env
   GEMINI_API_KEY=your_api_key_here
   TESSERACT_CMD=path_to_tesseract_if_needed
   LOG_LEVEL=INFO
   ```

2. Customize settings in `config.py`:
   - API configuration
   - OCR settings
   - File processing options
   - Logging preferences
   - Retry parameters
   - Title generation templates

## Usage

### Basic Usage

1. Set your PDF directory and API key in the configuration
2. Run the script:
   ```bash
   python pdf_smart_rename.py
   ```

### Advanced Usage

1. Configure custom title templates:
   ```python
   TITLE_TEMPLATE = "{authors}-{year}-{title}"
   ```

2. Enable backup functionality:
   ```python
   BACKUP_ENABLED = True
   BACKUP_DIR = ".backup"
   ```

3. Adjust retry settings:
   ```python
   MAX_RETRIES = 3
   RETRY_DELAY = 1
   ```

## Logging

The tool provides comprehensive logging:
- Console output for operation progress
- Rotating file logs for debugging
- Configurable log levels
- Detailed error tracking

Log files are stored in `pdf_rename.log` with automatic rotation.

## Error Handling

The tool includes robust error handling:
- Automatic retries for API calls and file operations
- Exponential backoff for failed attempts
- Detailed error logging
- Safe failure modes to prevent data loss

## Backup System

Automatic backup functionality:
- Creates timestamped backups before renaming
- Configurable backup directory
- Option to enable/disable backups
- Maintains file metadata

## Notes

- Currently, this service does not support Hong Kong IPs, [check supported regions](https://ai.google.dev/available_regions)
- API usage may be subject to rate limiting
- Consider using a secondary account for high-volume processing
- Always backup important files before batch processing

## Anti-Control Measures
- 2024-04-01: Updated to use direct API access instead of the `google-generativeai` library
- Configurable proxy support for restricted regions

## Precautions
- Always backup important files before processing
- Test with a small batch of files first
- Monitor API usage to avoid rate limiting
- Verify Tesseract OCR installation

## Contributing

Contributions are welcome! Please feel free to submit pull requests or create issues for bugs and feature requests.

## License

This project is licensed under the MIT License. See the LICENSE file for details.