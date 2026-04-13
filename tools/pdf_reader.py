import pdfplumber
import re
from docx import Document

def sanitize_text(text):
    """
    Cleans extracted text to improve LLM processing accuracy.
    - Removes non-ASCII characters.
    - Normalizes multiple whitespaces into a single space.
    - Removes empty lines.
    """
    # Remove non-ASCII characters
    text = text.encode("ascii", "ignore").decode()
    # Replace multiple newlines or spaces with a single newline/space
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r' +', ' ', text)
    return text.strip()

def extract_text_from_pdf(pdf_path):
    """Extract and sanitize text from a PDF file."""
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"
    return sanitize_text(text)

def extract_text_from_docx(docx_path):
    """Extract and sanitize text from a .docx file."""
    doc = Document(docx_path)
    text = ""
    for para in doc.paragraphs:
        if para.text.strip():
            text += para.text + "\n"
    return sanitize_text(text)

def extract_text_from_file(file_path):
    """Extract text from PDF or DOCX file."""
    if file_path.endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        return extract_text_from_docx(file_path)
    else:
        # Support for plain text files often found in repositories
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return sanitize_text(f.read())
        except Exception:
            raise ValueError("Unsupported file type. Use .pdf, .docx, or .txt")