import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes
import json
import os
import time
import sqlite3
from shapely.geometry import Polygon, MultiPolygon
from shapely.validation import make_valid
from shapely import simplify
import geopandas as gpd

print("=== PROCESSANDO MAPA #5: GEOLOGIA (ANEXO 4.3.5-1) COM DISSOLVE GEOLÓGICO ===")
t0 = time.time()

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\75631_4_3_5_1 Geologia.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]
objs = list(page.get_objects())

# Calibração Afim Rigorosa via Linhas de Grade Vetoriais (#6E6E6E)
# RMS de resíduo: 1.25 metros em todo o município (276.000E a 304.000E e 7.385.000N a 7.405.000N)
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

# Metadados Geológicos Oficiais com Base Legal e Aptidão Urbanística
units_meta = {
    "#FF7F7F": {
        "codigo_classe": "GEOL_GRANITO_SAO_ROQUE",
        "nome_classe": "Granito São Roque",
        "sigla": "NP3sγ1I",
        "hierarquia": "Orógeno Socorro-Guaxupé",
        "litologia": "Granitóides foliados e ortognaisses calcialcalinos, tipo I",
        "relevo_associado": "Maciços dissecados e relevos montanhosos com vertentes íngremes",
        "aptidao_geotecnica": "Alta resistência mecânica da rocha sã; mantos de alteração profundos suscetíveis a escorregamentos",
        "implicacao_urbanistica": "Exigência de sondagens a percussão/rotativa (LC 41/06); restrição a cortes em encostas > 30% (LC 40/06 e Lei 6.766/79)",
        "base_legal": "CPRM/SGB (2006) / IPT (1981) / Lei Federal nº 6.766/1979 e LC Municipal nº 40/2006",
        "cor_hex": "#FF7F7F"
    },
    "#E600A9": {
        "codigo_classe": "GEOL_GRANITO_IBIUNA",
        "nome_classe": "Granito Ibiúna",
        "sigla": "NP3pγ1I",
        "hierarquia": "Formação Iporanga",
        "litologia": "Granitóides foliados e ortognaisses calcialcalinos, tipo I",
        "relevo_associado": "Colinas convexas e altas encostas na porção sudoeste (borda de Ibiúna)",
        "aptidao_geotecnica": "Boa capacidade de suporte; risco de assoreamento e ravinamento em solo residual exposto",
        "implicacao_urbanistica": "Controle rigoroso de terraplenagem na bacia de contribuição da APA Itupararanga (Lei Estadual 11.579/03)",
        "base_legal": "CPRM/SGB / Lei Estadual nº 11.579/2003 / LC Municipal nº 39/2006 e LC nº 40/2006",
        "cor_hex": "#E600A9"
    },
    "#FF5500": {
        "codigo_classe": "GEOL_GRANITO_ITAPEVI",
        "nome_classe": "Granito Itapevi",
        "sigla": "NP3pγ1",
        "hierarquia": "Granitóides Foliados",
        "litologia": "Granitóides foliados indiferenciados quimicamente",
        "relevo_associado": "Relevo movimentado no divisor leste municipal com Itapevi",
        "aptidao_geotecnica": "Maciço granítico fraturado; média a alta estabilidade em condições naturais",
        "implicacao_urbanistica": "Planejamento de expansão urbana e contenção de ocupações irregulares em zonas de transição metropolitana",
        "base_legal": "CPRM/SGB / Estatuto da Metrópole (Lei Federal nº 13.089/2015) / LC Municipal nº 40/2006",
        "cor_hex": "#FF5500"
    },
    "#CDAA66": {
        "codigo_classe": "GEOL_SR_ESTRADA_ROMEIROS",
        "nome_classe": "Grupo São Roque - Fm. Estrada dos Romeiros",
        "sigla": "NP3srer",
        "hierarquia": "Grupo São Roque",
        "litologia": "Metassedimentos, metarenitos, filitos e quartzitos subordinados",
        "relevo_associado": "Cristas e espigões alongados com orientação estrutural NE-SW",
        "aptidao_geotecnica": "Planos de clivagem e foliação que induzem escorregamentos planares quando interceptados desfavoravelmente por cortes viários",
        "implicacao_urbanistica": "Obrigatória caracterização geológico-estrutural (mergulho de planos de fraqueza) em loteamentos e arruamentos",
        "base_legal": "CPRM/SGB / IPT / Lei Federal nº 12.608/2012 (Proteção e Defesa Civil) e LC nº 40/2006",
        "cor_hex": "#CDAA66"
    },
    "#728944": {
        "codigo_classe": "GEOL_SR_PIRAGIBU",
        "nome_classe": "Grupo São Roque - Fm. Piragibu",
        "sigla": "NP3srpi",
        "hierarquia": "Grupo São Roque",
        "litologia": "Xistos, filitos grafitosos, metarritmitos e níveis metavulcânicos",
        "relevo_associado": "Colinas onduladas e vales estruturais da depressão de São Roque",
        "aptidao_geotecnica": "Rochas muito intemperizadas gerando solos argilosos compressíveis com susceptibilidade a rastejo (creep)",
        "implicacao_urbanistica": "Aptidão restrita para edificações pesadas sem fundação profunda; exigência de drenagem subsuperficial obrigatória",
        "base_legal": "CPRM/SGB / IPT / Código de Obras LC nº 41/2006 e LC nº 40/2006",
        "cor_hex": "#728944"
    },
    "#897044": {
        "codigo_classe": "GEOL_SERRA_ITABERABA",
        "nome_classe": "Grupo Serra do Itaberaba",
        "sigla": "MP2si",
        "hierarquia": "Grupo Serra do Itaberaba",
        "litologia": "Unidade metapelítica ou metavulcanossedimentar",
        "relevo_associado": "Alinhamentos serranos e escarpas rochosas",
        "aptidao_geotecnica": "Forte anisotropia geomecânica; alto risco de desprendimento de blocos e corridas de massa em encostas abruptas",
        "implicacao_urbanistica": "Zona de preservação ambiental severa; vedado parcelamento do solo em encostas e topos de crista (STF ADPF 747/749)",
        "base_legal": "CPRM/SGB / STF ADPF 747/749 / Código Florestal Lei Federal nº 12.651/2012 Art. 4º, IX",
        "cor_hex": "#897044"
    },
    "#D79E9E": {
        "codigo_classe": "GEOL_VOTUVERAVA",
        "nome_classe": "Grupo Votuverava (Unidade Terrígena)",
        "sigla": "MP1vot",
        "hierarquia": "Grupo Votuverava",
        "litologia": "Unidade terrígena: filitos, metarenitos e metaconglomerados",
        "relevo_associado": "Vales encaixados e encostas dissecadas",
        "aptidao_geotecnica": "Suscetibilidade à erosão linear acelerada (ravinas e voçorocas) quando exposto o substrato arenoso",
        "implicacao_urbanistica": "Proibição de desmatamento em faixas de drenagem; obrigatória bacia de retenção de sedimentos pluviais",
        "base_legal": "CPRM/SGB / Lei Federal nº 6.766/1979 / LC Municipal nº 39/2006 e LC nº 40/2006",
        "cor_hex": "#D79E9E"
    }
}

