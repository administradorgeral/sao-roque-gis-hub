import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes
import time
import json
import os
import sqlite3
from shapely.geometry import Polygon, MultiPolygon
from shapely.validation import make_valid
from shapely.ops import unary_union
import geopandas as gpd

print("=== EXPORTAÇÃO DA CAMADA DE ZONEAMENTO AMBIENTAL (PDA 2019 - ANEXO 8.3.1-1) ===")
t_total_start = time.time()

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\Mapa_Anexo_8.3.1-1_Zoneamento_2019.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]
objs = list(page.get_objects())

slope_x, intercept_x = 17.637839, 271182.44
slope_y, intercept_y = 17.638906, 7381568.28

def pdf_to_utm(px, py):
    return (slope_x * px + intercept_x, slope_y * py + intercept_y)

r, g, b, a = ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint()
fm, st = ctypes.c_int(), ctypes.c_int()
x, y = ctypes.c_float(), ctypes.c_float()

zones_meta = {
    '#CA7AF5': {
        'codigo_classe': 'ZDES_CB',
        'macroclasse': 'Zona Prioritária de Desenvolvimento',
        'nome_classe': 'Subzona de Desenvolvimento Socioeconômico - Castelo Branco',
        'cor_hex': '#CA7AF5',
        'diretriz_ambiental': 'Polo de logística, indústria limpa e serviços avançados ao longo do Corredor Castelo Branco, compatibilizado com infraestrutura ambiental robusta.',
        'implicacao_uso': 'Permite ocupação industrial e terciária de grande porte com exigência de tratamento de efluentes e retenção pluvial on-site.',
        'legislacao_principal': 'LC nº 39/06 (Art. 45), LC nº 40/06 (Zona Industrial/Corredor), LC nº 41/06 (Art. 15), Lei Federal nº 6.766/79'
    },
    '#E8BEFF': {
        'codigo_classe': 'ZDES_SA',
        'macroclasse': 'Zona Prioritária de Desenvolvimento',
        'nome_classe': 'Subzona de Desenvolvimento Socioambiental',
        'cor_hex': '#E8BEFF',
        'diretriz_ambiental': 'Ocupação de baixa densidade com estímulo ao ecoturismo, turismo enogastronômico (Roteiro do Vinho), lazer sustentável e preservação paisagística.',
        'implicacao_uso': 'Taxa de ocupação reduzida, manutenção obrigatória de cobertura vegetal nativa e controle de drenagem superficial.',
        'legislacao_principal': 'LC nº 39/06 (Art. 13), LC nº 40/06 (Zona de Turismo e Lazer / ZTL), LC nº 41/06'
    },
    '#4CE600': {
        'codigo_classe': 'ZPBIO',
        'macroclasse': 'Proteção Integral e Biodiversidade',
        'nome_classe': 'Zona Prioritária de Proteção à Biodiversidade',
        'cor_hex': '#4CE600',
        'diretriz_ambiental': 'Maciços florestais contínuos de Mata Atlântica (Mata da Câmara, cristas do Saboó, Alto da Serra e morros orientais). Conservação genética e corredores ecológicos.',
        'implicacao_uso': 'Área non aedificandi de preservação estrita; proibida supressão vegetal primária e parcelamento urbano.',
        'legislacao_principal': 'Lei Federal nº 11.428/06 (Lei da Mata Atlântica), Lei nº 12.651/12 (Art. 4º), STF ADPF 747/749, LC nº 39/06'
    },
    '#FFAA00': {
        'codigo_classe': 'ZPED_ERO',
        'macroclasse': 'Zona Prioritária de Recursos Edáficos',
        'nome_classe': 'Subzona Especial para Controle de Processos Erosivos',
        'cor_hex': '#FFAA00',
        'diretriz_ambiental': 'Encostas com solos frágeis (Argissolos com B textural) e relevo forte ondulado sujeitos a ravinamento, sulcos e desestabilização geotécnica.',
        'implicacao_uso': 'Restrição severa a terraplenagem; obras condicionadas a projetos detalhados de drenagem e muros de contenção dimensionados por ART.',
        'legislacao_principal': 'LC nº 39/06 (Art. 18), LC nº 40/06 (Art. 31), LC nº 41/06 (Art. 18 e 42), Lei Federal nº 6.766/79 (Art. 3º)'
    },
    '#FFFF00': {
        'codigo_classe': 'ZPED_ESCO',
        'macroclasse': 'Zona Prioritária de Recursos Edáficos',
        'nome_classe': 'Subzona Especial de Controle Escoamento Superficial Águas Pluviais',
        'cor_hex': '#FFFF00',
        'diretriz_ambiental': 'Bacias de amortecimento pluvial intermediário com relevo ondulado; controle de enxurradas e retenção hidrológica da macro e microdrenagem.',
        'implicacao_uso': 'Exigência de bacias de infiltração, pavimentos permeáveis e respeito a taxas mínimas de permeabilidade do solo.',
        'legislacao_principal': 'LC nº 40/06 (Art. 24 e 25), LC nº 41/06 (Art. 15), Lei Federal nº 12.608/12'
    },
    '#FF7F7F': {
        'codigo_classe': 'ZPURB',
        'macroclasse': 'Gestão aos Processos de Urbanização',
        'nome_classe': 'Zona Prioritária de Gestão aos Processos de Urbanização',
        'cor_hex': '#FF7F7F',
        'diretriz_ambiental': 'Áreas urbanas consolidadas e distritos (Centro de São Roque, Mailasqui, Canguera, São João Novo); compatibilização entre adensamento e infraestrutura.',
        'implicacao_uso': 'Adensamento urbano condicionado à capacidade da rede pública de água, esgoto, coleta e drenagem pluvial.',
        'legislacao_principal': 'LC nº 39/06 (Macrozoneamento Urbano), LC nº 40/06 (Zonas Urbanas ZU-1, ZU-2, ZU-3), LC nº 41/06 (Código de Edificações)'
    },
    '#004DA8': {
        'codigo_classe': 'ZPHID_SEN',
        'macroclasse': 'Zona Prioritária de Recursos Hídricos',
        'nome_classe': 'Subzona de Áreas Hidrologicamente Sensíveis',
        'cor_hex': '#004DA8',
        'diretriz_ambiental': 'Margens imediatas da Represa de Itupararanga, várzeas de cabeceira e zonas de inundação crítica dos rios Guaçu e Carambeí.',
        'implicacao_uso': 'Preservação absoluta da faixa marginal de APP; vedada qualquer atividade potencialmente poluidora ou impermeabilização.',
        'legislacao_principal': 'Lei Federal nº 12.651/12 (Art. 4º, I), Lei Estadual nº 11.579/03, LC nº 39/06 (Arts. 60-64)'
    },
    '#00C5FF': {
        'codigo_classe': 'ZPHID_RUR',
        'macroclasse': 'Zona Prioritária de Recursos Hídricos',
        'nome_classe': 'Subzona de Manancial em Áreas Rurais',
        'cor_hex': '#00C5FF',
        'diretriz_ambiental': 'Bacia hidrográfica formadora de mananciais rurais da APA Itupararanga; práticas agrícolas conservacionistas e proteção de nascentes.',
        'implicacao_uso': 'Controle de agrotóxicos, proibição de efluentes in natura, exigência de fossas sépticas licenciadas e manutenção de florestas protetoras.',
        'legislacao_principal': 'Lei Estadual nº 11.579/03, Decreto Estadual nº 32.955/91, LC nº 39/06 (Art. 62)'
    },
    '#73DFFF': {
        'codigo_classe': 'ZPHID_INT',
        'macroclasse': 'Zona Prioritária de Recursos Hídricos',
        'nome_classe': 'Subzona de Manancial em Usos Intensivos ou Urbanizados',
        'cor_hex': '#73DFFF',
        'diretriz_ambiental': 'Áreas de mananciais limítrofes à malha urbana e loteamentos na bacia do Itupararanga (Vargem Grande Paulista / Canguera).',
        'implicacao_uso': 'Ocupação urbana com coeficiente de aproveitamento restrito e 100% de coleta e tratamento de esgoto obrigatório antes de qualquer liberação de habite-se.',
        'legislacao_principal': 'Lei Estadual nº 11.579/03, Lei Federal nº 6.766/79, LC nº 40/06, LC nº 41/06'
    }
}

