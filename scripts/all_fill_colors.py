import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes
from collections import Counter

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\40537_4_3_3_1 Declividade.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]

objs = list(page.get_objects())
path_objs = [obj for obj in objs if obj.type == 2]
print(f"Total de paths: {len(path_objs)}")

fill_colors = Counter()
r, g, b, a = ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint()

# Amostrar a cada 10 paths para ir super rápido em 158k
for i in range(0, len(path_objs), 5):
    p = path_objs[i]
    if pdfium_c.FPDFPageObj_GetFillColor(p.raw, ctypes.byref(r), ctypes.byref(g), ctypes.byref(b), ctypes.byref(a)):
        fill_colors[(r.value, g.value, b.value, a.value)] += 1

print("\nTodas as Cores de Preenchimento (Fill) encontradas nos caminhos vetoriais:")
for col, cnt in fill_colors.most_common(20):
    hex_col = f"#{col[0]:02X}{col[1]:02X}{col[2]:02X}"
    print(f"  {hex_col} (RGB {col[0]}, {col[1]}, {col[2]}, alpha={col[3]}): {cnt * 5} ocorrências estimadas")

doc.close()
