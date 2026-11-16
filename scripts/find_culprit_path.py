import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes
from shapely.geometry import Point, Polygon
import geopandas as gpd

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\Hidro .pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]

objs = list(page.get_objects())
path_objs = [obj for obj in objs if obj.type == 2]

slope_x = 17.636163
intercept_x = 269256.56
slope_y = 17.638983
intercept_y = 7381376.20

def pdf_to_utm(px, py):
    return (slope_x * px + intercept_x, slope_y * py + intercept_y)

r_val = ctypes.c_uint()
g_val = ctypes.c_uint()
b_val = ctypes.c_uint()
a_val = ctypes.c_uint()
x_val = ctypes.c_float()
y_val = ctypes.c_float()

# O ponto problemático em UTM: (281178, 7403132)
pt_utm = Point(281178.0, 7403132.0)

print("Procurando qual path original do PDF gerou esse polígono gigante...")

for idx, p in enumerate(path_objs):
    pdfium_c.FPDFPageObj_GetFillColor(p.raw, ctypes.byref(r_val), ctypes.byref(g_val), ctypes.byref(b_val), ctypes.byref(a_val))
    f_hex = f"#{r_val.value:02X}{g_val.value:02X}{b_val.value:02X}"
    
    if f_hex == "#97DBF2":
        n_segs = pdfium_c.FPDFPath_CountSegments(p.raw)
        pts = []
        for i in range(n_segs):
            seg = pdfium_c.FPDFPath_GetPathSegment(p.raw, i)
            pdfium_c.FPDFPathSegment_GetPoint(seg, ctypes.byref(x_val), ctypes.byref(y_val))
            pts.append(pdf_to_utm(x_val.value, y_val.value))
            
        if len(pts) >= 4:
            try:
                poly = Polygon(pts)
                if poly.contains(pt_utm):
                    print(f"\nACHADO! Path {idx}:")
                    print(f"  Número de segmentos: {n_segs}")
                    print(f"  Bounds PDF: {p.get_bounds()}")
                    print(f"  Área UTM: {poly.area / 10000.0:.2f} ha ({poly.area:,.0f} m²)")
                    pdfium_c.FPDFPageObj_GetStrokeColor(p.raw, ctypes.byref(r_val), ctypes.byref(g_val), ctypes.byref(b_val), ctypes.byref(a_val))
                    s_hex = f"#{r_val.value:02X}{g_val.value:02X}{b_val.value:02X}"
                    print(f"  Stroke: {s_hex}, Fill: {f_hex}")
                    
                    # Inspecionar os primeiros 10 pontos e tipos de segmento:
                    print("  Primeiros 10 segmentos:")
                    for s_i in range(min(15, n_segs)):
                        seg = pdfium_c.FPDFPath_GetPathSegment(p.raw, s_i)
                        pdfium_c.FPDFPathSegment_GetPoint(seg, ctypes.byref(x_val), ctypes.byref(y_val))
                        t = pdfium_c.FPDFPathSegment_GetType(seg)
                        c = pdfium_c.FPDFPathSegment_GetClose(seg)
                        print(f"    Seg {s_i}: X={x_val.value:.2f}, Y={y_val.value:.2f}, type={t}, close={c}")
            except Exception as e:
                pass

doc.close()
