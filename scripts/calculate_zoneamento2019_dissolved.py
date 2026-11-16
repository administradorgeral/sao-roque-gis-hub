import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes
from shapely.geometry import Polygon, MultiPolygon
from shapely.validation import make_valid
from shapely.ops import unary_union

doc = pdfium.PdfDocument(r'js/maps_pdf/temas/Mapa_Anexo_8.3.1-1_Zoneamento_2019.pdf')
page = doc[0]
objs = list(page.get_objects())

slope_x, intercept_x = 17.637839, 271182.44
slope_y, intercept_y = 17.638906, 7381568.28

def pdf_to_utm(px, py):
    return (slope_x * px + intercept_x, slope_y * py + intercept_y)

r, g, b, a = ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint()
fm, st = ctypes.c_int(), ctypes.c_int()
x, y = ctypes.c_float(), ctypes.c_float()

zones_map = {
    '#CA7AF5': ('ZDES_CB', 'Subzona de Desenvolvimento Socioeconômico - Castelo Branco', 'Zona Prioritária de Desenvolvimento'),
    '#E8BEFF': ('ZDES_SA', 'Subzona de Desenvolvimento Socioambiental', 'Zona Prioritária de Desenvolvimento'),
    '#4CE600': ('ZPBIO', 'Zona Prioritária de Proteção à Biodiversidade', 'Proteção Integral e Biodiversidade'),
    '#FFAA00': ('ZPED_ERO', 'Subzona Especial para Controle de Processos Erosivos', 'Zona Prioritária de Recursos Edáficos'),
    '#FFFF00': ('ZPED_ESCO', 'Subzona Especial de Controle Escoamento Superficial Águas Pluviais', 'Zona Prioritária de Recursos Edáficos'),
    '#FF7F7F': ('ZPURB', 'Zona Prioritária de Gestão aos Processos de Urbanização', 'Gestão aos Processos de Urbanização'),
    '#004DA8': ('ZPHID_SEN', 'Subzona de Áreas Hidrologicamente Sensíveis', 'Zona Prioritária de Recursos Hídricos'),
    '#00C5FF': ('ZPHID_RUR', 'Subzona de Manancial em Áreas Rurais', 'Zona Prioritária de Recursos Hídricos'),
    '#73DFFF': ('ZPHID_INT', 'Subzona de Manancial em Usos Intensivos ou Urbanizados', 'Zona Prioritária de Recursos Hídricos')
}

# Collect objects for each zone
zone_polys = {k: [] for k in zones_map}

for idx in range(0, 29):
    p = objs[idx]
    pdfium_c.FPDFPageObj_GetFillColor(p.raw, ctypes.byref(r), ctypes.byref(g), ctypes.byref(b), ctypes.byref(a))
    f_hex = f'#{r.value:02X}{g.value:02X}{b.value:02X}'
    
    # Skip underlay mint
    if f_hex == '#C4F5DE':
        continue
        
    if f_hex in zones_map:
        n_segs = pdfium_c.FPDFPath_CountSegments(p.raw)
        current_sp = []
        subpaths = []
        for s in range(n_segs):
            seg = pdfium_c.FPDFPath_GetPathSegment(p.raw, s)
            stype = pdfium_c.FPDFPathSegment_GetType(seg)
            pdfium_c.FPDFPathSegment_GetPoint(seg, ctypes.byref(x), ctypes.byref(y))
            pt = pdf_to_utm(x.value, y.value)
            if stype == pdfium_c.FPDF_SEGMENT_MOVETO:
                if len(current_sp) >= 3:
                    subpaths.append(current_sp)
                current_sp = [pt]
            else:
                current_sp.append(pt)
        if len(current_sp) >= 3:
            subpaths.append(current_sp)
            
        # First subpath is exterior, subsequent ones are holes
        sp0 = subpaths[0]
        if sp0[0] != sp0[-1]:
            sp0.append(sp0[0])
        holes = []
        for h in subpaths[1:]:
            if len(h) >= 3:
                if h[0] != h[-1]:
                    h.append(h[0])
                holes.append(h)
        poly = Polygon(sp0, holes)
        if not poly.is_valid:
            poly = make_valid(poly)
        if not poly.is_empty:
            zone_polys[f_hex].append(poly)

print("=== DISSOLVED ZONING 2019 (PDA) ===")
dissolved = {}
total_ha = 0.0
for f_hex, plist in zone_polys.items():
    code, name, group = zones_map[f_hex]
    u = unary_union(plist)
    if not u.is_valid:
        u = make_valid(u)
    dissolved[f_hex] = u
    area_ha = u.area / 10000.0
    total_ha += area_ha
    print(f"[{code}] {name} ({f_hex}): {len(plist)} polys -> {area_ha:.2f} ha")

print(f"\nTOTAL ZONED AREA: {total_ha:.2f} ha (PDA São Roque: 30.709,52 ha)")
for f_hex, u in dissolved.items():
    code, name, group = zones_map[f_hex]
    ha = u.area / 10000.0
    pct = (ha / total_ha) * 100
    print(f"  {code}: {ha:.2f} ha ({pct:.2f}%)")