zone_polys = {k: [] for k in zones_meta}

for idx in range(0, 29):
    p = objs[idx]
    pdfium_c.FPDFPageObj_GetFillColor(p.raw, ctypes.byref(r), ctypes.byref(g), ctypes.byref(b), ctypes.byref(a))
    f_hex = f'#{r.value:02X}{g.value:02X}{b.value:02X}'
    
    if f_hex == '#C4F5DE':
        continue
        
    if f_hex in zones_meta:
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

doc.close()

# Dissolve each zone
dissolved = {}
for f_hex, plist in zone_polys.items():
    u = unary_union(plist)
    if not u.is_valid:
        u = make_valid(u)
    dissolved[f_hex] = u

total_ha = sum(u.area for u in dissolved.values()) / 10000.0
print(f"Área Total Zoneada: {total_ha:.2f} ha (PDA São Roque: 30.709,52 ha)")

records = []
for f_hex, geom in dissolved.items():
    meta = zones_meta[f_hex]
    area_ha = round(geom.area / 10000.0, 2)
    pct = round((area_ha / total_ha) * 100, 2)
    records.append({
        'camada': 'Zoneamento Ambiental (PDA 2019)',
        'anexo_oficial': 'Anexo 8.3.1-1 - PDA 2019',
        'codigo_classe': meta['codigo_classe'],
        'macroclasse': meta['macroclasse'],
        'nome_classe': meta['nome_classe'],
        'cor_hex': f_hex,
        'diretriz_ambiental': meta['diretriz_ambiental'],
        'area_ha': area_ha,
        'porcentagem': pct,
        'implicacao_uso': meta['implicacao_uso'],
        'legislacao_principal': meta['legislacao_principal'],
        'geometry': geom
    })
    print(f"  {meta['codigo_classe']}: {area_ha} ha ({pct}%)")

