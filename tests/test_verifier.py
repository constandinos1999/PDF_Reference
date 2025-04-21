from pdf_python.verifier import verify_with_api 
def test_api_verification():
    # Test with a known valid reference (e.g., a DOI URL)
    reference = "https://doi.org/10.1038/s41586-020-2649-2"
    result = verify_with_api(reference)
    
    assert result["service"] in ["CrossRef", "Google Scholar"]
    assert result["status"] == "success"