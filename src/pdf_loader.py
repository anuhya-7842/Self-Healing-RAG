from pypdf import PdfReader

pdf_path = r"data/LangGraph V1 Essentials.pdf"

reader = PdfReader(pdf_path)

print("Number of pages:", len(reader.pages))

text = ""

for page in reader.pages:
    page_text = page.extract_text()
    if page_text:
        text += page_text + "\n"

print("\nFirst 2000 Characters:\n")
print(text[:2000])