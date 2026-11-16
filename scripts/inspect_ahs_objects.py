import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes

pdf_path = "C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/js/maps_pdf/temas/34229_4.2.5.1-1 AHS.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]
objs = list(page.get_objects())

r, g, b, a = ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint()
fm, st = ctypes.c_int(), ctypes.c_int()
left, bottom, right, top = ctypes.c_float(), ctypes.c_float(), ctypes.c_float(), ctypes.c_float()

ahs_objs = []
other_objs = []

for idx, p in enumerate(objs):
    if type(p).__name__ == 'PdfObject':
        pdfium_c.FPDFPath_GetDrawMode(p.raw, ctypes.byref(fm), ctypes.byref(st))
        if fm.value != 0:
            pdfium_c.FPDFPageObj_GetFillColor(p.raw, ctypes.byref(r), ctypes.byref(g), ctypes.byref(b), ctypes.byref(a))
            f_hex = f"#{r.value:02X}{g.value:02X}{b.value:02X}"
            pdfium_c.FPDFPageObj_GetBounds(p.raw, ctypes.byref(left), ctypes.byref(bottom), ctypes.byref(right), ctypes.byref(top))
            w = right.value - left.value
            h = top.value - bottom.value
            if f_hex == "#A80084":
                n_segs = pdfium_c.FPDFPath_CountSegments(p.raw)
                ahs_objs.append((idx, left.value, bottom.value, right.value, top.value, w, h, n_segs))
            else:
                other_objs.append((idx, f_hex, left.value, bottom.value, right.value, top.value, w, h))

print(f"Total AHS (#A80084) objects: {len(ahs_objs)}")
if ahs_objs:
    min_x = min(o[1] for o in ahs_objs)
    min_y = min(o[2] for o in ahs_objs)
    max_x = max(o[3] for o in ahs_objs)
    max_y = max(o[4] for o in ahs_objs)
    print(f"AHS BBox (pt): X=[{min_x:.1f}, {max_x:.1f}], Y=[{min_y:.1f}, {max_y:.1f}]")
    print("Primeiros 5 objetos AHS:")
    for o in ahs_objs[:5]:
        print(f"  idx={o[0]}: bounds=[{o[1]:.1f}, {o[2]:.1f}, {o[3]:.1f}, {o[4]:.1f}], size={o[5]:.1f}x{o[6]:.1f}, segs={o[7]}")
    print("Últimos 5 objetos AHS:")
    for o in ahs_objs[-5:]:
        print(f"  idx={o[0]}: bounds=[{o[1]:.1f}, {o[2]:.1f}, {o[3]:.1f}, {o[4]:.1f}], size={o[5]:.1f}x{o[6]:.1f}, segs={o[7]}")

print(f"\nOther fill objects: {len(other_objs)}")
for o in other_objs:
    print(f"  idx={o[0]}: color={o[1]}, bounds=[{o[2]:.1f}, {o[3]:.1f}, {o[4]:.1f}, {o[5]:.1f}], size={o[6]:.1f}x{o[7]:.1f}")
