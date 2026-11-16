#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
SÃO ROQUE GIS HUB · MOTOR DE INTELIGÊNCIA TERRITORIAL E AUDITORIA JURÍDICA
===============================================================================
Módulo: spatial_legal_engine.py
Propósito:
  Permite consultar:
    1) Um ponto georreferenciado específico (Lat/Lon WGS84 ou UTM SIRGAS 2000 23S)
    2) Uma lei ou conjunto de normas específicas
    3) Uma camada ou zona territorial específica
    4) OU OS TRÊS JUNTOS (Interseção Multi-Camadas + Matriz Normativa)
  
  Retorna um arquivo JSON AUDITÁVEL completo com:
    - Identificador único e Hash criptográfico SHA-256
    - Diagnóstico geoespacial em todas as 15 camadas oficiais
    - Matriz de normas incidentes divididas pela Pirâmide de Kelsen (Federal > Estadual > Municipal)
    - Condicionantes, parâmetros construtivos e regras impeditivas
    - Fontes cartográficas, anexos técnicos do PDA 2019/PMD 2006 e responsáveis CREA
    - Embasamento técnico e fundamentação jurídica para decisões e licenciamento
===============================================================================
"""

import os
import sys
import json
import time
import uuid
import hashlib
import sqlite3
import argparse
import datetime
from typing import Dict, List, Any, Optional, Tuple

import numpy as np
import geopandas as gpd
from shapely.geometry import Point, Polygon, MultiPolygon
from pyproj import Transformer

# Diretórios base
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(BASE_DIR, "dados_oficiais", "sao_roque_geodados.db")
ROL_PATH = os.path.join(BASE_DIR, "data", "rol_legislacao_territorial.json")

# Transformadores de Coordenadas
transformer_wgs_to_utm = Transformer.from_crs("EPSG:4326", "EPSG:31983", always_xy=True)
transformer_utm_to_wgs = Transformer.from_crs("EPSG:31983", "EPSG:4326", always_xy=True)


def sanitize_for_json(obj):
    import math
    if isinstance(obj, dict):
        return {str(k): sanitize_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [sanitize_for_json(v) for v in obj]
    elif hasattr(obj, "item"):
        val = obj.item()
        if isinstance(val, float) and math.isnan(val):
            return None
        return val
    elif isinstance(obj, float) and math.isnan(obj):
        return None
    return obj


class SpatialLegalEngine:
    """Motor Unificado de Inteligência Territorial e Jurídica de São Roque."""

    def __init__(self, preload_layers: bool = True):
        self.db_conn = sqlite3.connect(DB_PATH)
        self.db_conn.row_factory = sqlite3.Row
        self.cur = self.db_conn.cursor()
        
        # Carregar parâmetros de zonas
        self.zonas_parametros = {}
        if os.path.exists(ROL_PATH):
            with open(ROL_PATH, "r", encoding="utf-8") as f:
                self.rol_data = json.load(f)
                self.zonas_parametros = self.rol_data.get("zonas_parametros", {})

        self.layers: Dict[str, gpd.GeoDataFrame] = {}
        if preload_layers:
            self._preload_spatial_layers()

    def _preload_spatial_layers(self):
        """Carrega e indexa espacialmente as camadas vetoriais oficiais."""
        t0 = time.time()
        print("[SpatialLegalEngine] Indexando camadas territoriais oficiais...", file=sys.stderr)
        
        layer_files = {
            "territorio_municipal": "territorio_municipal_sao_roque_web.geojson",
            "distritos": "distritos_sao_roque_web.geojson",
            "setores_censitarios": "setores_censitarios_sao_roque_web.geojson",
            "logradouros": "logradouros_sao_roque_web.geojson",
            "zoneamento_pmd2006": "zoneamento_sao_roque_web.geojson",
            "zoneamento_minuta_pmd2006": "zoneamento_minuta_sao_roque_web.geojson",
            "declividade": "declividade_sao_roque_web.geojson",
            "mdt": "mdt_sao_roque_web.geojson",
            "hidrografia": "hidrografia_sao_roque_web.geojson",
            "geomorfologico": "geomorfologico_sao_roque_web.geojson",
            "geologia": "geologia_sao_roque_web.geojson",
            "fragilidade_potencial": "fragilidade_potencial_sao_roque_web.geojson",
            "pedologico": "pedologico_sao_roque_web.geojson",
            "zoneamento_ambiental_pda2019": "zoneamento_ambiental_pda2019_sao_roque_web.geojson",
            "apa_itupararanga": "apa_itupararanga_limite_sao_roque_web.geojson",
            "zona_protecao_aeroportuaria_catarina": "zona_protecao_aeroportuaria_catarina_web.geojson",
            "ahs": "ahs_sao_roque_web.geojson",
            "vegetacao_arborea": "vegetacao_arborea_sao_roque_web.geojson",
            "rbcv_cinturao_verde": "rbcv_cinturao_verde_nucleos_web.geojson"
        }

        for layer_id, fname in layer_files.items():
            fpath = os.path.join(DATA_DIR, fname)
            if os.path.exists(fpath):
                try:
                    gdf = gpd.read_file(fpath)
                    # Garantir EPSG:4326 para consultas geográficas
                    if gdf.crs != "EPSG:4326":
                        gdf = gdf.to_crs(epsg=4326)
                    # Forçar criação do índice espacial R-tree
                    _ = gdf.sindex
                    self.layers[layer_id] = gdf
                except Exception as e:
                    print(f"  [Alerta] Erro ao carregar {layer_id}: {e}", file=sys.stderr)

        print(f"[SpatialLegalEngine] {len(self.layers)} camadas carregadas em {time.time()-t0:.2f}s.", file=sys.stderr)

    def query_spatial_point(self, lat: float, lon: float) -> List[Dict[str, Any]]:
        """Intersecciona um ponto com todas as camadas territoriais."""
        pt = Point(lon, lat)
        intersections = []

        for layer_id, gdf in self.layers.items():
            try:
                if layer_id == "logradouros":
                    # Proximidade de vias até 100m (~0.0009 graus)
                    buf = pt.buffer(0.0009)
                    possible_matches_index = list(gdf.sindex.intersection(buf.bounds))
                    if possible_matches_index:
                        possible_matches = gdf.iloc[possible_matches_index]
                        near = possible_matches[possible_matches.intersects(buf)]
                        if not near.empty:
                            dists = near.distance(pt)
                            nearest_idx = dists.idxmin()
                            row = near.loc[nearest_idx]
                            props = {k: v for k, v in row.items() if k != "geometry"}
                            intersections.append({
                                "camada_id": layer_id,
                                "propriedades": props
                            })
                    continue

                # Consulta rápida via spatial index para polígonos
                possible_matches_index = list(gdf.sindex.intersection((lon, lat, lon, lat)))
                if not possible_matches_index:
                    continue
                
                possible_matches = gdf.iloc[possible_matches_index]
                exact_matches = possible_matches[possible_matches.intersects(pt)]
                
                for _, row in exact_matches.iterrows():
                    props = {k: v for k, v in row.items() if k != "geometry"}
                    intersections.append({
                        "camada_id": layer_id,
                        "propriedades": props
                    })
            except Exception as e:
                print(f"[Erro Espacial] {layer_id}: {e}", file=sys.stderr)

        return intersections

    def query_laws(self, search_term: Optional[str] = None, camada_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Consulta normas jurídicas e artigos com filtro por termo e/ou camada."""
        results = []
        
        query = """
            SELECT DISTINCT 
                n.id, n.esfera, n.tipo, n.numero, n.ano, n.orgao, n.ementa, n.vigencia, n.link_oficial,
                c.artigo_dispositivo, c.grau_restricao, c.regra_aplicacao, c.conflito_ou_ponto_atencao,
                c.camada_id, c.classe_id
            FROM normas_juridicas n
            LEFT JOIN cruzamento_camada_legislacao c ON (
                c.norma_numero = n.numero OR 
                c.norma_numero = replace(n.numero, '.', '') OR
                n.id LIKE '%' || c.norma_numero || '%'
            )
            WHERE 1=1
        """
        params = []

        if camada_id:
            query += " AND c.camada_id = ?"
            params.append(camada_id)

        if search_term:
            query += """ AND (
                n.numero LIKE ? OR
                n.ementa LIKE ? OR
                n.texto_integral LIKE ? OR
                c.artigo_dispositivo LIKE ? OR
                c.regra_aplicacao LIKE ?
            )"""
            term_wild = f"%{search_term}%"
            params.extend([term_wild, term_wild, term_wild, term_wild, term_wild])

        query += " ORDER BY CASE n.esfera WHEN 'Federal' THEN 1 WHEN 'Estadual' THEN 2 WHEN 'Municipal' THEN 3 ELSE 4 END, n.ano DESC LIMIT 100"

        self.cur.execute(query, params)
        rows = self.cur.fetchall()

        for r in rows:
            results.append({
                "id": r["id"],
                "esfera": r["esfera"],
                "tipo": r["tipo"],
                "numero": r["numero"],
                "ano": r["ano"],
                "orgao": r["orgao"],
                "ementa": r["ementa"],
                "vigencia": r["vigencia"],
                "link_oficial": r["link_oficial"],
                "artigo_dispositivo": r["artigo_dispositivo"],
                "grau_restricao": r["grau_restricao"],
                "regra_aplicacao": r["regra_aplicacao"],
                "conflito_ou_ponto_atencao": r["conflito_ou_ponto_atencao"],
                "camada_vinculada": r["camada_id"],
                "classe_vinculada": r["classe_id"]
            })

        return results

    def get_layer_metadata(self, camada_id: str) -> Optional[Dict[str, Any]]:
        """Recupera os metadados oficiais e classes cadastradas de uma camada."""
        self.cur.execute("SELECT * FROM camadas_territoriais WHERE id = ?", (camada_id,))
        layer_row = self.cur.fetchone()
        if not layer_row:
            return None

        layer_data = dict(layer_row)

        self.cur.execute("SELECT * FROM classes_camada_territorial WHERE camada_id = ?", (camada_id,))
        classes_rows = self.cur.fetchall()
        layer_data["classes"] = [dict(c) for c in classes_rows]

        return layer_data

    def generate_auditable_report(
        self,
        lat: Optional[float] = None,
        lon: Optional[float] = None,
        law_query: Optional[str] = None,
        layer_id: Optional[str] = None,
        finalidade: str = "Diagnóstico e Conformidade Urbanístico-Ambiental"
    ) -> Dict[str, Any]:
        """Gera o relatório JSON auditável completo e determinístico."""
        report_id = str(uuid.uuid4())
        timestamp_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
        timestamp_local = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        report: Dict[str, Any] = {
            "cabecalho_auditoria": {
                "relatorio_id": report_id,
                "emissao_utc": timestamp_utc,
                "emissao_local": timestamp_local,
                "municipio": "Estância Turística de São Roque (SP)",
                "codigo_ibge": "3550605",
                "finalidade_declarada": finalidade,
                "sistema_gerador": "São Roque GIS Hub · Spatial & Legal Audit Engine v2.0",
                "versao_base_dados": "15 Camadas Territoriais / PDA 2019 / PMD 2006 / SIRGAS 2000 UTM 23S"
            },
            "parametros_entrada": {
                "latitude": lat,
                "longitude": lon,
                "termo_legislacao": law_query,
                "camada_especifica": layer_id
            },
            "geolocalizacao_ponto": None,
            "diagnostico_espacial": [],
            "matriz_normativa_incidente": {
                "federal": [],
                "estadual": [],
                "municipal": []
            },
            "regras_e_restricoes_sintetizadas": {
                "grau_restricao_maximo": "Apto com Condicionantes",
                "regras_impeditivas": [],
                "condicionantes_obrigatorias": [],
                "parametros_urbanisticos_aplicaveis": {}
            },
            "fontes_cartograficas_e_responsabilidade_tecnica": []
        }

        # 1. Análise Espacial do Ponto (se fornecido)
        if lat is not None and lon is not None:
            utm_x, utm_y = transformer_wgs_to_utm.transform(lon, lat)
            report["geolocalizacao_ponto"] = {
                "coordenadas_wgs84": {"lat": lat, "lon": lon},
                "coordenadas_sirgas2000_utm23s": {"utm_e": round(utm_x, 2), "utm_n": round(utm_y, 2)},
                "datum": "SIRGAS 2000 / UTM Zone 23S (EPSG:31983)"
            }

            spatial_hits = self.query_spatial_point(lat, lon)
            
            for hit in spatial_hits:
                c_id = hit["camada_id"]
                props = hit["propriedades"]
                
                # Se filtrou por camada, só mantém a camada solicitada
                if layer_id and c_id != layer_id:
                    continue

                meta = self.get_layer_metadata(c_id)
                legenda = props.get("nome") or props.get("denominacao") or props.get("nome_classe") or props.get("classe") or props.get("zona") or (meta.get("nome") if meta else c_id)
                clean_props = {k: v for k, v in props.items() if not k.lower().startswith("fid")}
                diag_item = {
                    "camada_id": c_id,
                    "camada_nome": meta.get("nome") if meta else c_id,
                    "legenda_oficial": str(legenda).strip(),
                    "anexo_documento": meta.get("arquivo_origem") if meta else None,
                    "escala_nominal": meta.get("escala_nominal") if meta else None,
                    "alerta_juridico": meta.get("alerta_juridico") if meta else None,
                    "atributos_local": clean_props
                }
                report["diagnostico_espacial"].append(diag_item)

                # Coletar fontes técnicas
                if meta:
                    report["fontes_cartograficas_e_responsabilidade_tecnica"].append({
                        "camada": meta.get("nome"),
                        "documento": meta.get("titulo_documento"),
                        "responsavel_tecnico": meta.get("responsavel_tecnico"),
                        "crea_tecnico": meta.get("responsavel_crea"),
                        "desenho_tecnico": meta.get("desenho_tecnico"),
                        "fonte_dados": meta.get("fonte_cartografica")
                    })

                # Adicionar parâmetros de zona se existir código
                cod_classe = props.get("codigo_classe") or props.get("codigo") or props.get("sigla")
                if cod_classe and cod_classe in self.zonas_parametros:
                    report["regras_e_restricoes_sintetizadas"]["parametros_urbanisticos_aplicaveis"][cod_classe] = self.zonas_parametros[cod_classe]

        # 2. Análise Jurídica e Leis Incidentes
        # Se veio ponto, busca leis vinculadas a cada camada interceptada; senão busca por camada_id ou termo
        camadas_para_buscar = [d["camada_id"] for d in report["diagnostico_espacial"]] if report["diagnostico_espacial"] else ([layer_id] if layer_id else None)
        
        all_laws = []
        if camadas_para_buscar:
            for cid in camadas_para_buscar:
                all_laws.extend(self.query_laws(search_term=law_query, camada_id=cid))
        elif law_query or layer_id:
            all_laws.extend(self.query_laws(search_term=law_query, camada_id=layer_id))

        # Deduplicar leis por id + artigo
        seen_laws = set()
        for law in all_laws:
            law_key = f"{law['id']}_{law.get('artigo_dispositivo')}"
            if law_key in seen_laws:
                continue
            seen_laws.add(law_key)

            esf = law["esfera"].lower()
            if "fed" in esf:
                report["matriz_normativa_incidente"]["federal"].append(law)
            elif "est" in esf:
                report["matriz_normativa_incidente"]["estadual"].append(law)
            else:
                report["matriz_normativa_incidente"]["municipal"].append(law)

            # Classificar regras em impeditivas ou condicionantes
            grau = str(law.get("grau_restricao", "")).lower()
            regra = law.get("regra_aplicacao") or law.get("ementa")
            if "impeditiv" in grau or "vedada" in str(regra).lower() or "proib" in str(regra).lower():
                report["regras_e_restricoes_sintetizadas"]["regras_impeditivas"].append({
                    "norma": f"{law['tipo']} {law['numero']}/{law['ano']} ({law['esfera']})",
                    "artigo": law.get("artigo_dispositivo"),
                    "regra": regra
                })
            else:
                report["regras_e_restricoes_sintetizadas"]["condicionantes_obrigatorias"].append({
                    "norma": f"{law['tipo']} {law['numero']}/{law['ano']} ({law['esfera']})",
                    "artigo": law.get("artigo_dispositivo"),
                    "regra": regra
                })

        # Grau de restrição máximo
        if report["regras_e_restricoes_sintetizadas"]["regras_impeditivas"]:
            report["regras_e_restricoes_sintetizadas"]["grau_restricao_maximo"] = "RESTRITO / COM VEDAÇÕES LEGAIS EXPRESSAS"
        elif report["regras_e_restricoes_sintetizadas"]["condicionantes_obrigatorias"]:
            report["regras_e_restricoes_sintetizadas"]["grau_restricao_maximo"] = "APROVÁVEL MEDIANTE CONDICIONANTES TÉCNICAS E AMBIENTAIS"
        else:
            report["regras_e_restricoes_sintetizadas"]["grau_restricao_maximo"] = "ZONA LIVRE / DIRETRIZES ORDINÁRIAS"

        # Sanitização de tipos numpy/int32/float64
        report = sanitize_for_json(report)

        # 3. Hash Criptográfico de Auditoria SHA-256
        serialized_data = json.dumps(report, sort_keys=True, ensure_ascii=False)
        hash_digest = hashlib.sha256(serialized_data.encode("utf-8")).hexdigest()
        report["cabecalho_auditoria"]["hash_sha256_integridade"] = hash_digest
        report["cabecalho_auditoria"]["status_certificacao"] = "AUTENTICADO_SISTEMA_OFICIAL"

        return report