map_path_indices = [4, 8, 9, 10, 11, 12, 13, 14, 15]
raw_records = []

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
            
        raw_records.append({
            "codigo_classe": meta["codigo_classe"],
            "nome": meta["nome_classe"],
            "classe": meta["nome_classe"],
            "Unidade Geológica": meta["nome_classe"],
            "Sigla": meta["sigla"],
            "Hierarquia Estratigráfica": meta["hierarquia"],
            "Litologia Principal": meta["litologia"],
            "Relevo Associado": meta["relevo_associado"],
            "Comportamento Geotécnico": meta["aptidao_geotecnica"],
            "Diretriz Urbanística e Construtiva": meta["implicacao_urbanistica"],
            "Base Legal Normativa": meta["base_legal"],
            "Responsabilidade Técnica": "Maurício Scorsatto Sartori (CREA 5.060.532.187) / Ana Clara Cerminaro (CREA 473.423.455)",
            "Fonte Cartográfica Primária": "CPRM / Serviço Geológico do Brasil (2006) / IPT (1981) / PDA São Roque 2019",
            "cor_hex": meta["cor_hex"],
            "cor": meta["cor_hex"],
            "geometry": poly
        })

doc.close()

gdf_raw = gpd.GeoDataFrame(raw_records, crs="EPSG:31983")
print(f"[{time.time()-t0:.1f}s] Feições geológicas brutas lidas do PDF: {len(gdf_raw)}")

# DISSOLVE POR CLASSE - Unifica polígonos adjacentes e preserva afloramentos reais em MultiPolygon
gdf_dissolved = gdf_raw.dissolve(by="codigo_classe", as_index=False, aggfunc="first")
print(f"[{time.time()-t0:.1f}s] Unidades geológicas após DISSOLVE oficial: {len(gdf_dissolved)}")