gdf = gpd.GeoDataFrame(records, crs="EPSG:31983")

# Salvar GeoPackage
gpkg_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\data\zoneamento_ambiental_pda2019_sao_roque.gpkg"
gdf.to_file(gpkg_path, layer="zoneamento_ambiental_pda2019", driver="GPKG")
print(f"GeoPackage salvo: {gpkg_path}")

# Reprojetar para EPSG:4326 e salvar GeoJSON
gdf_wgs84 = gdf.to_crs("EPSG:4326")
total_bounds = gdf.total_bounds
wgs_bounds = gdf_wgs84.total_bounds
wgs_json = json.dumps([
    [round(wgs_bounds[1], 5), round(wgs_bounds[0], 5)],
    [round(wgs_bounds[3], 5), round(wgs_bounds[2], 5)]
])

geojson_dict = json.loads(gdf_wgs84.to_json())
def round_coords(obj):
    if isinstance(obj, list):
        if len(obj) == 2 and isinstance(obj[0], (int, float)) and isinstance(obj[1], (int, float)):
            return [round(obj[0], 5), round(obj[1], 5)]
        return [round_coords(item) for item in obj]
    return obj

for feat in geojson_dict["features"]:
    if feat.get("geometry") and "coordinates" in feat["geometry"]:
        feat["geometry"]["coordinates"] = round_coords(feat["geometry"]["coordinates"])

geojson_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\data\zoneamento_ambiental_pda2019_sao_roque_web.geojson"
with open(geojson_path, "w", encoding="utf-8") as f:
    json.dump(geojson_dict, f, ensure_ascii=False, separators=(',', ':'))

sz_kb = os.path.getsize(geojson_path) / 1024.0
print(f"GeoJSON salvo: {geojson_path} ({sz_kb:.1f} KB)")

# Ingestão no SQLite sao_roque_geodados.db
db_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\dados_oficiais\sao_roque_geodados.db"
conn = sqlite3.connect(db_path)
c = conn.cursor()

