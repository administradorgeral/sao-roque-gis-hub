import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes

doc = pdfium.PdfDocument(r'js/maps_pdf/temas/Mapa_Anexo_8.3.1-1_Zoneamento_2019.pdf')
page = doc[0]
objs = list(page.get_objects())

slope_x, intercept_x = 17.637839, 271182.44
slope_y, intercept_y = 17.638906, 7381568.28

def pdf_to_utm(px, py):
    return (slope_x * px + intercept_x, slope_y * py + intercept_y)

r, g, b, a = ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint()
fm, st = ctypes.c_int(), ctypes.c_int()
x, y = ctypes.c_float(), ctypes.c_float()
left, bottom, right, top = ctypes.c_float(), ctypes.c_float(), ctypes.c_float(), ctypes.c_float()

red_strokes = []

for idx, p in enumerate(objs):
    if type(p).__name__ == 'PdfObject':
        pdfium_c.FPDFPath_GetDrawMode(p.raw, ctypes.byref(fm), ctypes.byref(st))
        if st.value != 0:
            pdfium_c.FPDFPageObj_GetStrokeColor(p.raw, ctypes.byref(r), ctypes.byref(g), ctypes.byref(b), ctypes.byref(a))
            s_hex = f'#{r.value:02X}{g.value:02X}{b.value:02X}'
            pdfium_c.FPDFPageObj_GetBounds(p.raw, ctypes.byref(left), ctypes.byref(bottom), ctypes.byref(right), ctypes.byref(top))
            # Red color (high red, low green/blue, e.g. #FF0000, #E60000, #C00000, etc.)
            if r.value > 180 and g.value < 50 and b.value < 50:
                n_segs = pdfium_c.FPDFPath_CountSegments(p.raw)
                w = right.value - left.value
                h = top.value - bottom.value
                red_strokes.append({
                    'idx': idx,
                    'color': s_hex,
                    'bounds': (round(left.value, 1), round(bottom.value, 1), round(right.value, 1), round(top.value, 1)),
                    'w': round(w, 1),
                    'h': round(h, 1),
                    'n_segs': n_segs,
                    'fm': fm.value,
                    'st': st.value
                })

print(f"Found {len(red_strokes)} red stroke objects:")
for rs in red_strokes:
    print(f"  Idx={rs['idx']}, Color={rs['color']}, Segs={rs['n_segs']}, Bounds={rs['bounds']}, W={rs['w']}, H={rs['h']}")
