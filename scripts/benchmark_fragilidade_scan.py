import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes
import time

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\Mapa Fragilidade Potencial.pdf"
t0 = time.time()
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]
objs = list(page.get_objects())
print(f"[{time.time()-t0:.1f}s] Read {len(objs)} objects")

r, g, b, a = ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint()
fm, st = ctypes.c_int(), ctypes.c_int()
x, y = ctypes.c_float(), ctypes.c_float()
left, bottom, right, top = ctypes.c_float(), ctypes.c_float(), ctypes.c_float(), ctypes.c_float()

target_colors = {"#006100", "#7AAB00", "#FFFF00", "#FF0000", "#A80000"}

t1 = time.time()
extracted_count = 0
for i, p in enumerate(objs):
    if type(p).__name__ == 'PdfObject':
        pdfium_c.FPDFPath_GetDrawMode(p.raw, ctypes.byref(fm), ctypes.byref(st))
        if fm.value != 0:
            pdfium_c.FPDFPageObj_GetBounds(p.raw, ctypes.byref(left), ctypes.byref(bottom), ctypes.byref(right), ctypes.byref(top))
            if left.value >= 25 and right.value <= 1675:
                pdfium_c.FPDFPageObj_GetFillColor(p.raw, ctypes.byref(r), ctypes.byref(g), ctypes.byref(b), ctypes.byref(a))
                f_hex = f"#{r.value:02X}{g.value:02X}{b.value:02X}"
                if f_hex in target_colors:
                    extracted_count += 1

print(f"[{time.time()-t1:.1f}s] Scanned and matched {extracted_count} target filled paths")
doc.close()