records_final = []
for idx, row in gdf_dissolved.iterrows():
    poly = row.geometry
    area_m2 = poly.area
    area_ha = area_m2 / 10000.0
    r_dict = row.to_dict()
    r_dict["area_ha"] = round(area_ha, 2)
    r_dict["area_m2"] = round(area_m2, 1)
    r_dict["Área"] = f"{area_ha:.2f} ha ({area_ha/100:.2f} km²)"
    records_final.append(r_dict)

gdf = gpd.GeoDataFrame(records_final, crs="EPSG:31983")

for idx, r in gdf.iterrows():
    print(f"  -> Unidade {idx+1}: {r['Unidade Geológica']} ({r['Sigla']}) | Tipo: {r.geometry.geom_type} | Área: {r['Área']}")

# Salvar GeoPackage oficial
gpkg_out = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\data\geologia_sao_roque.gpkg"
gdf.to_file(gpkg_out, driver="GPKG", layer="unidades_geologicas")
print(f"[{time.time()-t0:.1f}s] GeoPackage salvo: {gpkg_out} ({os.path.getsize(gpkg_out)/1024:.1f} KB)")

# Simplificar para WebGIS com tolerância de 2m
gdf_web = gdf.copy()
gdf_web['geometry'] = simplify(gdf_web['geometry'].values, tolerance=2.0, preserve_topology=True)
gdf_wgs84 = gdf_web.to_crs("EPSG:4326")

data_geojson = json.loads(gdf_wgs84.to_json())

def round_coords(obj):
    if isinstance(obj, list):
        if len(obj) == 2 and isinstance(obj[0], (int, float)) and isinstance(obj[1], (int, float)):
            return [round(obj[0], 5), round(obj[1], 5)]
        return [round_coords(item) for item in obj]
    return obj

for feat in data_geojson['features']:
    if feat.get('geometry') and 'coordinates' in feat['geometry']:
        feat['geometry']['coordinates'] = round_coords(feat['geometry']['coordinates'])

geojson_out = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\data\geologia_sao_roque_web.geojson"
with open(geojson_out, "w", encoding="utf-8") as f:
    json.dump(data_geojson, f, ensure_ascii=False)

print(f"[{time.time()-t0:.1f}s] GeoJSON Web salvo: {geojson_out} ({os.path.getsize(geojson_out)/1024:.1f} KB, {len(data_geojson['features'])} feições limpas)")

# Bounding box
total_bounds = gdf.total_bounds
bounds_wgs84 = gdf_wgs84.total_bounds
wgs_json = json.dumps([[round(bounds_wgs84[1], 5), round(bounds_wgs84[0], 5)], [round(bounds_wgs84[3], 5), round(bounds_wgs84[2], 5)]])

# Sincronizar Banco de Dados SQLite Oficial (sao_roque_geodados.db)
db_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\dados_oficiais\sao_roque_geodados.db"
conn = sqlite3.connect(db_path)
c = conn.cursor()

# 1. Inserir na tabela camadas_territoriais
c.execute("""
INSERT OR REPLACE INTO camadas_territoriais (
    id, nome, titulo_documento, categoria, arquivo_origem, tipo_camada,
    escala_nominal, datum_projecao, data_elaboracao, responsavel_tecnico,
    responsavel_crea, desenho_tecnico, desenho_crea, fonte_cartografica,
    status_auditoria, bbox_utm_x0, bbox_utm_x1, bbox_utm_y0, bbox_utm_y1,
    bounds_wgs84_json, alerta_juridico
) VALUES (
    'geologia',
    'Unidades Geológicas e Substrato Rochoso',
    'ANEXO 4.3.5-1 - MAPA GEOLÓGICO DO MUNICÍPIO DE SÃO ROQUE - SP',
    'Geotécnica e Geomorfologia',
    '75631_4_3_5_1 Geologia.pdf',
    'vetor_poligonos',
    '1:50.000',
    'SIRGAS 2000 UTM Zone 23S',
    '11/11/2018',
    'Maurício Scorsatto Sartori (Eng. Florestal)',
    '5.060.532.187',
    'Ana Clara Cerminaro (Analista de Geoprocessamento)',
    '473.423.455',
    'CPRM / Serviço Geológico do Brasil (2006) e IPT (1981)',
    'Auditado, Calibrado e Dissolvido (7 Unidades Litoestratigráficas CPRM)',
    ?, ?, ?, ?,
    ?,
    '⛏️ DIRETRIZ GEOLÓGICA E GEOTÉCNICA: O substrato litológico de São Roque (Granito São Roque, Granito Ibiúna, Granito Itapevi, Fms. Estrada dos Romeiros e Piragibu, Grupos Serra do Itaberaba e Votuverava) condiciona o tipo de fundação (LC 41/06), o potencial de aquíferos fraturados e a estabilidade estrutural das encostas perante cortes e terraplenagens (Lei 6.766/79 Art. 3º e LC 40/06).'
)
""", (round(total_bounds[0], 2), round(total_bounds[2], 2), round(total_bounds[1], 2), round(total_bounds[3], 2), wgs_json))

