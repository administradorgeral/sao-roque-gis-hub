import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes
import numpy as np

doc = pdfium.PdfDocument(r'C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\75631_4_3_5_1 Geologia.pdf')
page = doc[0]
objs = list(page.get_objects())

r_val, g_val, b_val, a_val = ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint()
fm, st = ctypes.c_int(), ctypes.c_int()
x_val, y_val = ctypes.c_float(), ctypes.c_float()

grid_lines = []
for i, p in enumerate(objs):
    if type(p).__name__ == 'PdfObject':
        pdfium_c.FPDFPath_GetDrawMode(p.raw, ctypes.byref(fm), ctypes.byref(st))
        if st.value == 1 and fm.value == 0:
            pdfium_c.FPDFPageObj_GetStrokeColor(p.raw, ctypes.byref(r_val), ctypes.byref(g_val), ctypes.byref(b_val), ctypes.byref(a_val))
            # Grid lines are usually gray #6E6E6E (110, 110, 110)
            if (r_val.value, g_val.value, b_val.value) == (110, 110, 110):
                n_segs = pdfium_c.FPDFPath_CountSegments(p.raw)
                if n_segs == 2:
                    seg0 = pdfium_c.FPDFPath_GetPathSegment(p.raw, 0)
                    seg1 = pdfium_c.FPDFPath_GetPathSegment(p.raw, 1)
                    pdfium_c.FPDFPathSegment_GetPoint(seg0, ctypes.byref(x_val), ctypes.byref(y_val))
                    p0 = (x_val.value, y_val.value)
                    pdfium_c.FPDFPathSegment_GetPoint(seg1, ctypes.byref(x_val), ctypes.byref(y_val))
                    p1 = (x_val.value, y_val.value)
                    grid_lines.append((i, p0, p1))

print(f"Total #6E6E6E 2-segment grid lines: {len(grid_lines)}")
vert_lines = []
horiz_lines = []
for idx, (x0, y0), (x1, y1) in grid_lines:
    if abs(x0 - x1) < 0.01:
        vert_lines.append((round(x0, 3), round(min(y0, y1), 3), round(max(y0, y1), 3)))
    elif abs(y0 - y1) < 0.01:
        horiz_lines.append((round(y0, 3), round(min(x0, x1), 3), round(max(x0, x1), 3)))

print("Vertical grid lines (X):", sorted(list(set(x for x, _, _ in vert_lines))))
print("Horizontal grid lines (Y):", sorted(list(set(y for y, _, _ in horiz_lines))))
