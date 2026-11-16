import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes
import time
import json
import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union
from shapely.validation import make_valid

print("=== EXPORTAÇÃO DA CAMADA DE VEGETAÇÃO NATIVA ARBÓREA (PDA 2019) ===")
t0 = time.time()

pdf_path = "C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/js/maps_pdf/temas/34218_5_3_2_1_1 Vegetação Nativa arbórea.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]
objs = list(page.get_objects())

slope_x, intercept_x = 12.345755, 269928.85
slope_y, intercept_y = 12.345527, 7380932.58

def pt_to_utm(px, py):
    return (slope_x * px + intercept_x, slope_y * py + intercept_y)

r, g, b, a = ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint()
fm, st = ctypes.c_int(), ctypes.c_int()
left, bottom, right, top = ctypes.c_float(), ctypes.c_float(), ctypes.c_float(), ctypes.c_float()
point_x, point_y = ctypes.c_float(), ctypes.c_float()

polygons_avancado = []
polygons_inicial = []

for idx, p in enumerate(objs):
    if type(p).__name__ == 'PdfObject':
        pdfium_c.FPDFPath_GetDrawMode(p.raw, ctypes.byref(fm), ctypes.byref(st))
        if fm.value != 0:
            pdfium_c.FPDFPageObj_GetFillColor(p.raw, ctypes.byref(r), ctypes.byref(g), ctypes.byref(b), ctypes.byref(a))
            f_hex = f"#{r.value:02X}{g.value:02X}{b.value:02X}"
            
            if f_hex in ["#267300", "#55FF00"]:
                pdfium_c.FPDFPageObj_GetBounds(p.raw, ctypes.byref(left), ctypes.byref(bottom), ctypes.byref(right), ctypes.byref(top))
                # Excluir a legenda (x > 2650)
                if left.value > 2650:
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
                        poly = Polygon(subpaths[0], holes=subpaths[1:] if len(subpaths) > 1 else None)
                        if not poly.is_valid:
                            poly = make_valid(poly)
                        if not poly.is_empty:
                            if f_hex == "#267300":
                                polygons_avancado.append(poly)
                            else:
                                polygons_inicial.append(poly)
                    except Exception:
                        pass

print(f"Polígonos extraídos em {time.time()-t0:.2f}s:")
print(f"  Estágio Avançado/Médio (#267300): {len(polygons_avancado)}")
print(f"  Estágio Inicial (#55FF00): {len(polygons_inicial)}")

# Dissolver
t1 = time.time()
print("Dissolvendo geometrias...")
union_avancado = unary_union(polygons_avancado)
union_inicial = unary_union(polygons_inicial)
print(f"Dissolve concluído em {time.time()-t1:.2f}s.")

# Carregar limite municipal
mun_gdf = gpd.read_file("C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/data/territorio_municipal_sao_roque.gpkg")
mun_poly = mun_gdf.geometry.iloc[0]
mun_area_ha = mun_poly.area / 10000.0

clip_avancado = union_avancado.intersection(mun_poly)
clip_inicial = union_inicial.intersection(mun_poly)

area_av = round(clip_avancado.area / 10000.0, 2)
area_in = round(clip_inicial.area / 10000.0, 2)
pct_av = round((area_av / mun_area_ha) * 100.0, 2)
pct_in = round((area_in / mun_area_ha) * 100.0, 2)

