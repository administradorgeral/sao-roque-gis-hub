import geopandas as gpd
import json
import os
import sqlite3
import time

print("=== OTIMIZAÇÃO WEB E INGESTÃO SQLITE - FRAGILIDADE POTENCIAL ===")

gpkg_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\data\fragilidade_potencial_sao_roque.gpkg"
gdf = gpd.read_file(gpkg_path, layer="fragilidade_potencial")

total_bounds = gdf.total_bounds # minx, miny, maxx, maxy
total_area_ha = sum(gdf['area_ha'])

# Simplify with 4.0 meters tolerance (0.08 mm at 1:50k scale, pristine quality, fast web rendering)
gdf_web = gdf.copy()
gdf_web['geometry'] = gdf_web['geometry'].simplify(4.0, preserve_topology=True)

# Reproject to WGS84
gdf_wgs84 = gdf_web.to_crs("EPSG:4326")
wgs_bounds = gdf_wgs84.total_bounds
wgs_json = json.dumps([
    [round(wgs_bounds[1], 5), round(wgs_bounds[0], 5)],
    [round(wgs_bounds[3], 5), round(wgs_bounds[2], 5)]
])

# Round coordinates to 5 decimal places (~1.1 meter precision)
geojson_dict = json.loads(gdf_wgs84.to_json())
def round_coords(obj):
    if isinstance(obj, list):
        if len(obj) == 2 and isinstance(obj[0], (int, float)) and isinstance(obj[1], (int, float)):
            return [round(obj[0], 5), round(obj[1], 5)]
        return [round_coords(item) for item in obj]
    return obj

for feat in geojson_dict["features"]:
    feat["geometry"]["coordinates"] = round_coords(feat["geometry"]["coordinates"])

geojson_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\data\fragilidade_potencial_sao_roque_web.geojson"
with open(geojson_path, "w", encoding="utf-8") as f:
    json.dump(geojson_dict, f, ensure_ascii=False, separators=(',', ':'))

sz_kb = os.path.getsize(geojson_path) / 1024.0
print(f"GeoJSON otimizado gravado com sucesso: {geojson_path} ({sz_kb:.1f} KB / {sz_kb/1024.0:.2f} MB)")

# Ingestão no SQLite
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
    'fragilidade_potencial',
    'Fragilidade Potencial e Erosão',
    'ANEXO 7.3.1-1 - MAPA DE FRAGILIDADE POTENCIAL DO MUNICÍPIO DE SÃO ROQUE',
    'Ambiental e Geotécnica',
    'Mapa Fragilidade Potencial.pdf',
    'vetor_poligonos',
    '1:50.000',
    'SIRGAS 2000 UTM Zone 23S',
    '15/12/2018',
    'Maurício Scorsatto Sartori (Eng. Florestal)',
    '5.060.532.187',
    'Ana Clara Cerminaro (Analista de Geoprocessamento)',
    '473.423.455',
    'Plano Diretor Ambiental de São Roque (PDA 2019) / Metodologia Ross (1994) / Crepani et al. (2008)',
    'Auditado, Calibrado e Dissolvido (5 Classes Morfodinâmicas Ross 1994)',
    ?, ?, ?, ?,
    ?,
    '⚠️ RESTRIÇÃO AMBIENTAL E GEOTÉCNICA: A fragilidade potencial e suscetibilidade à erosão mecânica condiciona diretamente a ocupação do solo em São Roque. Classes Forte e Muito Forte vedam parcelamento sem laudo geotécnico circunstanciado (Lei 6.766/79 Art. 3º e LC 40/06 Art. 31), exigindo medidas de contenção de taludes (LC 41/06) e proteção rigorosa de APPs de topos de morro e encostas (Lei 12.651/12 e STF ADPF 747/749).'
)
""", (
    round(total_bounds[0], 2), round(total_bounds[2], 2),
    round(total_bounds[1], 2), round(total_bounds[3], 2),
    wgs_json
))

# 2. Inserir em classes_camada_territorial
c.execute("DELETE FROM classes_camada_territorial WHERE camada_id = 'fragilidade_potencial'")
for idx, r in gdf.iterrows():
    c.execute("""
    INSERT INTO classes_camada_territorial
    (camada_id, codigo_classe, nome_classe, angulo_equivalente, cor_hex, cor_rgb, metodologia_referencia, implicacao_pratica)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "fragilidade_potencial",
        r['codigo_classe'],
        r['nome_classe'],
        r['vulnerabilidade'],
        r['cor_hex'],
        f"RGB({int(r['cor_hex'][1:3], 16)}, {int(r['cor_hex'][3:5], 16)}, {int(r['cor_hex'][5:7], 16)})",
        "Ross (1994) / Crepani et al. (2008) / PDA 2019",
        f"{r['restricao_uso']} · Área: {r['area_ha']} ha ({r['porcentagem']}%)"
    ))

