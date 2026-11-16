import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes
import time
import json
import os
import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union
from shapely.validation import make_valid

print("=== EXPORTAÇÃO OFICIAL DA CAMADA DE ÁREAS HIDROLOGICAMENTE SENSÍVEIS (AHS) ===")
t0 = time.time()

pdf_path = "C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/js/maps_pdf/temas/34229_4.2.5.1-1 AHS.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]
objs = list(page.get_objects())

slope_x, intercept_x = 12.346837, 269458.60
slope_y, intercept_y = 12.345527, 7380944.43

def pt_to_utm(px, py):
    return (slope_x * px + intercept_x, slope_y * py + intercept_y)

r, g, b, a = ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint()
fm, st = ctypes.c_int(), ctypes.c_int()
left, bottom, right, top = ctypes.c_float(), ctypes.c_float(), ctypes.c_float(), ctypes.c_float()
point_x, point_y = ctypes.c_float(), ctypes.c_float()

polygons = []
legend_swatches = []

for idx, p in enumerate(objs):
    if type(p).__name__ == 'PdfObject':
        pdfium_c.FPDFPath_GetDrawMode(p.raw, ctypes.byref(fm), ctypes.byref(st))
        if fm.value != 0:
            pdfium_c.FPDFPageObj_GetFillColor(p.raw, ctypes.byref(r), ctypes.byref(g), ctypes.byref(b), ctypes.byref(a))
            f_hex = f"#{r.value:02X}{g.value:02X}{b.value:02X}"
            if f_hex == "#A80084":
                pdfium_c.FPDFPageObj_GetBounds(p.raw, ctypes.byref(left), ctypes.byref(bottom), ctypes.byref(right), ctypes.byref(top))
                # Excluir a amostra da legenda (x > 2650)
                if left.value > 2650:
                    legend_swatches.append(idx)
                    continue
                
                n_segs = pdfium_c.FPDFPath_CountSegments(p.raw)
                subpaths = []
                cur_sp = []
                for s_i in range(n_segs):
                    seg = pdfium_c.FPDFPath_GetPathSegment(p.raw, s_i)
                    pdfium_c.FPDFPathSegment_GetPoint(seg, ctypes.byref(point_x), ctypes.byref(point_y))
                    s_type = pdfium_c.FPDFPathSegment_GetType(seg)
                    is_close = pdfium_c.FPDFPathSegment_GetClose(seg)
                    
                    ux, uy = pt_to_utm(point_x.value, point_y.value)
                    cur_sp.append((ux, uy))
                    
                    if is_close or s_type == 1:
                        if len(cur_sp) >= 3:
                            subpaths.append(cur_sp)
                        cur_sp = []
                
                if cur_sp and len(cur_sp) >= 3:
                    subpaths.append(cur_sp)
                
                if subpaths:
                    try:
                        if len(subpaths) == 1:
                            poly = Polygon(subpaths[0])
                        else:
                            poly = Polygon(subpaths[0], subpaths[1:])
                        if not poly.is_valid:
                            poly = make_valid(poly)
                        if not poly.is_empty:
                            polygons.append(poly)
                    except Exception as e:
                        pass

print(f"1. Polígonos nativos extraídos: {len(polygons)}")

# Dissolver todas as peças de AHS
print("2. Executando unary_union para dissolver emendas e sobreposições de mosaico...")
dissolved_raw = unary_union(polygons)

# Carregar o contorno municipal oficial para clip rigoroso
gdf_mun = gpd.read_file("C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/data/territorio_municipal_sao_roque.gpkg")
mun_poly = gdf_mun.geometry.iloc[0]
mun_ha = round(mun_poly.area / 10000.0, 2)

print("3. Executando intersecção espacial estrita com o Território Municipal de São Roque...")
dissolved_ahs = dissolved_raw.intersection(mun_poly)
if not dissolved_ahs.is_valid:
    dissolved_ahs = make_valid(dissolved_ahs)

area_m2 = dissolved_ahs.area
area_ha = round(area_m2 / 10000.0, 2)
area_km2 = round(area_ha / 100.0, 2)
pct_mun = round((area_ha / mun_ha) * 100, 2)

