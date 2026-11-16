import pypdfium2 as pdfium, ctypes
import pypdfium2.raw as pdfium_c

pdf_path = 'js/maps_pdf/temas/zoneamento_rbcv_2019.pdf'
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]

objs = list(page.get_objects())
left, bottom, right, top = ctypes.c_float(), ctypes.c_float(), ctypes.c_float(), ctypes.c_float()
r, g, b, a = ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint()
fm, st = ctypes.c_int(), ctypes.c_int()

red_squares = []

for i, p in enumerate(objs):
    if p.type == pdfium.raw.FPDF_PAGEOBJ_PATH:
        pdfium_c.FPDFPath_GetDrawMode(p.raw, ctypes.byref(fm), ctypes.byref(st))
        if fm.value != 0:
            pdfium_c.FPDFPageObj_GetFillColor(p.raw, ctypes.byref(r), ctypes.byref(g), ctypes.byref(b), ctypes.byref(a))
            c = f'#{r.value:02X}{g.value:02X}{b.value:02X}'
            if c == '#FF0000':
                pdfium_c.FPDFPageObj_GetBounds(p.raw, ctypes.byref(left), ctypes.byref(bottom), ctypes.byref(right), ctypes.byref(top))
                cx = (left.value + right.value) / 2
                cy = (bottom.value + top.value) / 2
                red_squares.append((i, cx, cy, right.value - left.value, top.value - bottom.value))

print(f"Total red squares: {len(red_squares)}")
# Sort by cx (west to east)
red_squares.sort(key=lambda s: s[1])
print("Westernmost 10 red squares (closest to São Roque / Vargem Grande / Cotia):")
for s in red_squares[:10]:
    print(f"  #{s[0]}: cx={s[1]:.2f}, cy={s[2]:.2f}, size=({s[3]:.2f}x{s[4]:.2f})")

print("\nEasternmost 5 red squares:")
for s in red_squares[-5:]:
    print(f"  #{s[0]}: cx={s[1]:.2f}, cy={s[2]:.2f}")
