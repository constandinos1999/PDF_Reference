import hashlib
import requests
import time
import logging
from config import CONFIG

cache = {}

def verify_with_api(reference: str):
    """Verify references using external APIs."""
    ref_hash = hashlib.md5(reference.encode()).hexdigest()

    if ref_hash in cache:
        return cache[ref_hash]

    services = [
        {"name": "CrossRef", "url": "https://api.crossref.org/works", "params": {"query.bibliographic": reference}},
        {"name": "Google Scholar", "url": "https://scholar.google.com/scholar", "params": {"q": reference}}
    ]

    result = {"service": "N/A", "status": "failed"}

    for service in services:
        try:
            time.sleep(CONFIG["api_delay"])
            response = requests.get(service["url"], params=service["params"], timeout=15)
            response.raise_for_status()
            result = {"service": service["name"], "status": "success", "data": response.json()}
            break
        except requests.RequestException as e:
            logging.warning(f"{service['name']} failed: {str(e)}")

    cache[ref_hash] = result
    return result