print(f"Área Total Oficial de AHS em São Roque: {area_ha} ha ({area_km2} km²)")
print(f"Porcentagem do Município ({mun_ha} ha): {pct_mun}% de AHS")

# Propriedades da camada AHS
properties = {
    "codigo_classe": "AHS_SAO_ROQUE",
    "codigo": "AHS",
    "nome": "Áreas Hidrologicamente Sensíveis (AHS)",
    "classe": "Áreas Hidrologicamente Sensíveis",
    "denominacao": "Áreas Hidrologicamente Sensíveis do Município de São Roque",
    "documento_origem": "Plano Diretor Ambiental de São Roque (PDA 2019) - Anexo 4.2.5.1-1",
    "escala_nominal": "1:35.000",
    "esfera": "Municipal / Estadual / Federal",
    "orgao_gestor": "Prefeitura da Estância Turística de São Roque / DAEE / CETESB / Fundação Florestal",
    "base_legal": "Código Florestal (Lei Federal nº 12.651/2012 Arts. 4º e 6º), Lei Estadual nº 9.866/1997, Lei Estadual nº 11.579/2003, LC Municipal nº 39/2006 (Arts. 60-64) e LC nº 40/2006",
    "responsavel_tecnico": "Maurício Scorsatto Sartori (CREA 5.060.532.187) / Ana Clara Cerminaro (CREA 473.423.455)",
    "fonte_cartografica": "IGC 1:10.000 (1978), Código Florestal (Lei 12.651/12), Ortoimagem SPOT 1,5m (15/02/2016) e Hidrografia Corrigida em Campo",
    "area_ha": area_ha,
    "area_km2": area_km2,
    "porcentagem_municipio": pct_mun,
    "cor_hex": "#A80084",
    "cor_borda": "#700058",
    "implicacao_juridica": "Áreas de Preservação Permanente (APPs) de nascentes (raio 50m), faixas marginais de cursos d'água (30m a 100m), várzeas inundáveis, planícies de meandro e zonas de recarga hídrica. É vedada qualquer edificação, terraplenagem, aterro ou impermeabilização do solo, sendo obrigatória a manutenção e restauração da vegetação nativa ciliar protetora dos recursos hídricos."
}

# Separar geometrias para o GeoDataFrame
if dissolved_ahs.geom_type == 'MultiPolygon':
    geoms = list(dissolved_ahs.geoms)
else:
    geoms = [dissolved_ahs]

gdf_ahs_utm = gpd.GeoDataFrame([properties] * len(geoms), geometry=geoms, crs="EPSG:31983")

# Salvar GeoPackage
gpkg_path = "C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/data/ahs_sao_roque.gpkg"
gdf_ahs_utm.to_file(gpkg_path, driver="GPKG")
print(f"4. Salvo GPKG em: {gpkg_path}")

# Salvar GeoJSON Web Otimizado
gdf_ahs_wgs84 = gdf_ahs_utm.to_crs(epsg=4326)
geojson_path = "C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/data/ahs_sao_roque_web.geojson"

geojson_dict = json.loads(gdf_ahs_wgs84.to_json())
def round_coords(geom):
    if geom['type'] == 'Polygon':
        geom['coordinates'] = [[[round(coord[0], 5), round(coord[1], 5)] for coord in ring] for ring in geom['coordinates']]
    elif geom['type'] == 'MultiPolygon':
        geom['coordinates'] = [[[[round(coord[0], 5), round(coord[1], 5)] for coord in ring] for ring in poly] for poly in geom['coordinates']]

for f in geojson_dict['features']:
    round_coords(f['geometry'])

with open(geojson_path, "w", encoding="utf-8") as f:
    json.dump(geojson_dict, f, ensure_ascii=False, indent=2)

print(f"5. Salvo GeoJSON Web em: {geojson_path} ({os.path.getsize(geojson_path)/1024:.1f} KB)")
print(f"=== CONCLUÍDO COM SUCESSO EM {time.time()-t0:.2f}s ===")
