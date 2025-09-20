#!/usr/bin/env python3
"""
Converter PDF em chunks menores para processar gradualmente
"""

import pymupdf
import os
from pathlib import Path

def chunk_pdf_convert():
    """Converte PDF por seções para evitar timeout"""

    pdf_path = "docs/Breakthrough_Advertising_-_Eugene_Schwartz.pdf"

    print("=" * 60)
    print("PROCESSANDO BREAKTHROUGH ADVERTISING EM CHUNKS")
    print("=" * 60)

    try:
        # Abrir PDF
        doc = pymupdf.open(pdf_path)
        total_pages = len(doc)

        print(f"PDF: {total_pages} páginas")
        print("Extraindo texto por seções...")

        # Processar em chunks de 10 páginas
        chunk_size = 10
        all_text = []

        for start_page in range(0, total_pages, chunk_size):
            end_page = min(start_page + chunk_size, total_pages)
            print(f"Processando páginas {start_page+1}-{end_page}...")

            chunk_text = ""
            for page_num in range(start_page, end_page):
                page = doc[page_num]
                text = page.get_text()
                chunk_text += f"\n\n--- PÁGINA {page_num + 1} ---\n\n"
                chunk_text += text

            all_text.append(chunk_text)

        doc.close()

        # Combinar todo o texto
        full_text = "\n".join(all_text)

        # Salvar como MD
        output_path = "docs/breakthrough_advertising.md"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# Breakthrough Advertising - Eugene Schwartz\n\n")
            f.write(full_text)

        # Estatísticas
        file_size = os.path.getsize(output_path)
        lines = len(full_text.split('\n'))
        words = len(full_text.split())

        print(f"\nSUCESSO!")
        print(f"Arquivo: {output_path}")
        print(f"Tamanho: {file_size:,} bytes")
        print(f"Linhas: {lines:,}")
        print(f"Palavras: {words:,}")

        # Preview
        preview = full_text[:500] + "..."
        print(f"\nPREVIEW:\n{preview}")

        print("\n" + "=" * 60)
        print("PRÓXIMO: Quebrar em chunks para RAG")
        print("=" * 60)

        return True

    except Exception as e:
        print(f"ERRO: {e}")
        return False

if __name__ == "__main__":
    chunk_pdf_convert()