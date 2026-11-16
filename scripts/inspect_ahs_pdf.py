import pypdf
import pypdfium2 as pdfium
import os

pdf_path = "C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/js/maps_pdf/temas/34229_4.2.5.1-1 AHS.pdf"

print("=== INSPEÇÃO GERAL DO PDF AHS ===")
print("Arquivo:", pdf_path)
print("Tamanho:", os.path.getsize(pdf_path), "bytes")

# 1. Leitura de Texto com pypdf
reader = pypdf.PdfReader(pdf_path)
print(f"Número de páginas: {len(reader.pages)}")
page = reader.pages[0]
print(f"MediaBox: {page.mediabox}")
text = page.extract_text()
print(f"Texto extraído ({len(text)} caracteres):")
lines = text.split("\n")
for l in lines[:40]:
    if l.strip():
        print("  ", l.strip())

# 2. Leitura com pypdfium2 para inspecionar objetos
pdf = pdfium.PdfDocument(pdf_path)
p0 = pdf[0]
width, height = p0.get_size()
print(f"Tamanho pypdfium2: {width} x {height} pt")

# Contar tipos de objetos
n_objs = p0.count_objects()
print(f"Total de objetos na página: {n_objs}")

text_page = p0.get_textpage()
n_chars = text_page.count_chars()
print(f"Total de caracteres de texto no textpage: {n_chars}")

# Buscar palavras de legenda e UTM no texto
print("\n--- Linhas com coordenadas UTM ou palavras-chave ---")
full_text = text_page.get_text_range()
for line in full_text.split("\r\n"):
    line = line.strip()
    if any(k in line.lower() for k in ["ahs", "hidro", "sensiv", "sensív", "nascente", "73", "74", "27", "28", "29", "escala", "anexo"]):
        print("  >", line)
