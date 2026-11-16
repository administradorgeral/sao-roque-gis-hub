import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes
from shapely.geometry import LineString, MultiLineString

doc = pdfium.PdfDocument(r'js/maps_pdf/temas/Mapa_Anexo_8.3.1-1_Zoneamento_2019.pdf')
page = doc[0]
objs = list(page.get_objects())

slope_x, intercept_x = 17.637839, 271182.44
slope_y, intercept_y = 17.638906, 7381568.28

def pdf_to_utm(px, py):
    return (slope_x * px + intercept_x, slope_y * py + intercept_y)

x, y = ctypes.c_float(), ctypes.c_float()
p = objs[32]
n_segs = pdfium_c.FPDFPath_CountSegments(p.raw)

lines = []
current_line = []
for s in range(n_segs):
    seg = pdfium_c.FPDFPath_GetPathSegment(p.raw, s)
    stype = pdfium_c.FPDFPathSegment_GetType(seg)
    pdfium_c.FPDFPathSegment_GetPoint(seg, ctypes.byref(x), ctypes.byref(y))
    pt = pdf_to_utm(x.value, y.value)
    if stype == pdfium_c.FPDF_SEGMENT_MOVETO:
        if len(current_line) >= 2:
            lines.append(current_line)
        current_line = [pt]
    else:
        current_line.append(pt)
if len(current_line) >= 2:
    lines.append(current_line)

print(f"Object #32 produced {len(lines)} lines:")
total_len_km = 0.0
for i, line in enumerate(lines):
    ls = LineString(line)
    total_len_km += ls.length / 1000.0
    print(f"  Line #{i}: {len(line)} vertices, length={ls.length/1000.0:.2f} km, start={line[0]}, end={line[-1]}")

print(f"Total line length: {total_len_km:.2f} km")
