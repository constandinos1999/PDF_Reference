import re

def clean_text(text: str) -> str:
    """Clean extracted text."""
    text = re.sub(r"\n\s*\d+\s", "\n", text)
    text = re.sub(r"(?<=\w)-\s(?=\w)", "", text)
    return re.sub(r"\s+", " ", text).strip()

def find_reference_section(text: str):
    """Find reference section in text."""
    match = re.search(r"(?i)(\d+\.\s*references\b.*?)(?=\n\s*\d+\.\s|\Z)", text, flags=re.DOTALL)
    return match.group(1).strip() if match else None

def parse_individual_references(section: str):
    """Extract URLs from reference section."""
    return re.findall(r"https?://[^\s]+", section)
