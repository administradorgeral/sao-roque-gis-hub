import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes
from shapely.geometry import Polygon
from shapely.validation import make_valid

doc = pdfium.PdfDocument(r'js/maps_pdf/temas/1835_4_3_6_1 Pedológico.pdf')
page = doc[0]
objs = list(page.get_objects())

slope_x, intercept_x = 17.636295, 272427.45
slope_y, intercept_y = 17.636560, 7381364.75

def pdf_to_utm(px, py):
    return (slope_x * px + intercept_x, slope_y * py + intercept_y)

r, g, b, a = ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint()
sr, sg, sb, sa = ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint()
fm, st = ctypes.c_int(), ctypes.c_int()
x, y = ctypes.c_float(), ctypes.c_float()
left, bottom, right, top = ctypes.c_float(), ctypes.c_float(), ctypes.c_float(), ctypes.c_float()

path_objects = []

for idx, p in enumerate(objs):
    if type(p).__name__ == 'PdfObject':
        pdfium_c.FPDFPath_GetDrawMode(p.raw, ctypes.byref(fm), ctypes.byref(st))
        pdfium_c.FPDFPageObj_GetBounds(p.raw, ctypes.byref(left), ctypes.byref(bottom), ctypes.byref(right), ctypes.byref(top))
        pdfium_c.FPDFPageObj_GetFillColor(p.raw, ctypes.byref(r), ctypes.byref(g), ctypes.byref(b), ctypes.byref(a))
        pdfium_c.FPDFPageObj_GetStrokeColor(p.raw, ctypes.byref(sr), ctypes.byref(sg), ctypes.byref(sb), ctypes.byref(sa))
        f_hex = f"#{r.value:02X}{g.value:02X}{b.value:02X}"
        s_hex = f"#{sr.value:02X}{sg.value:02X}{sb.value:02X}"
        n_segs = pdfium_c.FPDFPath_CountSegments(p.raw)
        
        # If in map area
        if left.value < 1675 and top.value > 100:
            path_objects.append({
                'idx': idx,
                'fill_mode': fm.value,
                'stroke_mode': st.value,
                'fill_hex': f_hex,
                'stroke_hex': s_hex,
                'bounds': (round(left.value, 1), round(bottom.value, 1), round(right.value, 1), round(top.value, 1)),
                'n_segs': n_segs
            })

print(f"Total path objects in map area: {len(path_objects)}")
# Group by fill_mode
fills = [p for p in path_objects if p['fill_mode'] != 0]
strokes_only = [p for p in path_objects if p['fill_mode'] == 0 and p['stroke_mode'] != 0]

print(f"Filled path objects: {len(fills)}")
for f in fills:
    print(f"  Idx={f['idx']}, Fill={f['fill_hex']}, Stroke={f['stroke_hex']}, Segs={f['n_segs']}, Bounds={f['bounds']}")

print(f"\nStroke-only path objects: {len(strokes_only)}")
for s in strokes_only[:15]:
    print(f"  Idx={s['idx']}, Stroke={s['stroke_hex']}, Segs={s['n_segs']}, Bounds={s['bounds']}")
