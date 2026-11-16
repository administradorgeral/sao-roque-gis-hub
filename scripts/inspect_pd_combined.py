import pypdfium2 as pdfium
import os

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\minuta_pd2026\Plano Diretor - Combined.pdf"
doc = pdfium.PdfDocument(pdf_path)

print(f"Total de páginas: {len(doc)}")
print("--- Sumário / Bookmarks ---")

for item in doc.get_toc():
    title = item.get_title()
    dest = item.get_dest()
    p_idx = dest.get_index() if dest else None
    page_str = str(p_idx + 1) if p_idx is not None else "N/A"
    indent = "  " * item.level
    print(f"{indent}* {title} -> Pág. {page_str}")
