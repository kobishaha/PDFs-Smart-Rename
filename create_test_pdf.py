import fitz

# Create a new PDF document
doc = fitz.open()
page = doc.new_page()

# Add test text
text = '''Test Research Paper
Authors: John Smith & Jane Doe
Year: 2024

Abstract:
This is a test document to evaluate the PDF smart rename functionality.
The system should extract this text and generate an appropriate filename
based on the content, authors, and year information provided.'''

# Insert text and save
page.insert_text((50, 50), text, fontsize=12)
doc.save('test_pdfs/test-paper-2024.pdf')
doc.close()

print('Test PDF created in test_pdfs/test-paper-2024.pdf')

print(f"Test P
    print(f"Test PDF created successfully in {output_path}")

if __na
