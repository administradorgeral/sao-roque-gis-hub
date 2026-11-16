import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes
import time
from shapely.geometry import Polygon
from shapely.affinity import affine_transform

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\40537_4_3_3_1 Declividade.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]

t0 = time.time()
objs = list(page.get_objects())
path_objs = [obj for obj in objs if obj.type == 2]
print(f"Carregados {len(path_objs)} paths em {time.time()-t0:.2f}s")

# Cores alvo
color_map = {
    "#FFFF73": "Plano (0-3%)",
    "#FFFF00": "Suave ondulado (3-8%)",
    "#FFAA00": "Ondulado (8-20%)",
    "#FF5500": "Forte ondulado (20-45%)",
    "#E60000": "Montanhoso (45-75%)"
}

r, g, b, a = ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint()
x = ctypes.c_float()
y = ctypes.c_float()

extracted = []
t1 = time.time()
for p in path_objs[:1000]:
    pdfium_c.FPDFPageObj_GetFillColor(p.raw, ctypes.byref(r), ctypes.byref(g), ctypes.byref(b), ctypes.byref(a))
    hex_col = f"#{r.value:02X}{g.value:02X}{b.value:02X}"
    if hex_col in color_map:
        n_seg = pdfium_c.FPDFPath_CountSegments(p.raw)
        coords = []
        for s in range(n_seg):
            seg = pdfium_c.FPDFPath_GetPathSegment(p.raw, s)
            pdfium_c.FPDFPathSegment_GetPoint(seg, ctypes.byref(x), ctypes.byref(y))
            coords.append((x.value, y.value))
        if len(coords) >= 3:
            extracted.append((hex_col, coords))

print(f"Extraídos {len(extracted)} polígonos de 1000 paths em {time.time()-t1:.2f}s")

# Criar polígonos Shapely
t2 = time.time()
polys = []
for col, ring in extracted:
    if ring[0] != ring[-1]:
        ring.append(ring[0])
    try:
        p = Polygon(ring)
        if p.is_valid and p.area > 0.01:
            polys.append((col, p))
    except Exception:
        pass

print(f"Criados {len(polys)} polígonos Shapely válidos em {time.time()-t2:.2f}s")
doc.close()
