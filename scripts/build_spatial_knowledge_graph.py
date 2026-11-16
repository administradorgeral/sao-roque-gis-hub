#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
SÃO ROQUE GIS HUB · MOTOR DE GRAFO TERRITORIAL MULTICAMADAS & TOPOLOGIA CRUZADA
===============================================================================
Desenvolvido em conformidade com as melhores práticas de GeoSPARQL, Linked Spatial Data,
DE-9IM Topological Relations e OGC Standards.

Elimina totalmente o uso de 'FIDs' numéricos opacos.
Todas as feições e consultas são indexadas e referenciadas por:
  [Camada Oficial] -> [Legenda Oficial / Nome Semântico]

Gera o Grafo Territorial Unificado:
  data/grafo_territorial_sao_roque.json
===============================================================================
"""

import os
import sys
import json
import time
import math
import sqlite3
import geopandas as gpd
from shapely.geometry import Point, Polygon, MultiPolygon
from pyproj import Transformer

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(BASE_DIR, "dados_oficiais", "sao_roque_geodados.db")
ROL_PATH = os.path.join(DATA_DIR, "rol_legislacao_territorial.json")
PARTICIPACAO_PATH = os.path.join(DATA_DIR, "participacao_popular_plano_diretor.json")
BASE_IA_PATH = os.path.join(DATA_DIR, "base_conhecimento_ia.json")

OUTPUT_PATH = os.path.join(DATA_DIR, "grafo_territorial_sao_roque.json")

def normalize_text(text: str) -> str:
    if not text:
        return ""
    import unicodedata
    n = unicodedata.normalize("NFD", str(text))
    clean = "".join(c for c in n if unicodedata.category(c) != "Mn")
    return clean.strip().lower()

def sanitize_json(obj):
    if isinstance(obj, dict):
        return {str(k): sanitize_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [sanitize_json(v) for v in obj]
    elif isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None
        return round(obj, 6)
    elif hasattr(obj, "item"):
        val = obj.item()
        if isinstance(val, float) and (math.isnan(val) or math.isinf(val)):
            return None
        return val
    return obj

def main():
    t0 = time.time()
    print("=" * 75)
    print("SÃO ROQUE GIS HUB · CONSTRUÇÃO DO GRAFO TERRITORIAL MULTICAMADAS")
    print("=" * 75)

    # 1. Carregar Dados Auxiliares
    zonas_parametros = {}
    if os.path.exists(ROL_PATH):
        with open(ROL_PATH, "r", encoding="utf-8") as f:
            rol = json.load(f)
            zonas_parametros = rol.get("zonas_parametros", {})
            print(f"[*] Parâmetros de zonas carregados: {len(zonas_parametros)} zonas.")

    participacao_data = []
    if os.path.exists(PARTICIPACAO_PATH):
        with open(PARTICIPACAO_PATH, "r", encoding="utf-8") as f:
            part = json.load(f)
            participacao_data = part if isinstance(part, list) else part.get("demandas_revisao_2026", [])
            print(f"[*] Demandas de participação popular carregadas: {len(participacao_data)} registros.")

    base_ia = {}
    if os.path.exists(BASE_IA_PATH):
        with open(BASE_IA_PATH, "r", encoding="utf-8") as f:
            base_ia = json.load(f)
            print(f"[*] Base de IA carregada: {len(base_ia.get('cartas_pd2026', []))} cartas, {len(base_ia.get('obras_prioritarias_srq', []))} obras, {len(base_ia.get('bairros_localidades', []))} bairros.")

    # 2. Carregar Camadas Vetoriais
    layers = {}
    layer_definitions = [
        ("distritos", "distritos_sao_roque_web.geojson", "Divisão Distrital Oficial"),
        ("setores_censitarios", "setores_censitarios_sao_roque_web.geojson", "Bairros e Setores Censitários (IBGE)"),
        ("zoneamento_2006", "pmsr_zoneamento_pmd2006.geojson", "Zoneamento Municipal (LC 40/2006)"),
        ("pedologia", "pedologico_sao_roque_web.geojson", "Pedologia e Solos (PDA 2019)"),
        ("geologia", "geologia_sao_roque_web.geojson", "Geologia e Geotecnia (CPRM/PDA 2019)"),
        ("geomorfologia", "geomorfologico_sao_roque_web.geojson", "Geomorfologia e Relevo (IPT/PDA 2019)"),
        ("fragilidade", "fragilidade_potencial_sao_roque_web.geojson", "Fragilidade Ambiental Potencial (PDA 2019)"),
        ("apa_itupararanga", "apa_itupararanga_limite_sao_roque_web.geojson", "Área de Proteção Ambiental da Represa de Itupararanga"),
        ("aeroporto_catarina", "zona_protecao_aeroportuaria_catarina_web.geojson", "Zona de Proteção Aeroportuária Catarina (SBJH / DECEA)"),
        ("ahs", "ahs_sao_roque_web.geojson", "Áreas Hidrologicamente Sensíveis (AHS)"),
        ("vegetacao_arborea", "vegetacao_arborea_sao_roque_web.geojson", "Vegetação Nativa da Mata Atlântica"),
        ("rbcv", "rbcv_cinturao_verde_nucleos_web.geojson", "Reserva da Biosfera do Cinturão Verde (UNESCO)"),
        ("logradouros", "logradouros_sao_roque_web.geojson", "Sistema Viário e Logradouros")
    ]

    for key, fname, desc in layer_definitions:
        fpath = os.path.join(DATA_DIR, fname)
        if os.path.exists(fpath):
            try:
                gdf = gpd.read_file(fpath)
                if gdf.crs != "EPSG:4326":
                    gdf = gdf.to_crs(epsg=4326)
                _ = gdf.sindex
                layers[key] = (gdf, desc)
                print(f"  [+] {desc} ({fname}): {len(gdf)} feições.")
            except Exception as e:
                print(f"  [!] Erro ao carregar {fname}: {e}")

    # 3. Construir Catálogo de Entidades Semânticas (Sem FIDs!)
    print("\n[*] Indexando Entidades Semânticas e Criando Nós do Grafo...")
    graph = {
        "metadata": {
            "titulo": "Grafo de Inteligência Territorial Multicamadas de São Roque",
            "padrao": "GeoSPARQL / OGC Linked Data / Topological DE-9IM",
            "versao": "2.0.0",
            "data_compilacao": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "municipio": "Estância Turística de São Roque (SP)",
            "codigo_ibge": "3550605",
            "nota_semantica": "Todas as referências são formuladas como [Nome da Camada]: [Legenda Oficial], sem dependência de FIDs numéricos."
        },
        "distritos": {},
        "bairros": {},
        "logradouros": {},
        "zonas_2006": {},
        "cartas_2026": {},
        "solos_pedologia": {},
        "unidades_geologicas": {},
        "compartimentos_geomorfologicos": {},
        "fragilidades": {},
        "unidades_conservacao": {},
        "obras_estruturantes_2026": {},
        "matriz_cruzada_zonas": {},
        "matriz_cruzada_vias": {}
    }

    # 3.1 Distritos
    if "distritos" in layers:
        gdf_dist = layers["distritos"][0]
        for _, row in gdf_dist.iterrows():
            nome_dist = row.get("distrito") or row.get("nome")
            clean_name = nome_dist.replace("Distrito de ", "").replace("Distrito ", "").strip()
            key = f"distrito:{normalize_text(clean_name)}"
            graph["distritos"][key] = {
                "id": key,
                "nome_oficial": row.get("nome"),
                "distrito": clean_name,
                "camada": "Divisão Distrital Oficial",
                "legenda_oficial": f"Distrito de {clean_name}",
                "area_ha": row.get("area_ha"),
                "area_km2": row.get("area_km2"),
                "porcentagem_municipio": row.get("porcentagem_municipio"),
                "cor_hex": row.get("cor_hex", "#2563EB"),
                "vias_principais": [],
                "zonas_presentes": [],
                "obras_prioritarias": []
            }

    # 3.2 Obras Estruturantes da Carta XIII (SRQ-01 a SRQ-22)
    obras_list = base_ia.get("obras_prioritarias_srq", [])
    for obra in obras_list:
        codigo = obra.get("codigo") # SRQ-01..22
        key = f"obra:{codigo.lower()}"
        graph["obras_estruturantes_2026"][key] = {
            "id": key,
            "codigo": codigo,
            "nome": obra.get("nome"),
            "camada": "Carta XIII: 22 Obras Estruturantes Prioritárias (2026)",
            "legenda_oficial": f"{codigo} - {obra.get('nome')}",
            "local": obra.get("local"),
            "tipo_intervencao": obra.get("tipo"),
            "descricao": obra.get("descricao")
        }

    # 3.3 Cartas do Plano Diretor 2026
    cartas_list = base_ia.get("cartas_pd2026", [])
    for c in cartas_list:
        romano = c.get("romano")
        key = f"carta_2026:{c.get('camada_id', romano.lower())}"
        graph["cartas_2026"][key] = {
            "id": key,
            "numero": c.get("numero"),
            "romano": romano,
            "titulo": c.get("titulo"),
            "camada": f"Carta {romano}: {c.get('titulo')}",
            "legenda_oficial": c.get("titulo"),
            "folha": c.get("folha"),
            "descricao": c.get("descricao"),
            "zonas_principais": c.get("zonas_principais", []),
            "leis_correlatas": c.get("leis_correlatas", [])
        }

    # 3.3.1 Bairros e Localidades de São Roque
    bairros_list = base_ia.get("bairros_localidades", [])
    for b in bairros_list:
        b_nome = b.get("nome")
        key = f"bairro:{normalize_text(b_nome)}"
        centro = b.get("centro", [-23.535, -47.135, 14])
        graph["bairros"][key] = {
            "id": key,
            "nome": b_nome,
            "distrito": b.get("distrito"),
            "camada": "Bairros e Localidades Oficiais",
            "legenda_oficial": f"Bairro {b_nome} ({b.get('distrito')})",
            "cartas_incidentes": b.get("cartas", []),
            "zoneamento_padrao": b.get("zoneamento_padrao"),
            "descricao": b.get("descricao"),
            "centro": {
                "lat": centro[0] if len(centro) > 0 else -23.535,
                "lng": centro[1] if len(centro) > 1 else -47.135
            },
            "vias_principais": [],
            "obras_proximas": [],
            "demandas_populares": []
        }

    # 3.4 Zonas de Uso do Solo LC 40/2006
    if "zoneamento_2006" in layers:
        gdf_zone = layers["zoneamento_2006"][0]
        for _, row in gdf_zone.iterrows():
            sigla = row.get("sigla") or row.get("zona")
            denominacao = row.get("denominacao") or row.get("zona")
            if not sigla:
                continue
            key = f"zona:{normalize_text(sigla)}"
            params = zonas_parametros.get(sigla, {})
            graph["zonas_2006"][key] = {
                "id": key,
                "sigla": sigla,
                "denominacao": denominacao,
                "camada": "Zoneamento Municipal (LC 40/2006)",
                "legenda_oficial": f"{sigla} · {denominacao}",
                "lei_regulamentadora": row.get("lei_regulamentadora"),
                "orgao_gestor": row.get("orgao_gestor"),
                "cor_hex": row.get("cor", "#2563eb"),
                "parametros_construtivos": {
                    "coeficiente_aproveitamento_basico": params.get("coeficiente_aproveitamento_basico"),
                    "coeficiente_aproveitamento_maximo": params.get("coeficiente_aproveitamento_maximo"),
                    "taxa_ocupacao_maxima": params.get("taxa_ocupacao_maxima"),
                    "taxa_permeabilidade_minima": params.get("taxa_permeabilidade_minima"),
                    "lote_minimo_m2": params.get("lote_minimo_m2"),
                    "testada_minima_m": params.get("testada_minima_m"),
                    "gabarito_maximo": params.get("gabarito_maximo"),
                    "recuo_frontal_m": params.get("recuo_frontal_m"),
                    "recuo_lateral_fundos_m": params.get("recuo_lateral_fundos_m"),
                    "usos_permitidos": params.get("usos_permitidos", []),
                    "usos_proibidos": params.get("usos_proibidos", [])
                },
                "distritos_onde_ocorre": [],
                "vias_que_atravessam": [],
                "solos_incidentes": [],
                "percentual_apa_itupararanga": 0.0
            }

    # 3.5 Pedologia / Solos
    if "pedologia" in layers:
        gdf_ped = layers["pedologia"][0]
        for _, row in gdf_ped.iterrows():
            cod = row.get("codigo_classe")
            macro = row.get("macroclasse")
            nome_classe = row.get("nome_classe")
            key = f"solo:{normalize_text(cod)}"
            graph["solos_pedologia"][key] = {
                "id": key,
                "codigo_classe": cod,
                "macroclasse": macro,
                "nome_classe": nome_classe,
                "camada": "Pedologia e Solos (PDA 2019)",
                "legenda_oficial": nome_classe,
                "textura": row.get("textura"),
                "relevo": row.get("relevo"),
                "permeabilidade": row.get("permeabilidade"),
                "area_ha": row.get("area_ha"),
                "porcentagem_municipio": row.get("porcentagem"),
                "implicacao_obras": row.get("implicacao_obras"),
                "legislacao_principal": row.get("legislacao_principal"),
                "cor_hex": row.get("cor_hex")
            }

    # 3.6 Geologia
    if "geologia" in layers:
        gdf_geol = layers["geologia"][0]
        for _, row in gdf_geol.iterrows():
            nome = row.get("nome") or row.get("classe")
            cod = row.get("codigo_classe") or normalize_text(nome)
            key = f"geologia:{normalize_text(cod)}"
            graph["unidades_geologicas"][key] = {
                "id": key,
                "codigo": cod,
                "nome": nome,
                "camada": "Geologia e Geotecnia (CPRM/PDA 2019)",
                "legenda_oficial": f"Geologia: {nome}",
                "hierarquia": row.get("Hierarquia Estratigráfica"),
                "litologia": row.get("Litologia Principal"),
                "relevo_associado": row.get("Relevo Associado"),
                "comportamento_geotecnico": row.get("Comportamento Geotécnico"),
                "diretriz_urbanistica": row.get("Diretriz Urbanística e Construtiva"),
                "base_legal": row.get("Base Legal Normativa"),
                "cor_hex": row.get("cor_hex")
            }

    # 3.7 Geomorfologia
    if "geomorfologia" in layers:
        gdf_geom = layers["geomorfologia"][0]
        for _, row in gdf_geom.iterrows():
            nome = row.get("nome") or row.get("classe")
            cod = row.get("codigo_classe") or normalize_text(nome)
            key = f"geomorfologia:{normalize_text(cod)}"
            graph["compartimentos_geomorfologicos"][key] = {
                "id": key,
                "codigo": cod,
                "nome": nome,
                "camada": "Geomorfologia e Relevo (IPT/PDA 2019)",
                "legenda_oficial": f"Compartimento Geomorfológico: {nome}",
                "relevo_associado": row.get("Relevo Associado"),
                "declividade_media": row.get("Declividade Média"),
                "fragilidade_morfodinamica": row.get("Fragilidade Morfodinâmica"),
                "aptidao_urbanizacao": row.get("Aptidão à Urbanização"),
                "diretrizes": row.get("Diretrizes Urbanísticas"),
                "cor_hex": row.get("cor_hex")
            }

    # 3.8 Fragilidade Potencial
    if "fragilidade" in layers:
        gdf_frag = layers["fragilidade"][0]
        for _, row in gdf_frag.iterrows():
            cod = row.get("codigo_classe")
            nome = row.get("nome_classe")
            key = f"fragilidade:{normalize_text(cod)}"
            graph["fragilidades"][key] = {
                "id": key,
                "codigo": cod,
                "nome": nome,
                "camada": "Fragilidade Ambiental Potencial (PDA 2019)",
                "legenda_oficial": f"Fragilidade à Erosão: {nome}",
                "vulnerabilidade": row.get("vulnerabilidade"),
                "restricao_uso": row.get("restricao_uso"),
                "legislacao": row.get("legislacao_principal"),
                "cor_hex": row.get("cor_hex")
            }

    # 3.9 Unidades de Conservação e Proteção
    graph["unidades_conservacao"]["apa_itupararanga"] = {
        "id": "unidade_conservacao:apa_itupararanga",
        "nome": "Área de Proteção Ambiental da Represa de Itupararanga",
        "camada": "Unidades de Conservação Estaduais",
        "legenda_oficial": "APA da Represa de Itupararanga (Lei Estadual nº 11.579/2003)",
        "esfera": "Estadual",
        "orgao": "Fundação Florestal / SEMIL-SP",
        "legislacao": "Lei Estadual 11.579/03, Decreto 52.879/08 (Plano de Manejo), Lei 9.866/97 (Mananciais)",
        "regras_chave": [
            "Proibição de loteamentos com alta densidade na bacia de drenagem.",
            "Lote mínimo de 1.000 m² a 5.000 m² conforme subzona.",
            "Tratamento biológico de efluentes sanitários obrigatório; vedado lançamento in natura no lençol freático.",
            "Anuência prévia da Fundação Florestal e do COMDEMA para novos empreendimentos."
        ]
    }
    graph["unidades_conservacao"]["rbcv_unesco"] = {
        "id": "unidade_conservacao:rbcv_unesco",
        "nome": "Reserva da Biosfera do Cinturão Verde da Cidade de São Paulo",
        "camada": "Reserva da Biosfera Internacional (UNESCO / MaB)",
        "legenda_oficial": "Zonas-Núcleo e Amortecimento da RBCV (UNESCO)",
        "esfera": "Internacional / Federal / Estadual",
        "orgao": "UNESCO MaB / Fundação Florestal",
        "legislacao": "Resolução 28 C/2.4 UNESCO, Lei 9.985/00 Art. 41, Decreto Estadual 47.094/02"
    }

    # 4. Cruzamento Espacial Topológico de Logradouros (4.868 segmentos viários)
    print("\n[*] Processando Cruzamentos Espaciais dos Logradouros (Vias x Zonas x Solos x Distritos x APA)...")
    if "logradouros" in layers:
        gdf_log = layers["logradouros"][0]
        gdf_dist = layers.get("distritos", (None,))[0]
        gdf_zone = layers.get("zoneamento_2006", (None,))[0]
        gdf_ped = layers.get("pedologia", (None,))[0]
        gdf_apa = layers.get("apa_itupararanga", (None,))[0]

        apa_poly = gdf_apa.unary_union if gdf_apa is not None else None

        vias_agregadas = {}

        for idx, row in gdf_log.iterrows():
            nome_via = row.get("nome")
            if not nome_via or nome_via.strip() == "":
                continue
            
            nome_via_clean = nome_via.strip()
            via_key = f"rua:{normalize_text(nome_via_clean)}"
            geom = row.geometry
            if geom is None or geom.is_empty:
                continue

            if via_key not in vias_agregadas:
                vias_agregadas[via_key] = {
                    "id": via_key,
                    "nome_oficial": nome_via_clean,
                    "camada": "Sistema Viário e Logradouros de São Roque",
                    "legenda_oficial": f"Logradouro: {nome_via_clean}",
                    "tipo_via": row.get("tipo_via"),
                    "superficie": row.get("superficie"),
                    "velocidade_max": row.get("velocidade_max"),
                    "bairros": set(),
                    "distritos": set(),
                    "zonas_incidentes": set(),
                    "solos_predominantes": set(),
                    "inside_apa": False,
                    "coordenadas_referencia": {
                        "lat": None,
                        "lng": None
                    },
                    "obras_proximas": []
                }

            via_obj = vias_agregadas[via_key]
            
            if via_obj["coordenadas_referencia"]["lat"] is None:
                c = geom.centroid
                via_obj["coordenadas_referencia"]["lat"] = round(c.y, 5)
                via_obj["coordenadas_referencia"]["lng"] = round(c.x, 5)

            bairro_prop = row.get("bairro")
            if bairro_prop:
                via_obj["bairros"].add(str(bairro_prop).strip())

            if apa_poly is not None and not via_obj["inside_apa"]:
                if geom.intersects(apa_poly):
                    via_obj["inside_apa"] = True

            if gdf_dist is not None:
                pt_sample = geom.centroid
                for _, drow in gdf_dist.iterrows():
                    if drow.geometry.contains(pt_sample):
                        d_nome = drow.get("distrito") or drow.get("nome")
                        via_obj["distritos"].add(d_nome.replace("Distrito de ", ""))
                        break

            if gdf_zone is not None:
                pt_sample = geom.centroid
                for _, zrow in gdf_zone.iterrows():
                    if zrow.geometry.contains(pt_sample):
                        sigla = zrow.get("sigla") or zrow.get("zona")
                        denominacao = zrow.get("denominacao") or sigla
                        if sigla:
                            via_obj["zonas_incidentes"].add(f"{sigla} ({denominacao})")
                        break

            if gdf_ped is not None:
                pt_sample = geom.centroid
                for _, prow in gdf_ped.iterrows():
                    if prow.geometry.contains(pt_sample):
                        macro = prow.get("macroclasse") or prow.get("codigo_classe")
                        if macro:
                            via_obj["solos_predominantes"].add(macro)
                        break

        # Cruzar ruas com as 22 obras estruturantes da Carta XIII
        for via_key, via_obj in vias_agregadas.items():
            ref_lat = via_obj["coordenadas_referencia"]["lat"]
            ref_lng = via_obj["coordenadas_referencia"]["lng"]
            if ref_lat and ref_lng:
                pt_via = Point(ref_lng, ref_lat)
                for obra_key, obra_obj in graph["obras_estruturantes_2026"].items():
                    olat = obra_obj.get("lat")
                    olng = obra_obj.get("lng")
                    if olat and olng:
                        pt_obra = Point(olng, olat)
                        dist_km = pt_via.distance(pt_obra) * 111.0
                        if dist_km <= 2.5:
                            via_obj["obras_proximas"].append({
                                "codigo": obra_obj["codigo"],
                                "nome": obra_obj["nome"],
                                "distancia_km": round(dist_km, 2)
                            })

            via_obj["bairros"] = sorted(list(via_obj["bairros"]))
            via_obj["distritos"] = sorted(list(via_obj["distritos"]))
            via_obj["zonas_incidentes"] = sorted(list(via_obj["zonas_incidentes"]))
            via_obj["solos_predominantes"] = sorted(list(via_obj["solos_predominantes"]))
            
            graph["logradouros"][via_key] = via_obj

        print(f"[*] Total de logradouros unificados e topologicamente enriquecidos: {len(graph['logradouros'])} vias.")

    # 5. Cruzamento de Zonas com Distritos, Vias e Obras
    print("\n[*] Cruzando Zonas de Uso com Vias e Obras...")
    for z_key, z_obj in graph["zonas_2006"].items():
        sigla = z_obj["sigla"]
        vias_na_zona = []
        distritos_na_zona = set()
        for v_key, v_obj in graph["logradouros"].items():
            for z_inc in v_obj["zonas_incidentes"]:
                if sigla in z_inc:
                    vias_na_zona.append(v_obj["nome_oficial"])
                    for d in v_obj["distritos"]:
                        distritos_na_zona.add(d)
                    break
            if len(vias_na_zona) >= 30:
                break
        
        z_obj["vias_que_atravessam"] = vias_na_zona
        z_obj["distritos_onde_ocorre"] = sorted(list(distritos_na_zona))

    # 6. Vincular Demandas Comunitárias / Participação Popular
    print("\n[*] Vinculando Vetor Social (Audiências e Consultas Públicas)...")
    for dem in participacao_data:
        tema = dem.get("tema", "")
        proponente = dem.get("proponente", "")
        pedido = dem.get("pedido_principal", "")
        parecer = dem.get("posicao_tecnica_prefeitura", "")
        impacto = dem.get("impacto_territorial", "")
        full_text = f"{tema} {pedido} {parecer} {impacto}".lower()
        for d_key, d_obj in graph["distritos"].items():
            d_name = d_obj["distrito"].lower()
            if d_name in full_text or (d_name == "canguera" and ("itupararanga" in full_text or "vinho" in full_text)):
                if "demandas_populares" not in d_obj:
                    d_obj["demandas_populares"] = []
                d_obj["demandas_populares"].append({
                    "tema": tema,
                    "solicitante": proponente,
                    "pedido": pedido,
                    "parecer_tecnico": parecer,
                    "impacto_territorial": impacto
                })

    # 6.1 Ingerir Base Jurídica Completa do SQLite (221 leis, 1.709 artigos, 163 cruzamentos)
    print("\n[*] Integrando Inteligência Jurídica Completa (SQLite sao_roque_geodados.db)...")
    if os.path.exists(DB_PATH):
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()

            # A. Cruzamentos Camada x Legislação (163 regras)
            cur.execute("""
            SELECT camada_id, classe_id, norma_esfera, norma_tipo, norma_numero, norma_ano, artigo_dispositivo, grau_restricao, regra_aplicacao, conflito_ou_ponto_atencao
            FROM cruzamento_camada_legislacao
            """)
            cruzamentos_dict = {}
            for r in cur.fetchall():
                cruzamentos_dict.setdefault(r[0], []).append({
                    "classe_id": r[1],
                    "norma": f"{r[3]} nº {r[4]}/{r[5]} ({r[2]})",
                    "artigo": r[6],
                    "grau_restricao": r[7],
                    "regra": r[8],
                    "ponto_atencao": r[9]
                })

            graph["cruzamentos_camadas_leis"] = cruzamentos_dict
            print(f"  [+] {len(cruzamentos_dict)} camadas conectadas com regras jurídicas explícitas.")

            # B. Artigos Dispositivos por Norma (1.709 artigos)
            cur.execute("""
            SELECT norma_id, artigo, texto_normativo, restricao_urbanistica_ambiental, palavras_chave
            FROM artigos_dispositivos
            """)
            artigos_map = {}
            total_artigos = 0
            for r in cur.fetchall():
                artigos_map.setdefault(r[0], []).append({
                    "artigo": r[1],
                    "texto": r[2],
                    "restricao": r[3],
                    "palavras_chave": r[4]
                })
                total_artigos += 1

            # C. 221 Normas Jurídicas
            cur.execute("""
            SELECT id, esfera, tipo, numero, ano, orgao, ementa, link_oficial, camadas_competencia
            FROM normas_juridicas
            ORDER BY ano DESC, numero DESC
            """)
            normas_dict = {}
            for r in cur.fetchall():
                n_id = r[0]
                n_arts = artigos_map.get(n_id, [])
                normas_dict[n_id] = {
                    "id": n_id,
                    "esfera": r[1],
                    "tipo": r[2],
                    "numero": str(r[3]),
                    "ano": r[4],
                    "orgao": r[5],
                    "ementa": r[6],
                    "link_oficial": r[7],
                    "camadas": [c.strip() for c in (r[8] or "").split(",") if c.strip()],
                    "total_artigos": len(n_arts),
                    "artigos": n_arts[:10]
                }

            graph["legislacao_territorial"] = {
                "total_normas": len(normas_dict),
                "total_artigos": total_artigos,
                "total_cruzamentos": sum(len(v) for v in cruzamentos_dict.values()),
                "normas": normas_dict
            }
            print(f"  [+] {len(normas_dict)} normas jurídicas e {total_artigos} artigos integrados ao Grafo Territorial.")
            conn.close()
        except Exception as e:
            print(f"  [!] Erro ao integrar base jurídica do SQLite: {e}")

    # 7. Salvar Grafo Territorial Consolidado
    sanitized = sanitize_json(graph)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(sanitized, f, ensure_ascii=False, indent=2)

    sz_kb = os.path.getsize(OUTPUT_PATH) / 1024
    print("\n" + "=" * 75)
    print(f"[OK] Grafo Territorial Multicamadas gerado com sucesso!")
    print(f"     Arquivo: {OUTPUT_PATH} ({sz_kb:.1f} KB)")
    print(f"     Distritos: {len(graph['distritos'])}")
    print(f"     Zonas 2006: {len(graph['zonas_2006'])}")
    print(f"     Cartas 2026: {len(graph['cartas_2026'])}")
    print(f"     Solos (Pedologia): {len(graph['solos_pedologia'])}")
    print(f"     Unidades Geológicas: {len(graph['unidades_geologicas'])}")
    print(f"     Logradouros (Vias): {len(graph['logradouros'])}")
    print(f"     Obras da Carta XIII: {len(graph['obras_estruturantes_2026'])}")
    print(f"     Tempo total: {time.time()-t0:.2f}s")
    print("=" * 75)

if __name__ == "__main__":
    main()
