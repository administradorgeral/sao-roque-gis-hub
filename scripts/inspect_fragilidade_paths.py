import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\Mapa Fragilidade Potencial.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]
objs = list(page.get_objects())

r_val, g_val, b_val, a_val = ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint()
fm, st = ctypes.c_int(), ctypes.c_int()
left, bottom, right, top = ctypes.c_float(), ctypes.c_float(), ctypes.c_float(), ctypes.c_float()

color_counts = {}
filled_count = 0
in_map_count = 0

for i, p in enumerate(objs):
    if type(p).__name__ == 'PdfObject':
        pdfium_c.FPDFPath_GetDrawMode(p.raw, ctypes.byref(fm), ctypes.byref(st))
        if fm.value != 0:
            filled_count += 1
            pdfium_c.FPDFPageObj_GetBounds(p.raw, ctypes.byref(left), ctypes.byref(bottom), ctypes.byref(right), ctypes.byref(top))
            # Check if in map area (X < 1675)
            if right.value <= 1675 and left.value >= 25:
                in_map_count += 1
                pdfium_c.FPDFPageObj_GetFillColor(p.raw, ctypes.byref(r_val), ctypes.byref(g_val), ctypes.byref(b_val), ctypes.byref(a_val))
                f_hex = f"#{r_val.value:02X}{g_val.value:02X}{b_val.value:02X}"
                color_counts[f_hex] = color_counts.get(f_hex, 0) + 1

print(f"Total filled objects: {filled_count}")
print(f"Filled objects in map area: {in_map_count}")
print("Colors in map area:")
for c, cnt in sorted(color_counts.items(), key=lambda x: -x[1]):
    print(f"  {c}: {cnt} paths")
