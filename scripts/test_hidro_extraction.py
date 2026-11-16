import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes
import numpy as np
from shapely.geometry import LineString, Polygon, MultiPolygon
from shapely import make_valid
import geopandas as gpd
import time

print("=== TESTANDO EXTRAÇÃO DE VETORES NATIVOS DA HIDROGRAFIA ===")
t0 = time.time()

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\Hidro .pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]

objs = list(page.get_objects())
path_objs = [obj for obj in objs if obj.type == 2]

# Parâmetros de calibração afim calibrados por regressão linear:
# UTM_X = 17.636222 * PDF_X + 269492.23
# UTM_Y = 17.639066 * PDF_Y + 7381376.13
slope_x = 17.636222
intercept_x = 269492.23
slope_y = 17.639066
intercept_y = 7381376.13

def pdf_to_utm(px, py):
    return (slope_x * px + intercept_x, slope_y * py + intercept_y)

lines_records = []
polys_records = []

r_val = ctypes.c_uint()
g_val = ctypes.c_uint()
b_val = ctypes.c_uint()
a_val = ctypes.c_uint()
x_val = ctypes.c_float()
y_val = ctypes.c_float()

for idx, p in enumerate(path_objs):
    s_col, f_col = None, None
    if pdfium_c.FPDFPageObj_GetStrokeColor(p.raw, ctypes.byref(r_val), ctypes.byref(g_val), ctypes.byref(b_val), ctypes.byref(a_val)):
        s_col = (r_val.value, g_val.value, b_val.value)
    if pdfium_c.FPDFPageObj_GetFillColor(p.raw, ctypes.byref(r_val), ctypes.byref(g_val), ctypes.byref(b_val), ctypes.byref(a_val)):
        f_col = (r_val.value, g_val.value, b_val.value)
        
    s_hex = f"#{s_col[0]:02X}{s_col[1]:02X}{s_col[2]:02X}" if s_col else "NONE"
    f_hex = f"#{f_col[0]:02X}{f_col[1]:02X}{f_col[2]:02X}" if f_col else "NONE"
    
    b = p.get_bounds()
    # Ignorar legenda e carimbo (X > 1680)
    if b[0] > 1680:
        continue
    # Ignorar moldura externa
    if (b[2] - b[0]) > 1600 and (b[3] - b[1]) > 1550:
        continue
        
    n_segs = pdfium_c.FPDFPath_CountSegments(p.raw)
    if n_segs < 2:
        continue
        
    pts = []
    is_closed = False
    for i in range(n_segs):
        seg = pdfium_c.FPDFPath_GetPathSegment(p.raw, i)
        pdfium_c.FPDFPathSegment_GetPoint(seg, ctypes.byref(x_val), ctypes.byref(y_val))
        c = pdfium_c.FPDFPathSegment_GetClose(seg)
        if c == 1:
            is_closed = True
        pts.append(pdf_to_utm(x_val.value, y_val.value))
        
    if len(pts) < 2:
        continue
        
    # Verificar se é Corpo d'Água Poligonal (Represa / Lago / Açude)
    if f_hex == "#97DBF2":
        if pts[0] != pts[-1]:
            pts.append(pts[0])
        if len(pts) >= 4:
            try:
                poly = Polygon(pts)
                if not poly.is_valid:
                    poly = make_valid(poly)
                if poly.area >= 50.0: # >= 50 m²
                    polys_records.append({
                        "tipo": "Represa / Corpo d'Água",
                        "categoria": "Massa d'Água Poligonal",
                        "area_m2": round(poly.area, 1),
                        "area_ha": round(poly.area / 10000.0, 3),
                        "cor_hex": "#00A2E8",
                        "stroke_hex": s_hex,
                        "fill_hex": f_hex,
                        "base_legal": "Lei Federal nº 12.651/2012 Art. 4º, II e Lei nº 6.766/1979",
                        "restricao": "Impeditiva / Faixa de APP de Reservatório",
                        "alerta": "🌊 APP DE CORPO D'ÁGUA: Proibida a ocupação, parcelamento ou edificação no entorno de lagos e reservatórios artificiais/naturais.",
                        "geometry": poly
                    })
            except Exception:
                pass
    # Caso contrário, se for linha de drenagem (azul #0A93FC ou #4065EB)
    elif s_hex in ("#0A93FC", "#4065EB"):
        try:
            line = LineString(pts)
            if line.length >= 10.0: # >= 10 metros
                subtipo = "Rio Principal / Calha de Drenagem" if s_hex == "#4065EB" else "Córrego / Afluente / Drenagem Secundária"
                largura_presumida = "5 a 10 metros" if s_hex == "#4065EB" else "Até 10 metros"
                faixa_app = "30 a 50 metros" if s_hex == "#4065EB" else "30 metros"
                lines_records.append({
                    "tipo": subtipo,
                    "categoria": "Curso d'Água Linear",
                    "extensao_m": round(line.length, 1),
                    "largura_estimada": largura_presumida,
                    "faixa_app_legal": faixa_app,
                    "cor_hex": s_hex,
                    "stroke_hex": s_hex,
                    "base_legal": "Lei Federal nº 12.651/2012 Art. 4º, I e Lei nº 6.766/1979 Art. 3º",
                    "restricao": "Impeditiva / Faixa Marginal de APP Hídrica",
                    "alerta": f"💧 APP HÍDRICA (Faixa de {faixa_app}): Faixa marginal de preservação permanente inalienável e non aedificandi de ambos os lados da calha.",
                    "geometry": line
                })
        except Exception:
            pass

doc.close()

print(f"[{time.time()-t0:.1f}s] Linhas de drenagem extraídas: {len(lines_records)}")
print(f"[{time.time()-t0:.1f}s] Corpos d'água poligonais extraídos: {len(polys_records)}")

gdf_lines = gpd.GeoDataFrame(lines_records, crs="EPSG:31983")
gdf_polys = gpd.GeoDataFrame(polys_records, crs="EPSG:31983")

print("\n--- RESUMO DAS LINHAS DE DRENAGEM ---")
print(f"Extensão total da rede de drenagem: {gdf_lines['extensao_m'].sum() / 1000.0:.2f} km!")
print(f"Subtipos:\n{gdf_lines['tipo'].value_counts()}")

print("\n--- RESUMO DOS CORPOS D'ÁGUA ---")
print(f"Área total de espelhos d'água: {gdf_polys['area_ha'].sum():.2f} hectares ({gdf_polys['area_ha'].sum()/100:.2f} km²)")
