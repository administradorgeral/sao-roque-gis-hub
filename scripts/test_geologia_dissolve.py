import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes
from shapely.geometry import Polygon, MultiPolygon
from shapely.validation import make_valid
import geopandas as gpd

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\75631_4_3_5_1 Geologia.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]
objs = list(page.get_objects())

slope_x = 18.439009
intercept_x = 273617.99
slope_y = 18.440501
intercept_y = 7380104.97

def pdf_to_utm(px, py):
    return (slope_x * px + intercept_x, slope_y * py + intercept_y)

r_val = ctypes.c_uint()
g_val = ctypes.c_uint()
b_val = ctypes.c_uint()
a_val = ctypes.c_uint()
x_val = ctypes.c_float()
y_val = ctypes.c_float()

units_meta = {
    "#FF7F7F": {"codigo": "GEOL_GRANITO_SAO_ROQUE", "nome": "Granito São Roque"},
    "#E600A9": {"codigo": "GEOL_GRANITO_IBIUNA", "nome": "Granito Ibiúna"},
    "#FF5500": {"codigo": "GEOL_GRANITO_ITAPEVI", "nome": "Granito Itapevi"},
    "#CDAA66": {"codigo": "GEOL_SR_ESTRADA_ROMEIROS", "nome": "Formação Estrada dos Romeiros"},
    "#728944": {"codigo": "GEOL_SR_PIRAGIBU", "nome": "Formação Piragibu"},
    "#897044": {"codigo": "GEOL_SERRA_ITABERABA", "nome": "Grupo Serra do Itaberaba"},
    "#D79E9E": {"codigo": "GEOL_VOTUVERAVA", "nome": "Grupo Votuverava"}
}

map_path_indices = [4, 8, 9, 10, 11, 12, 13, 14, 15]
records = []

for idx in map_path_indices:
    p = objs[idx]
    pdfium_c.FPDFPageObj_GetFillColor(p.raw, ctypes.byref(r_val), ctypes.byref(g_val), ctypes.byref(b_val), ctypes.byref(a_val))
    f_hex = f"#{r_val.value:02X}{g_val.value:02X}{b_val.value:02X}"
    meta = units_meta[f_hex]
    
    n_segs = pdfium_c.FPDFPath_CountSegments(p.raw)
    subpaths = []
    current_subpath = []
    
    for i in range(n_segs):
        seg = pdfium_c.FPDFPath_GetPathSegment(p.raw, i)
        stype = pdfium_c.FPDFPathSegment_GetType(seg)
        pdfium_c.FPDFPathSegment_GetPoint(seg, ctypes.byref(x_val), ctypes.byref(y_val))
        pt = pdf_to_utm(x_val.value, y_val.value)
        if stype == pdfium_c.FPDF_SEGMENT_MOVETO:
            if len(current_subpath) >= 3:
                subpaths.append(current_subpath)
            current_subpath = [pt]
        else:
            current_subpath.append(pt)
    if len(current_subpath) >= 3:
        subpaths.append(current_subpath)
        
    for sp in subpaths:
        if len(sp) < 3:
            continue
        if sp[0] != sp[-1]:
            sp.append(sp[0])
        poly = Polygon(sp)
        if not poly.is_valid:
            poly = make_valid(poly)
        if poly.is_empty:
            continue
        if poly.area / 10000.0 < 0.1:
            continue
        records.append({
            "codigo_classe": meta["codigo"],
            "nome_classe": meta["nome"],
            "cor_hex": f_hex,
            "geometry": poly
        })

doc.close()

gdf_raw = gpd.GeoDataFrame(records, crs="EPSG:31983")
print("Raw features:", len(gdf_raw))
for code, group in gdf_raw.groupby('codigo_classe'):
    print(f"  {code}: {len(group)} features, total area: {group.geometry.area.sum()/10000.0:.2f} ha")

gdf_dissolved = gdf_raw.dissolve(by="codigo_classe", as_index=False, aggfunc="first")
print("\nDissolved features:", len(gdf_dissolved))
for idx, r in gdf_dissolved.iterrows():
    print(f"  {r['codigo_classe']} | {r['nome_classe']} | geom_type={r.geometry.geom_type} | area={r.geometry.area/10000.0:.2f} ha")

total_area = gdf_dissolved.geometry.area.sum() / 10000.0
print(f"\nTotal municipal geological area: {total_area:.2f} ha ({total_area/100:.2f} km²)")
