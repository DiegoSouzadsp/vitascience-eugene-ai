#!/usr/bin/env python3
"""
Converter PDF Breakthrough Advertising para Markdown
Processamento otimizado para vetorização RAG
"""

import pymupdf4llm
import os
from pathlib import Path

def convert_breakthrough_advertising():
    """Converte PDF do Eugene Schwartz para MD"""

    pdf_path = "docs/Breakthrough_Advertising_-_Eugene_Schwartz.pdf"
    output_path = "docs/breakthrough_advertising.md"

    print("=" * 60)
    print("CONVERTENDO BREAKTHROUGH ADVERTISING PDF -> MD")
    print("=" * 60)
    print(f"Input: {pdf_path}")
    print(f"Output: {output_path}")

    # Verificar se arquivo existe
    if not Path(pdf_path).exists():
        print(f"ERRO: Arquivo {pdf_path} não encontrado")
        return False

    try:
        print("Convertendo PDF para Markdown...")

        # Converter PDF para MD usando pymupdf4llm
        md_text = pymupdf4llm.to_markdown(pdf_path)

        # Salvar arquivo MD
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(md_text)

        # Verificar resultado
        file_size = os.path.getsize(output_path)
        lines = len(md_text.split('\n'))

        print(f"SUCESSO!")
        print(f"Arquivo MD criado: {output_path}")
        print(f"Tamanho: {file_size:,} bytes")
        print(f"Linhas: {lines:,}")

        # Preview das primeiras linhas
        preview_lines = md_text.split('\n')[:20]
        print("\nPREVIEW DO CONTEUDO:")
        print("-" * 40)
        for i, line in enumerate(preview_lines, 1):
            if line.strip():
                print(f"{i:2d}: {line[:80]}...")

        print("=" * 60)
        print("PROXIMO PASSO: Quebrar em chunks para RAG")
        print("Execute: python scripts/chunk_and_vectorize.py")
        print("=" * 60)

        return True

    except Exception as e:
        print(f"ERRO na conversao: {e}")
        return False

if __name__ == "__main__":
    convert_breakthrough_advertising()