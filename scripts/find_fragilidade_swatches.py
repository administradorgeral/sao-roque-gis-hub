import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\Mapa Fragilidade Potencial.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]
objs = list(page.get_objects())
tp = page.get_textpage()

r_val, g_val, b_val, a_val = ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint()
fm, st = ctypes.c_int(), ctypes.c_int()
left, bottom, right, top = ctypes.c_float(), ctypes.c_float(), ctypes.c_float(), ctypes.c_float()

print(f"Total objects: {len(objs)}")

# Search for small filled rectangles near legend (X between 1600 and 1900, Y between 950 and 1200)
swatches = []
for i, p in enumerate(objs):
    if type(p).__name__ == 'PdfObject':
        pdfium_c.FPDFPath_GetDrawMode(p.raw, ctypes.byref(fm), ctypes.byref(st))
        if fm.value != 0:
            pdfium_c.FPDFPageObj_GetBounds(p.raw, ctypes.byref(left), ctypes.byref(bottom), ctypes.byref(right), ctypes.byref(top))
            w = right.value - left.value
            h = top.value - bottom.value
            # Check if it looks like a legend swatch (width 20-80, height 10-40)
            if 1600 <= left.value <= 2200 and 950 <= bottom.value <= 1250 and 15 <= w <= 80 and 8 <= h <= 40:
                pdfium_c.FPDFPageObj_GetFillColor(p.raw, ctypes.byref(r_val), ctypes.byref(g_val), ctypes.byref(b_val), ctypes.byref(a_val))
                f_hex = f"#{r_val.value:02X}{g_val.value:02X}{b_val.value:02X}"
                # Grab text nearby
                txt = tp.get_text_bounded(right.value, bottom.value - 8, right.value + 300, top.value + 8).strip()
                txt = ' '.join(txt.split())
                swatches.append((i, f_hex, (left.value, bottom.value, right.value, top.value), txt))

print(f"Found {len(swatches)} candidate swatches:")
for idx, f_hex, bbox, txt in swatches:
    print(f"Obj {idx}: Color={f_hex} BBox=({bbox[0]:.1f}, {bbox[1]:.1f}, {bbox[2]:.1f}, {bbox[3]:.1f}) -> Text: '{txt}'")