# 3. Inserir em cruzamento_camada_legislacao
c.execute("DELETE FROM cruzamento_camada_legislacao WHERE camada_id = 'fragilidade_potencial'")
fragilidade_laws = [
    ("fragilidade_potencial", "muito_fraca", "Federal", "Lei", "12651", 2012, "Art. 4º, I", "Restrição Proporcional à Faixa Marginal", "Preservação da faixa de APP ao longo dos cursos d'água em fundos de vale aluvionares.", "Incompatibilidade de qualquer edificação não dispensável dentro da faixa non aedificandi de APP."),
    ("fragilidade_potencial", "fraca", "Municipal", "Lei Complementar", "40", 2006, "Arts. 24 e 25", "Permissivo com Mitigação", "Ocupação urbana e rural com implantação de rede de macro e microdrenagem pluvial para evitar processos de ravinamento.", "Atenção ao coeficiente de permeabilidade do solo para evitar saturação superficial."),
    ("fragilidade_potencial", "media", "Municipal", "Lei Complementar", "39", 2006, "Art. 18", "Condicionado", "Condicionamento de projetos de loteamento e terraplenagem a obras de contenção de taludes e terraceamento.", "Exigência de medidas preventivas de contenção em cortes de morro superiores a 3 metros."),
    ("fragilidade_potencial", "media", "Municipal", "Lei Complementar", "41", 2006, "Art. 18", "Técnica Obrigatória", "Exigência de laudo geotécnico e dimensionamento de águas pluviais para aprovação de edificações residenciais e industriais.", "Responsabilidade técnica por ART/RRT de estabilidade do terreno."),
    ("fragilidade_potencial", "forte", "Federal", "Lei", "6766", 1979, "Art. 3º, Parágrafo Único", "Vedação / Restrição Severa", "Proibição expressa de parcelamento do solo em terrenos com declividade igual ou superior a 30% ou sujeitos a erosão e deslizamento.", "Áreas com declividade acentuada requerem comprovação de estabilidade absoluta e atendimento às diretrizes do Plano Diretor."),
    ("fragilidade_potencial", "forte", "Federal", "Lei", "12608", 2012, "Arts. 3º e 8º", "Vigilância Geotécnica", "Mapeamento obrigatório de áreas suscetíveis à ocorrência de deslizamentos de grande impacto e processos correlatos.", "Prioridade máxima de fiscalização municipal pela Defesa Civil em eventos pluviométricos extremos."),
    ("fragilidade_potencial", "muito_forte", "Estadual / Federal", "STF ADPF", "747", 2021, "Acórdão Plenário", "Proteção Integral", "Declaração de inconstitucionalidade da Resolução CONAMA 500/2020, restaurando a proteção permanente das escarpas, topos de morro e cristas.", "Nenhuma autorização municipal de desmatamento ou supressão de vegetação pode subsistir em topos de morro ou áreas de preservação permanente.")
]

for row in fragilidade_laws:
    c.execute("""
    INSERT INTO cruzamento_camada_legislacao
    (camada_id, classe_id, norma_esfera, norma_tipo, norma_numero, norma_ano, artigo_dispositivo, grau_restricao, regra_aplicacao, conflito_ou_ponto_atencao)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, row)

conn.commit()

# Auditoria final
c.execute("SELECT count(*) FROM cruzamento_camada_legislacao")
total_laws = c.fetchone()[0]
c.execute("SELECT count(*) FROM camadas_territoriais")
total_layers = c.fetchone()[0]
c.execute("SELECT count(*) FROM classes_camada_territorial WHERE camada_id = 'fragilidade_potencial'")
total_classes = c.fetchone()[0]
conn.close()

print(f"Banco de dados atualizado: {total_layers} camadas ativas, {total_classes} classes de fragilidade, {total_laws} vinculações normativas registradas!")
print("=== SUCESSO COMPLETO ===")