features_data = [
    {
        "codigo_classe": "VN_AVANCADO_MEDIO",
        "codigo": "VN_AV_MED",
        "nome": "Vegetação Nativa Arbórea em Estágio Avançado e Médio",
        "classe": "Estágio Avançado e Médio",
        "denominacao": "Vegetação Nativa Arbórea em Estágio Avançado e Médio (Mata Atlântica)",
        "documento_origem": "Plano Diretor Ambiental de São Roque (PDA 2019) - Anexo 5.3.2.1-1",
        "escala_nominal": "1:35.000",
        "esfera": "Federal / Estadual / Municipal",
        "orgao_gestor": "Prefeitura Municipal de São Roque / CETESB / Fundação Florestal / IBAMA",
        "base_legal": "Lei da Mata Atlântica (Lei Federal nº 11.428/2006 Arts. 11, 14, 21), Decreto Federal nº 6.660/2008, Código Florestal (Lei nº 12.651/2012) e LC Municipal nº 39/2006 (Arts. 60-64)",
        "responsavel_tecnico": "Maurício Scorsatto Sartori (CREA 5.060.532.187) / Ana Clara Cerminaro (CREA 473.423.455)",
        "fonte_cartografica": "IGC 1:10.000 (1978), Código Florestal (Lei 12.651/12), Ortoimagem SPOT 1,5m (15/02/2016) e Verificação de Campo",
        "area_ha": area_av,
        "area_km2": round(area_av / 100.0, 2),
        "porcentagem_municipio": pct_av,
        "cor_hex": "#267300",
        "cor_borda": "#1A4D00",
        "implicacao_juridica": "Proteção rigorosa contra corte, supressão e parcelamento predatório. Supressão de vegetação primária ou em estágio avançado é terminantemente vedada, ressalvadas obras de utilidade pública com compensação ambiental gravada e autorização expressa da CETESB (Lei Federal 11.428/06 e Dec. 6.660/08).",
        "geometry": clip_avancado
    },
    {
        "codigo_classe": "VN_INICIAL",
        "codigo": "VN_INI",
        "nome": "Vegetação Nativa Arbórea em Estágio Inicial",
        "classe": "Estágio Inicial",
        "denominacao": "Vegetação Nativa Arbórea em Estágio Inicial de Regeneração (Capoeira / Mata Secundária)",
        "documento_origem": "Plano Diretor Ambiental de São Roque (PDA 2019) - Anexo 5.3.2.1-1",
        "escala_nominal": "1:35.000",
        "esfera": "Federal / Estadual / Municipal",
        "orgao_gestor": "Prefeitura Municipal de São Roque / CETESB / Fundação Florestal",
        "base_legal": "Lei da Mata Atlântica (Lei Federal nº 11.428/2006 Art. 25), Decreto Federal nº 6.660/2008 e LC Municipal nº 39/2006",
        "responsavel_tecnico": "Maurício Scorsatto Sartori (CREA 5.060.532.187) / Ana Clara Cerminaro (CREA 473.423.455)",
        "fonte_cartografica": "IGC 1:10.000 (1978), Código Florestal (Lei 12.651/12), Ortoimagem SPOT 1,5m (15/02/2016)",
        "area_ha": area_in,
        "area_km2": round(area_in / 100.0, 2),
        "porcentagem_municipio": pct_in,
        "cor_hex": "#55FF00",
        "cor_borda": "#3BB300",
        "implicacao_juridica": "Vegetação em estágio inicial de regeneração natural. Qualquer intervenção requer autorização prévia da CETESB e atendimento às diretrizes de compensação e manutenção da conectividade de fragmentos florestais.",
        "geometry": clip_inicial
    }
]

gdf_utm = gpd.GeoDataFrame(features_data, crs="EPSG:31983")

# Salvar GPKG
gpkg_path = "C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/data/vegetacao_arborea_sao_roque.gpkg"
gdf_utm.to_file(gpkg_path, driver="GPKG")
print(f"GPKG salvo: {gpkg_path}")

# Simplificar para WebGIS (tolerância de 2.0 metros)
print("Simplificando geometrias para GeoJSON Web...")
gdf_utm_simp = gdf_utm.copy()
gdf_utm_simp['geometry'] = gdf_utm_simp['geometry'].simplify(tolerance=2.0, preserve_topology=True)

gdf_wgs = gdf_utm_simp.to_crs(epsg=4326)
geojson_path = "C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/data/vegetacao_arborea_sao_roque_web.geojson"
gdf_wgs.to_file(geojson_path, driver="GeoJSON")
print(f"GeoJSON Web salvo: {geojson_path}")

# Verificar tamanho do arquivo
import os
sz_mb = os.path.getsize(geojson_path) / (1024 * 1024)
print(f"Tamanho do GeoJSON otimizado: {sz_mb:.2f} MB")
print("=== EXPORTAÇÃO CONCLUÍDA COM SUCESSO! ===")
