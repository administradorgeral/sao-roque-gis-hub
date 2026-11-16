import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes
from shapely.geometry import Polygon, Point
from shapely.validation import make_valid

doc = pdfium.PdfDocument(r'js/maps_pdf/temas/1835_4_3_6_1 Pedológico.pdf')
page = doc[0]
objs = list(page.get_objects())

slope_x, intercept_x = 17.636295, 272427.45
slope_y, intercept_y = 17.636560, 7381364.75

def pdf_to_utm(px, py):
    return (slope_x * px + intercept_x, slope_y * py + intercept_y)

r, g, b, a = ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint()
fm, st = ctypes.c_int(), ctypes.c_int()
x, y = ctypes.c_float(), ctypes.c_float()

soil_polys = []

for idx in [1, 2, 3, 4, 5, 6]:
    p = objs[idx]
    pdfium_c.FPDFPageObj_GetFillColor(p.raw, ctypes.byref(r), ctypes.byref(g), ctypes.byref(b), ctypes.byref(a))
    f_hex = f"#{r.value:02X}{g.value:02X}{b.value:02X}"
    n_segs = pdfium_c.FPDFPath_CountSegments(p.raw)
    current_sp = []
    subpaths = []
    for s in range(n_segs):
        seg = pdfium_c.FPDFPath_GetPathSegment(p.raw, s)
        stype = pdfium_c.FPDFPathSegment_GetType(seg)
        pdfium_c.FPDFPathSegment_GetPoint(seg, ctypes.byref(x), ctypes.byref(y))
        pt = pdf_to_utm(x.value, y.value)
        if stype == pdfium_c.FPDF_SEGMENT_MOVETO:
            if len(current_sp) >= 3:
                subpaths.append(current_sp)
            current_sp = [pt]
        else:
            current_sp.append(pt)
    if len(current_sp) >= 3:
        subpaths.append(current_sp)
    
    # Construct polygon
    sp0 = subpaths[0]
    if sp0[0] != sp0[-1]:
        sp0.append(sp0[0])
    holes = []
    for h in subpaths[1:]:
        if len(h) >= 3:
            if h[0] != h[-1]:
                h.append(h[0])
            holes.append(h)
    poly = Polygon(sp0, holes)
    if not poly.is_valid:
        poly = make_valid(poly)
    soil_polys.append((idx, f_hex, poly))

# Map labels we found:
labels = [
    ("PVA19", 286473.4, 7394200.1),
    ("PVA41", 282778.2, 7400388.2),
    ("PVA46_NW", 278714.7, 7407139.2),
    ("PVA55", 278045.9, 7401882.3),
    ("PVA46_NE", 288636.4, 7400527.9),
    ("LVA17", 283291.6, 7385950.7),
]

print("=== SOIL POLYGONS & LABELS ===")
total_ha = 0.0
for idx, f_hex, poly in soil_polys:
    area_ha = poly.area / 10000.0
    total_ha += area_ha
    matched_labels = []
    for name, lx, ly in labels:
        if poly.contains(Point(lx, ly)):
            matched_labels.append(name)
    print(f"Object #{idx}: Color={f_hex}, Area={area_ha:.2f} ha ({area_ha/307.0952:.1f}%), Matched: {matched_labels}")

print(f"\nTOTAL SOIL AREA: {total_ha:.2f} ha (PDA São Roque: 30.709,52 ha)")