# 1. Inserir em camadas_territoriais
c.execute("""
INSERT OR REPLACE INTO camadas_territoriais (
    id, nome, titulo_documento, categoria, arquivo_origem, tipo_camada,
    escala_nominal, datum_projecao, data_elaboracao, responsavel_tecnico,
    responsavel_crea, desenho_tecnico, desenho_crea, fonte_cartografica,
    status_auditoria, bbox_utm_x0, bbox_utm_x1, bbox_utm_y0, bbox_utm_y1,
    bounds_wgs84_json, alerta_juridico
) VALUES (
    'zoneamento_ambiental_pda2019',
    'Zoneamento Ambiental (PDA 2019)',
    'ANEXO 8.3.1-1 - MAPA DE ZONEAMENTO AMBIENTAL DO MUNICÍPIO DE SÃO ROQUE',
    'Ambiental e Geotécnica',
    'Mapa_Anexo_8.3.1-1_Zoneamento_2019.pdf',
    'vetor_poligonos',
    '1:50.000',
    'SIRGAS 2000 UTM Zone 23S',
    '20/12/2018',
    'Maurício Scorsatto Sartori (Eng. Florestal)',
    '5.060.532.187',
    'Ana Clara Cerminaro (Analista de Geoprocessamento)',
    '473.423.455',
    'Plano Diretor Ambiental de São Roque (PDA 2019) / IGC (1978) / SEMIL / IPT',
    'Auditado, Calibrado e Dissolvido (9 Zonas e Subzonas Ambientais Oficiais PDA 2019)',
    ?, ?, ?, ?,
    ?,
    '🌿 DIRETRIZ AMBIENTAL E DE MACROZONEAMENTO: O Zoneamento Ambiental do PDA 2019 complementa e condiciona o Zoneamento Municipal da LC 40/2006. As zonas prioritárias hídricas (ZPHID) e edáficas (ZPED) impõem restrições de permeabilidade, retenção pluvial e contenção de encostas que vinculam qualquer licenciamento de obras (LC 41/06) e loteamentos (Lei Federal 6.766/79 e Lei 12.608/12).'
)
""", (
    round(total_bounds[0], 2), round(total_bounds[2], 2),
    round(total_bounds[1], 2), round(total_bounds[3], 2),
    wgs_json
))

