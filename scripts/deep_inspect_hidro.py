import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes
from collections import Counter

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\Hidro .pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]

objs = list(page.get_objects())
path_objs = [obj for obj in objs if obj.type == 2]
text_objs = [obj for obj in objs if obj.type == 1]
image_objs = [obj for obj in objs if obj.type == 3]

print(f"PATH objs: {len(path_objs)}")
print(f"TEXT objs: {len(text_objs)}")
print(f"IMAGE objs: {len(image_objs)}")

stroke_colors = Counter()
fill_colors = Counter()

r, g, b, a = ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint()

for p in path_objs:
    if pdfium_c.FPDFPageObj_GetStrokeColor(p.raw, ctypes.byref(r), ctypes.byref(g), ctypes.byref(b), ctypes.byref(a)):
        stroke_colors[(r.value, g.value, b.value, a.value)] += 1
    if pdfium_c.FPDFPageObj_GetFillColor(p.raw, ctypes.byref(r), ctypes.byref(g), ctypes.byref(b), ctypes.byref(a)):
        fill_colors[(r.value, g.value, b.value, a.value)] += 1

print("\n--- CORES DE LINHA (STROKE) DOS PATHS ---")
for col, cnt in stroke_colors.most_common(20):
    hex_col = f"#{col[0]:02X}{col[1]:02X}{col[2]:02X} (alpha={col[3]})"
    print(f"  {hex_col}: {cnt} vetores")

print("\n--- CORES DE PREENCHIMENTO (FILL) DOS PATHS ---")
for col, cnt in fill_colors.most_common(20):
    hex_col = f"#{col[0]:02X}{col[1]:02X}{col[2]:02X} (alpha={col[3]})"
    print(f"  {hex_col}: {cnt} vetores")

print("\n--- IMAGENS NO PDF ---")
for i, img in enumerate(image_objs):
    b = img.get_bounds()
    px = img.get_px_size()
    print(f"  Img {i}: bounds={b}, px_size={px}")

doc.close()
