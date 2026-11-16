import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes
from collections import Counter

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\40537_4_3_3_1 Declividade.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]

objs = list(page.get_objects())
path_objs = [obj for obj in objs if obj.type == 2]

stroke_colors = Counter()
fill_colors = Counter()

r, g, b, a = ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint()

for p in path_objs[:5000]:
    if pdfium_c.FPDFPageObj_GetStrokeColor(p.raw, ctypes.byref(r), ctypes.byref(g), ctypes.byref(b), ctypes.byref(a)):
        stroke_colors[(r.value, g.value, b.value, a.value)] += 1
    if pdfium_c.FPDFPageObj_GetFillColor(p.raw, ctypes.byref(r), ctypes.byref(g), ctypes.byref(b), ctypes.byref(a)):
        fill_colors[(r.value, g.value, b.value, a.value)] += 1

print("Cores de Stroke (amostra de 5000):")
for col, cnt in stroke_colors.most_common(10):
    hex_col = f"#{col[0]:02X}{col[1]:02X}{col[2]:02X} (alpha={col[3]})"
    print(f"  {hex_col}: {cnt}")

print("\nCores de Fill (amostra de 5000):")
for col, cnt in fill_colors.most_common(10):
    hex_col = f"#{col[0]:02X}{col[1]:02X}{col[2]:02X} (alpha={col[3]})"
    print(f"  {hex_col}: {cnt}")

# Vamos ver o tamanho dos segmentos dos paths
seg_counts = Counter()
for p in path_objs[:1000]:
    c = pdfium_c.FPDFPath_CountSegments(p.raw)
    seg_counts[c] += 1

print("\nContagem de segmentos por path:")
for s, cnt in seg_counts.most_common(10):
    print(f"  {s} segmentos: {cnt} paths")

doc.close()
