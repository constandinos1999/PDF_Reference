import os
import logging
from pdfminer.high_level import extract_text
from pdfplumber import open as pdf_open
from PyPDF2 import PdfReader
from verifier import verify_with_api
from utils import clean_text, find_reference_section, parse_individual_references

logging.basicConfig(level=logging.INFO)

def extract_text_with_fallbacks(pdf_path: str) -> str:
    """Extracts text using multiple methods."""
    methods = [
        ("pdfplumber", lambda: pdfplumber_extract(pdf_path)),
        ("pdfminer", lambda: extract_text(pdf_path)),
        ("pypdf2", lambda: pypdf2_extract(pdf_path))
    ]

    for name, method in methods:
        try:
            text = method()
            if text and len(text) > 500:
                logging.info(f"Used {name} for extraction")
                return text
        except Exception as e:
            logging.warning(f"{name} extraction failed: {str(e)}")
    return ""

def pdfplumber_extract(pdf_path: str) -> str:
    try:
        with pdf_open(pdf_path) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)
    except Exception as e:
        logging.warning(f"PDFPlumber failed: {str(e)}")
        return ""

def pypdf2_extract(pdf_path: str) -> str:
    try:
        return "\n".join(page.extract_text() or "" for page in PdfReader(pdf_path).pages)
    except Exception as e:
        logging.warning(f"PyPDF2 failed: {str(e)}")
        return ""

def process_pdf(pdf_path: str):
    """Main processing function."""
    if not os.path.exists(pdf_path):
        logging.error("PDF file not found")
        return {}

    raw_text = extract_text_with_fallbacks(pdf_path)
    if not raw_text:
        logging.error("Failed to extract text from PDF")
        return {}

    cleaned_text = clean_text(raw_text)
    reference_section = find_reference_section(cleaned_text)

    if not reference_section:
        logging.warning("No reference section found")
        return {}

    references = parse_individual_references(reference_section)
    results = {ref: verify_with_api(ref) for ref in references}

    return results
