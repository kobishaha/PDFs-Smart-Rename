import fitz

# Read the text file
with open("test_pdfs/test-paper.txt", "r") as f:
    text = f.read()

# Create PDF
doc = fitz.open()
page = doc.new_page()
page.insert_text((50, 50), text, fontsize=12)
doc.save("test_pdfs/test-paper-2024.pdf")
doc.close()

print("PDF file created successfully")