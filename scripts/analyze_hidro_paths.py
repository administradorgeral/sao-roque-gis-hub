import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes
from collections import Counter

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\Hidro .pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]

objs = list(page.get_objects())
path_objs = [obj for obj in objs if obj.type == 2]

print(f"Total PATH objects: {len(path_objs)}")

# Analisar características de cada path
categories = Counter()
color_combos = Counter()
seg_counts = Counter()

r, g, b, a = ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint()

for i, p in enumerate(path_objs):
    s_col = None
    f_col = None
    
    if pdfium_c.FPDFPageObj_GetStrokeColor(p.raw, ctypes.byref(r), ctypes.byref(g), ctypes.byref(b), ctypes.byref(a)):
        s_col = (r.value, g.value, b.value)
    if pdfium_c.FPDFPageObj_GetFillColor(p.raw, ctypes.byref(r), ctypes.byref(g), ctypes.byref(b), ctypes.byref(a)):
        f_col = (r.value, g.value, b.value)
        
    s_hex = f"#{s_col[0]:02X}{s_col[1]:02X}{s_col[2]:02X}" if s_col else "NONE"
    f_hex = f"#{f_col[0]:02X}{f_col[1]:02X}{f_col[2]:02X}" if f_col else "NONE"
    
    n_segs = pdfium_c.FPDFPath_CountSegments(p.raw)
    seg_counts[n_segs] += 1
    
    # Categorizar por cor
    # #0A93FC = Córregos secundários / nascentes / afluentes
    # #4065EB = Rios principais (Rio Guaçu, Rio Carambeí, etc.)
    # #97DBF2 = Represas e corpos d'água poligonais
    # #000000 = Limite / grid / neatline
    combo = f"Stroke={s_hex} | Fill={f_hex}"
    color_combos[combo] += 1

print("\n--- COMBINAÇÕES DE CORES (STROKE E FILL) ---")
for combo, cnt in color_combos.most_common(20):
    print(f"  {combo}: {cnt} paths")

print("\n--- DISTRIBUIÇÃO DE SEGMENTOS ---")
for s, cnt in seg_counts.most_common(15):
    print(f"  {s} segmentos: {cnt} paths")

doc.close()
