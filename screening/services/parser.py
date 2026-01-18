import re
import PyPDF2
from docx import Document


def extract_text_from_pdf(file_path):
    """
    Extract text from PDF file using PyPDF2.
    Returns raw text string.
    """
    text = ""
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
    except Exception as e:
        raise ValueError(f"PDF parsing failed: {str(e)}")
    
    return text


def extract_text_from_docx(file_path):
    """
    Extract text from DOCX file using python-docx.
    Returns raw text string.
    """
    text = ""
    try:
        doc = Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        raise ValueError(f"DOCX parsing failed: {str(e)}")
    
    return text


def normalize_text(text):
    """
    Clean and normalize extracted text:
    - Convert to lowercase
    - Remove extra whitespace
    - Remove multiple newlines
    """
    if not text:
        return ""
    
    # Lowercase
    text = text.lower()
    
    # Replace multiple spaces with single space
    text = re.sub(r'\s+', ' ', text)
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    return text


def parse_resume(file_path, file_extension):
    """
    Main parsing function.
    Accepts file path and extension.
    Returns normalized text.
    """
    if file_extension == '.pdf':
        raw_text = extract_text_from_pdf(file_path)
    elif file_extension in ['.docx', '.doc']:
        raw_text = extract_text_from_docx(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_extension}")
    
    normalized_text = normalize_text(raw_text)
    
    if not normalized_text:
        raise ValueError("No text extracted from resume")
    
    return normalized_text