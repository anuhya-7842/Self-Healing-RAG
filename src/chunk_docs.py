from pypdf import PdfReader

pdf_path = r"data/LangGraph V1 Essentials.pdf"

reader = PdfReader(pdf_path)

text = ""

for page in reader.pages:
    page_text = page.extract_text()

    if page_text:
        text += page_text + "\n"


# Split into chunks
chunk_size = 500

chunks = []

for i in range(0, len(text), chunk_size):
    chunks.append(text[i:i + chunk_size])

print("Total Chunks:", len(chunks))

print("\nFirst Chunk:\n")
print(chunks[0])