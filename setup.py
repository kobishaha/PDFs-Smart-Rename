"""
Setup configuration for the PDF Smart Rename package.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pdf-smart-rename",
    version="1.0.0",
    author="Kodu AI",
    author_email="info@kodu.ai",
    description="Smart PDF renaming tool using OCR and AI title generation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kodu-ai/PDFs-Smart-Rename",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business",
        "Topic :: Text Processing :: General",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "PyMuPDF>=1.23.8",
        "pytesseract>=0.3.10",
        "Pillow>=10.0.0",
        "requests>=2.31.0",
        "tqdm>=4.66.0",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "pdf-smart-rename=src.__main__:main",
        ],
    },
    package_data={
        "pdf_smart_rename": [
            "examples/test_pdfs/*",
            "scripts/*",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)