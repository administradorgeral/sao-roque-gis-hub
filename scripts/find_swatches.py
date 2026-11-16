import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes

doc = pdfium.PdfDocument(r'js/maps_pdf/temas/Mapa Fragilidade Potencial.pdf')
page = doc[0]
objs = list(page.get_objects())
tp = page.get_textpage()

r, g, b, a = ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint()
fm, st = ctypes.c_int(), ctypes.c_int()
left, bottom, right, top = ctypes.c_float(), ctypes.c_float(), ctypes.c_float(), ctypes.c_float()

swatches = []
for idx, p in enumerate(objs):
    if type(p).__name__ == 'PdfObject':
        pdfium_c.FPDFPath_GetDrawMode(p.raw, ctypes.byref(fm), ctypes.byref(st))
        if fm.value != 0:
            pdfium_c.FPDFPageObj_GetBounds(p.raw, ctypes.byref(left), ctypes.byref(bottom), ctypes.byref(right), ctypes.byref(top))
            w = right.value - left.value
            h = top.value - bottom.value
            if 5 <= w <= 80 and 5 <= h <= 80 and left.value > 800:
                pdfium_c.FPDFPageObj_GetFillColor(p.raw, ctypes.byref(r), ctypes.byref(g), ctypes.byref(b), ctypes.byref(a))
                f_hex = f'#{r.value:02X}{g.value:02X}{b.value:02X}'
                swatches.append((idx, f_hex, left.value, bottom.value, right.value, top.value))

print(f'Found {len(swatches)} candidate swatches:')
for s in swatches:
    idx, f_hex, l, bot, r_val, t = s
    nearby_text = []
    for i in range(tp.count_chars()):
        cb = tp.get_charbox(i)
        if r_val <= cb[0] <= r_val + 200 and bot - 10 <= cb[1] <= t + 10:
            nearby_text.append((cb[0], tp.get_text_range(i, 1)))
    nearby_text.sort(key=lambda x: x[0])
    text = ''.join(c[1] for c in nearby_text).strip()
    if text:
        print(f'Swatch #{idx}: {f_hex} at ({l:.1f}, {bot:.1f}, {r_val:.1f}, {t:.1f}) -> Text: "{text}"')
