import os
from docx import Document
from PyPDF2 import PdfReader


def process_document(file_path: str) -> dict:
    if not os.path.exists(file_path):
        raise FileNotFoundError("File not found")

    # Read file header to detect actual content type
    with open(file_path, "rb") as file:
        header = file.read(4)

    
    # Extract text
   
    if header.startswith(b"PK"):
        detected_type = "docx"
        doc = Document(file_path)
        text = "\n".join(p.text for p in doc.paragraphs)

    elif header.startswith(b"%PDF"):
        detected_type = "pdf"
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""

    else:
        detected_type = "txt"
        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
            text = file.read()

    text_lower = text.lower()

    
    # Categorization
    
    categories = {
        "Resume": ["experience", "education", "skills", "projects"],
        "Invoice": ["invoice", "total", "amount", "gst", "bill"],
        "Offer Letter": ["offer", "joining", "salary", "designation"],
        "Legal Document": ["agreement", "clause", "party", "terms"],
        "Technical Document": ["api", "architecture", "system", "database"]
    }

    scores = {}
    for category, keywords in categories.items():
        scores[category] = sum(text_lower.count(k) for k in keywords)

    best_category = max(scores, key=scores.get)
    category = best_category if scores[best_category] > 0 else "Unknown"

    
    # Final JSON output

    return {
        "file_path": file_path,
        "detected_type": detected_type,
        "category": category,
        "content": text.strip()
    }

a=process_document("resume.txt")
print(a)