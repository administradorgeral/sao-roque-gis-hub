import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes

doc = pdfium.PdfDocument(r'js/maps_pdf/temas/Mapa_Anexo_8.3.1-1_Zoneamento_2019.pdf')
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
            pdfium_c.FPDFPageObj_GetFillColor(p.raw, ctypes.byref(r), ctypes.byref(g), ctypes.byref(b), ctypes.byref(a))
            f_hex = f'#{r.value:02X}{g.value:02X}{b.value:02X}'
            w = right.value - left.value
            h = top.value - bottom.value
            if 1100 <= left.value <= 1350 and 1000 <= bottom.value <= 1550 and 10 <= w <= 80 and 8 <= h <= 40:
                swatches.append((idx, f_hex, left.value, bottom.value, right.value, top.value))

print(f"Found {len(swatches)} swatches in legend box:")
for s in sorted(swatches, key=lambda x: -x[3]):
    idx, f_hex, l, bot, r_val, t = s
    nearby = []
    for i in range(tp.count_chars()):
        cb = tp.get_charbox(i)
        if r_val <= cb[0] <= r_val + 350 and bot - 10 <= cb[1] <= t + 10:
            nearby.append((cb[0], tp.get_text_range(i, 1)))
    nearby.sort(key=lambda x: x[0])
    text = ''.join(c[1] for c in nearby).strip()
    print(f"  Swatch {f_hex} at Y={bot:.1f}..{t:.1f}: '{text}'")