# 2. Inserir em classes_camada_territorial
c.execute("DELETE FROM classes_camada_territorial WHERE camada_id = 'zoneamento_ambiental_pda2019'")
for r in records:
    c.execute("""
    INSERT INTO classes_camada_territorial
    (camada_id, codigo_classe, nome_classe, angulo_equivalente, cor_hex, cor_rgb, metodologia_referencia, implicacao_pratica)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "zoneamento_ambiental_pda2019",
        r['codigo_classe'],
        r['nome_classe'],
        r['macroclasse'],
        r['cor_hex'],
        f"RGB({int(r['cor_hex'][1:3], 16)}, {int(r['cor_hex'][3:5], 16)}, {int(r['cor_hex'][5:7], 16)})",
        "PDA (2019) / Anexo 8.3.1-1",
        f"{r['diretriz_ambiental']} {r['implicacao_uso']} · Área: {r['area_ha']} ha ({r['porcentagem']}%)"
    ))

# 3. Inserir em cruzamento_camada_legislacao
c.execute("DELETE FROM cruzamento_camada_legislacao WHERE camada_id = 'zoneamento_ambiental_pda2019'")
zoneamento_laws = [
    ("zoneamento_ambiental_pda2019", "ZDES_CB", "Municipal", "Lei Complementar", "40", 2006, "Arts. 45 a 48", "Permissivo Condicionado", "Desenvolvimento industrial e logístico ao longo da Rodovia Castello Branco com Estudo de Impacto de Vizinhança (EIV) obrigatório.", "Obrigatória implantação de bacia de retenção de águas pluviais para amortecimento de pico."),
    ("zoneamento_ambiental_pda2019", "ZDES_SA", "Municipal", "Lei Complementar", "39", 2006, "Art. 13", "Sustentabilidade", "Estímulo a empreendimentos ecoturísticos, enogastronômicos e de lazer com baixa taxa de impermeabilização.", "Preservação da paisagem cênica e da silhueta dos morros."),
    ("zoneamento_ambiental_pda2019", "ZPBIO", "Federal", "Lei", "11428", 2006, "Arts. 11 a 20", "Proteção Absoluta", "Proteção integral dos remanescentes primários e secundários em estágio avançado de regeneração do Bioma Mata Atlântica.", "Vedada a supressão de vegetação e vedado o parcelamento urbano para fins residenciais."),
    ("zoneamento_ambiental_pda2019", "ZPED_ERO", "Federal", "Lei", "6766", 1979, "Art. 3º, Parágrafo Único", "Restrição Severa", "Proibição de parcelamento do solo em terrenos com declividade > 30% ou sujeitos a erosão sem prévio laudo geotécnico circunstanciado.", "Projetos de corte e aterro exigem muros de contenção e drenagem superficial por ART."),
    ("zoneamento_ambiental_pda2019", "ZPED_ESCO", "Municipal", "Lei Complementar", "41", 2006, "Art. 18", "Técnica Obrigatória", "Manejo de águas pluviais, terraceamento e amortecimento do escoamento superficial para evitar assoreamento dos cursos d'água.", "Controle rigoroso de terraplenagens e coeficiente de infiltração natural."),
    ("zoneamento_ambiental_pda2019", "ZPURB", "Municipal", "Lei Complementar", "40", 2006, "Arts. 13 a 28", "Urbana Ordinária", "Parâmetros construtivos de uso e ocupação do solo nos perímetros urbanos consolidados do Município.", "Atendimento aos coeficientes de aproveitamento máximo e taxas de permeabilidade mínima."),
    ("zoneamento_ambiental_pda2019", "ZPHID_SEN", "Federal", "Lei", "12651", 2012, "Art. 4º", "APP Absoluta", "Preservação estrita das faixas marginais de corpos hídricos e nascentes ao redor da Represa de Itupararanga.", "Áreas non aedificandi com recuperação vegetal ciliar obrigatória."),
    ("zoneamento_ambiental_pda2019", "ZPHID_RUR", "Estadual", "Lei", "11579", 2003, "Arts. 4º a 8º", "APA Estadual", "Área de Proteção Ambiental da Represa de Itupararanga; manutenção da qualidade da água e recarga dos aquíferos.", "Condicionamento de fossas sépticas e atividades agrícolas a boas práticas conservacionistas."),
    ("zoneamento_ambiental_pda2019", "ZPHID_INT", "Municipal", "Lei Complementar", "39", 2006, "Arts. 60 a 64", "Mananciais Urbanos", "Zona de Proteção aos Mananciais com ocupação urbana controlada e 100% de esgotamento sanitário obrigatório.", "Vedada instalação de atividades potencialmente poluidoras de mananciais subterrâneos ou superficiais.")
]

for row in zoneamento_laws:
    c.execute("""
    INSERT INTO cruzamento_camada_legislacao
    (camada_id, classe_id, norma_esfera, norma_tipo, norma_numero, norma_ano, artigo_dispositivo, grau_restricao, regra_aplicacao, conflito_ou_ponto_atencao)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, row)

conn.commit()

c.execute("SELECT count(*) FROM cruzamento_camada_legislacao")
total_laws = c.fetchone()[0]
c.execute("SELECT count(*) FROM camadas_territoriais")
total_layers = c.fetchone()[0]
c.execute("SELECT count(*) FROM classes_camada_territorial WHERE camada_id = 'zoneamento_ambiental_pda2019'")
total_classes = c.fetchone()[0]
conn.close()

print(f"Banco de dados atualizado: {total_layers} camadas ativas, {total_classes} zonas ambientais, {total_laws} vinculações normativas registradas!")
print(f"=== SUCESSO TOTAL EM {time.time()-t_total_start:.1f}s ===")