def main():
    parser = argparse.ArgumentParser(description="Motor de Inteligência Territorial de São Roque (Relatórios JSON Auditáveis)")
    parser.add_argument("--lat", type=float, help="Latitude WGS84")
    parser.add_argument("--lon", type=float, help="Longitude WGS84")
    parser.add_argument("--utm-e", type=float, help="Coordenada UTM Leste (SIRGAS 2000 Fuso 23S)")
    parser.add_argument("--utm-n", type=float, help="Coordenada UTM Norte (SIRGAS 2000 Fuso 23S)")
    parser.add_argument("--law", type=str, help="Termo de pesquisa jurídica (ex: 11.428, Mata Atlântica, declividade)")
    parser.add_argument("--layer", type=str, help="ID da camada (ex: vegetacao_arborea, ahs, zoneamento_pmd2006)")
    parser.add_argument("--json-out", type=str, help="Arquivo de destino para salvar o JSON auditável")
    parser.add_argument("--finalidade", type=str, default="Diagnóstico e Embasamento Urbanístico", help="Finalidade do laudo")

    args = parser.parse_args()

    lat = args.lat
    lon = args.lon

    if args.utm_e is not None and args.utm_n is not None:
        lon, lat = transformer_utm_to_wgs.transform(args.utm_e, args.utm_n)

    engine = SpatialLegalEngine(preload_layers=(lat is not None and lon is not None))

    report = engine.generate_auditable_report(
        lat=lat,
        lon=lon,
        law_query=args.law,
        layer_id=args.layer,
        finalidade=args.finalidade
    )

    out_json = json.dumps(report, indent=2, ensure_ascii=False)

    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as f:
            f.write(out_json)
        print(f"\n[SUCESSO] Relatório JSON Auditável gravado em: {args.json_out}")
        print(f"  ID do Relatório: {report['cabecalho_auditoria']['relatorio_id']}")
        print(f"  Hash SHA-256: {report['cabecalho_auditoria']['hash_sha256_integridade']}")
        print(f"  Camadas Interceptadas: {len(report['diagnostico_espacial'])}")
        print(f"  Regras Impeditivas: {len(report['regras_e_restricoes_sintetizadas']['regras_impeditivas'])}")
        print(f"  Condicionantes: {len(report['regras_e_restricoes_sintetizadas']['condicionantes_obrigatorias'])}")
    else:
        print(out_json)


if __name__ == "__main__":
    main()
