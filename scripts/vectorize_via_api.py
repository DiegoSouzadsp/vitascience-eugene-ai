#!/usr/bin/env python3
"""
Vectorize Eugene book via RAG API
"""

import requests
import json
import os

def process_eugene_book():
    """Process Eugene book via RAG API"""

    print("=== VECTORIZING EUGENE BOOK VIA API ===")

    # Check if markdown file exists
    md_path = "docs/breakthrough_advertising.md"
    if not os.path.exists(md_path):
        print(f"ERROR: {md_path} not found")
        return False

    # Load the markdown content
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    print(f"Loaded: {len(content):,} characters")

    # Call RAG API to process the book
    url = "http://localhost:8000/process-book"

    try:
        response = requests.post(url,
            json={"pdf_path": md_path},
            timeout=300
        )

        if response.status_code == 200:
            result = response.json()
            print(f"Processing started: {result}")
            return True
        else:
            print(f"API Error: {response.status_code} - {response.text}")
            return False

    except Exception as e:
        print(f"Request failed: {e}")
        return False

if __name__ == "__main__":
    process_eugene_book()