# PDF Smart Rename - Context Menu Setup

This guide explains how to add the PDF Smart Rename feature to your Windows right-click context menu.

## Prerequisites

1. Make sure Python is installed and available in your system PATH
2. Install all required dependencies by running:
   ```
   pip install -r requirements.txt
   ```
3. Configure your Gemini API key in the `.env` file (copy from `.env.example`)

## Installation

1. Edit the `add_context_menu.reg` file:
   - Right-click and select "Edit"
   - Update the path in the last line to match your actual installation path
   - The path should point to where `pdf_context_menu.py` is located
   - Make sure to use double backslashes in the path

2. Install the context menu:
   - Double-click the `add_context_menu.reg` file
   - Click "Yes" when prompted to add the information to the registry
   - Click "OK" to confirm

## Usage

1. Right-click any PDF file in Windows Explorer
2. Select "Smart Rename with AI" from the context menu
3. The file will be automatically renamed based on its content
4. A backup of the original file will be created if enabled in config

## Uninstallation

To remove the context menu entry:
1. Create a file named `remove_context_menu.reg` with the following content:
   ```
   Windows Registry Editor Version 5.00

   [-HKEY_CLASSES_ROOT\.pdf\shell\SmartRename]
   ```
2. Double-click the file and confirm the removal

## Troubleshooting

If you encounter any issues:
1. Check that all paths in the registry file are correct
2. Ensure Python and all dependencies are properly installed
3. Verify that your Gemini API key is correctly configured
4. Check the log file for detailed error messages