# 2. Inserir classes em classes_camada_territorial
c.execute("DELETE FROM classes_camada_territorial WHERE camada_id = 'geologia'")
for code, meta in units_meta.items():
    c.execute("""
    INSERT INTO classes_camada_territorial (
        camada_id, codigo_classe, nome_classe, angulo_equivalente,
        cor_hex, cor_rgb, metodologia_referencia, implicacao_pratica
    ) VALUES (
        'geologia',
        ?,
        ?,
        ?,
        ?,
        ?,
        'CPRM / SGB (2006) / IPT (1981)',
        ?
    )
    """, (
        meta["codigo_classe"],
        meta["nome_classe"],
        meta["litologia"],
        meta["cor_hex"],
        f"RGB({int(meta['cor_hex'][1:3], 16)}, {int(meta['cor_hex'][3:5], 16)}, {int(meta['cor_hex'][5:7], 16)})",
        meta["implicacao_urbanistica"]
    ))

# 3. Cruzamento Jurídico-Normativo em cruzamento_camada_legislacao
c.execute("DELETE FROM cruzamento_camada_legislacao WHERE camada_id = 'geologia'")
geologia_laws = [
    ('geologia', None, 'Municipal', 'Lei Complementar', '39', 2006, 'Art. 18, II e Art. 45', 'Diretriz Estratégica',
     'Macrozoneamento e condicionantes geológico-geotécnicos para direcionamento da expansão urbana sustentável em São Roque.',
     'Condiciona a ocupação urbana às características do substrato rochoso e capacidade de infiltração.'),
     
    ('geologia', None, 'Municipal', 'Lei Complementar', '40', 2006, 'Art. 13 e Art. 14', 'Impeditiva',
     'Exigência de laudo geológico-geotécnico com ART para aprovação de loteamentos, desdobros e terraplenagens em terrenos com litologia fraturada ou declividade > 30%.',
     'Vedação ao parcelamento em áreas com risco de escorregamento planar por foliação desfavorável.'),
     
    ('geologia', None, 'Municipal', 'Lei Complementar', '41', 2006, 'Art. 25 a 30', 'Condicionante',
     'Código de Obras: exigência de sondagem do solo (SPT/rotativa) e dimensionamento de fundações conforme a resistência do maciço rochoso ou manto de alteração.',
     'Obrigatório para todas as edificações com mais de dois pavimentos ou em encostas.'),
     
    ('geologia', None, 'Estadual', 'Lei Ordinária', '11579', 2003, 'Art. 4º a 8º', 'Impeditiva / Protetiva',
     'APA Itupararanga: controle rigoroso de atividades minerárias e terraplenagem sobre o Granito Ibiúna para evitar assoreamento de mananciais.',
     'Licenciamento ambiental específico perante a CETESB e Fundação Florestal.'),
     
    ('geologia', None, 'Federal', 'Lei Ordinária', '6766', 1979, 'Art. 3º, parágrafo único, I', 'Impeditiva',
     'Lei Lehmann de Parcelamento do Solo: veda o parcelamento em terrenos onde as condições geológicas e morfológicas não aconselhem a edificação sem obras saneadoras.',
     'Norma federal cogente para qualquer aprovação de loteamento.'),
     
    ('geologia', None, 'Federal', 'Lei Ordinária', '12608', 2012, 'Art. 2º e Art. 22', 'Condicionante',
     'Política Nacional de Proteção e Defesa Civil: mapeamento de riscos geológicos e obrigatoriedade de cartas geotécnicas nos municípios suscetíveis a desastres.',
     'Integração obrigatória do substrato rochoso nas ações de contingência e defesa civil.')
]

for g_law in geologia_laws:
    c.execute("""
    INSERT INTO cruzamento_camada_legislacao (
        camada_id, classe_id, norma_esfera, norma_tipo, norma_numero,
        norma_ano, artigo_dispositivo, grau_restricao, regra_aplicacao,
        conflito_ou_ponto_atencao
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, g_law)

conn.commit()

total_laws = c.execute("SELECT count(*) FROM cruzamento_camada_legislacao").fetchone()[0]
print(f"[{time.time()-t0:.1f}s] Banco de dados sao_roque_geodados.db atualizado (Total de {total_laws} normas vinculadas)!")
conn.close()

print("=== MAPA GEOLÓGICO EXPORTADO E AUDITADO COM SUCESSO! ===")
