import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes

doc = pdfium.PdfDocument(r'C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\75631_4_3_5_1 Geologia.pdf')
page = doc[0]
objs = list(page.get_objects())

x_val, y_val = ctypes.c_float(), ctypes.c_float()

map_path_indices = [4, 8, 9, 10, 11, 12, 13, 14, 15]

for idx in map_path_indices:
    p = objs[idx]
    n_segs = pdfium_c.FPDFPath_CountSegments(p.raw)
    moveto_indices = []
    close_indices = []
    for i in range(n_segs):
        seg = pdfium_c.FPDFPath_GetPathSegment(p.raw, i)
        stype = pdfium_c.FPDFPathSegment_GetType(seg)
        is_close = pdfium_c.FPDFPathSegment_GetClose(seg)
        if stype == pdfium_c.FPDF_SEGMENT_MOVETO:
            moveto_indices.append(i)
        if is_close:
            close_indices.append(i)
    print(f"Path {idx:2d}: {n_segs:5d} segs | MOVETO at {moveto_indices} | CLOSE at {len(close_indices)} segs")
