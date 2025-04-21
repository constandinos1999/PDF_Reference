from pdf_python.extractor import PDFExtractor  # Absolute import

def test_valid_pdf_extraction():
    pdf_path = "tests/data/valid_references.pdf"
    extractor = PDFExtractor()
    text = extractor.extract_text_from_pdf(pdf_path)
    assert "References" in text  # Example assertion

def test_corrupted_pdf():
    pdf_path = "tests/data/corrupted.pdf"
    extractor = PDFExtractor()
    text = extractor.extract_text_from_pdf(pdf_path)
    
    # Check if extraction failed (either fallback message or empty)
    assert text == "No text extracted" or len(text.strip()) < 50  # Adjust 50 as needed
