import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes
from collections import Counter

doc = pdfium.PdfDocument(r'js/maps_pdf/temas/Mapa_Anexo_8.3.1-1_Zoneamento_2019.pdf')
page = doc[0]
objs = list(page.get_objects())

r, g, b, a = ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint()
fm, st = ctypes.c_int(), ctypes.c_int()
left, bottom, right, top = ctypes.c_float(), ctypes.c_float(), ctypes.c_float(), ctypes.c_float()

all_fills = Counter()

for idx, p in enumerate(objs):
    if type(p).__name__ == 'PdfObject':
        pdfium_c.FPDFPath_GetDrawMode(p.raw, ctypes.byref(fm), ctypes.byref(st))
        if fm.value != 0:
            pdfium_c.FPDFPageObj_GetBounds(p.raw, ctypes.byref(left), ctypes.byref(bottom), ctypes.byref(right), ctypes.byref(top))
            # if inside map area
            if left.value < 1650 and not (left.value > 1100 and bottom.value > 1050):
                pdfium_c.FPDFPageObj_GetFillColor(p.raw, ctypes.byref(r), ctypes.byref(g), ctypes.byref(b), ctypes.byref(a))
                f_hex = f'#{r.value:02X}{g.value:02X}{b.value:02X}'
                w = right.value - left.value
                h = top.value - bottom.value
                if w > 10 and h > 10:
                    all_fills[f_hex] += 1
                    print(f"Fill #{idx}: {f_hex}, bounds=({left.value:.1f}, {bottom.value:.1f}, {right.value:.1f}, {top.value:.1f}), w={w:.1f}, h={h:.1f}")

print("\nSummary of fills in map:")
for c, cnt in all_fills.items():
    print(f"  {c}: {cnt}")
