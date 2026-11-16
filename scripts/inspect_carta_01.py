import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes
import os

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\minuta_pd2026\desmembrado\02_cartas_tecnicas\carta_01_macrozoneamento_municipal.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]

w, h = page.get_size()
print(f"Carta I dimensões do PDF: {w:.1f} x {h:.1f} pt")

tp = page.get_textpage()
n_chars = tp.count_chars()
text = tp.get_text_range(0, n_chars) if n_chars > 0 else ""

print(f"Total de caracteres de texto: {n_chars}")
lines = [l.strip() for l in text.split("\n") if l.strip()]

print("\n--- Amostra do Texto / Legenda / Carimbo ---")
for l in lines[:60]:
    print("  ", l)

# Scan for UTM or Lat/Lon ticks in the text
coord_lines = [l for l in lines if any(k in l for k in ["7.", "2.", "3.", "23°", "47°", "UTM", "SIRGAS", "FUSO"])]
print(f"\nLinhas com possíveis coordenadas/referências ({len(coord_lines)}):")
for cl in coord_lines[:30]:
    print("   [COORD?]", cl)
