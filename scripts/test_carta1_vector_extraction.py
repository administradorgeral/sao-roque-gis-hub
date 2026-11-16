import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes
import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union
from shapely.validation import make_valid
import time

print("=== TESTE DE EXTRAÇÃO VETORIAL DAS MACROZONAS DA CARTA I ===")
t0 = time.time()

doc = pdfium.PdfDocument(r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\minuta_pd2026\desmembrado\02_cartas_tecnicas\carta_01_macrozoneamento_municipal.pdf")
page = doc[0]

r, g, b, a = ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint()
fm, st = ctypes.c_int(), ctypes.c_int()
point_x, point_y = ctypes.c_float(), ctypes.c_float()
mat = pdfium.raw.FS_MATRIX()

objs = list(page.get_objects())
print(f"Total de objetos na página: {len(objs)}")

# We will collect polygons by color:
# 1. Vermelho: Consolidação Urbana (255, 0, 0)
# 2. Laranja: Urbanização Específica (255, 127, 0)
# 3. Verde: Ambiental / Preservação (0, 255, 0)
# 4. Rosa/Salmão: Rural (247, 171, 174)

polys_by_color = {
    "CONSOLIDACAO_URBANA": [],
    "URBANIZACAO_ESPECIFICA": [],
    "AMBIENTAL_PRESERVACAO": [],
    "RURAL": []
}

color_map = {
    (255, 0, 0): "CONSOLIDACAO_URBANA",
    (255, 127, 0): "URBANIZACAO_ESPECIFICA",
    (0, 255, 0): "AMBIENTAL_PRESERVACAO",
    (247, 171, 174): "RURAL"
}

for idx, p in enumerate(objs):
    if p.type == pdfium.raw.FPDF_PAGEOBJ_PATH:
        pdfium_c.FPDFPath_GetDrawMode(p.raw, ctypes.byref(fm), ctypes.byref(st))
        if fm.value != 0:
            pdfium_c.FPDFPageObj_GetFillColor(p.raw, ctypes.byref(r), ctypes.byref(g), ctypes.byref(b), ctypes.byref(a))
            c = (r.value, g.value, b.value)
            
            zone_key = color_map.get(c)
            if not zone_key:
                continue
                
            pdfium_c.FPDFPageObj_GetMatrix(p.raw, ctypes.byref(mat))
            n_segs = pdfium_c.FPDFPath_CountSegments(p.raw)
            if n_segs < 3:
                continue
                
            pts = []
            for s_i in range(n_segs):
                seg = pdfium_c.FPDFPath_GetPathSegment(p.raw, s_i)
                pdfium_c.FPDFPathSegment_GetPoint(seg, ctypes.byref(point_x), ctypes.byref(point_y))
                # Apply matrix
                px = mat.a * point_x.value + mat.c * point_y.value + mat.e
                py = mat.b * point_x.value + mat.d * point_y.value + mat.f
                pts.append((px, py))
                
            if len(pts) >= 3:
                try:
                    poly = Polygon(pts)
                    if poly.is_valid and poly.area > 0.1:
                        polys_by_color[zone_key].append(poly)
                except Exception:
                    pass

for z, p_list in polys_by_color.items():
    print(f"Zona {z}: {len(p_list)} polígonos brutos encontrados.")

# Test dissolving one zone (e.g., CONSOLIDACAO_URBANA - only 163 polys)
print("\nDissolvendo CONSOLIDACAO_URBANA...")
cu_union = unary_union(polys_by_color["CONSOLIDACAO_URBANA"])
cu_union = cu_union.buffer(0.1).buffer(-0.1)
print(f"CONSOLIDACAO_URBANA dissolvida: type={cu_union.geom_type}, area={cu_union.area:.1f} pt²")

print(f"Tempo total: {time.time() - t0:.2f}s")
