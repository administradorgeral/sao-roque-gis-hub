#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
SÃO ROQUE GIS HUB · COMPILADOR DE DADOS DA VOZ DO BAIRRO (CÂMARA & MORADORES)
===============================================================================
Gera o arquivo otimizado 'data/voz_do_bairro_resumo.json' cruzando:
 1. Banco Real EPROCLEG da Câmara Municipal (22.468 proposições com data/hora,
    autor, tema, íntegra e URL auditável).
 2. 11 Perfis Regionais com centroides, raios e palavras-chave.
 3. Sugestões dos Cidadãos no Plano Diretor (Audiências Públicas 2024-2026)
    com status da Prefeitura e respostas na Minuta 2026.
===============================================================================
"""

import json
import os
import sqlite3
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "camara_eprocleg_sao_roque.db")
PART_JSON_PATH = os.path.join(BASE_DIR, "data", "participacao_cidada_camara_clima.json")
OUTPUT_JSON_PATH = os.path.join(BASE_DIR, "data", "voz_do_bairro_resumo.json")

# Dicionário Amigável de Macrotemas Legislativos
TEMAS_LABELS = {
    "ZELADORIA_VIARIA_ASFALTO": "Pavimentação, Tapa-Buraco e Asfalto",
    "GESTAO_ADMIN_EXPEDIENTE": "Gestão Administrativa e Expediente",
    "TRANSITO_MOBILIDADE_CALCADAS": "Trânsito, Mobilidade, Calçadas e Abrigos",
    "LIMPEZA_ROCADA_LIXO_ECOPONTO": "Limpeza Pública, Roçada e Ecopontos",
    "ILUMINACAO_ENERGIA_CPFL": "Iluminação Pública e Rede Elétrica",
    "SAUDE_EDUCACAO_ASSISTENCIA": "Saúde (Postos/UPA) e Educação (Escolas/Creches)",
    "LAZER_ESPORTE_CULTURA_TURISMO": "Praças, Lazer, Esporte e Turismo",
    "DRENAGEM_ENCHENTE_CORREGOS": "Drenagem Pluvial, Enchentes e Córregos",
    "AGUA_ESGOTO_SABESP_POCO": "Saneamento Básico, Esgoto e Sabesp",
    "MEIO_AMBIENTE_ZONEAMENTO_FISCALIZACAO": "Meio Ambiente, Zoneamento e Fiscalização",
    "SEGURANCA_GCM_MONITORAMENTO": "Segurança Pública, GCM e Câmeras",
    "OUTROS": "Outras Matérias Municipais"
}

def main():
    print("[Voz do Bairro] Iniciando compilação do índice de inteligência comunitária...")
    if not os.path.exists(DB_PATH):
        print(f"[ERRO] Banco {DB_PATH} não encontrado!")
        sys.exit(1)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # 1. Carrega perfis regionais e audiências públicas
    part_data = {}
    if os.path.exists(PART_JSON_PATH):
        with open(PART_JSON_PATH, "r", encoding="utf-8") as f:
            part_data = json.load(f)

    perfis_regionais_raw = part_data.get("pesquisa_camara_municipal", {}).get("perfis_regionais", [])
    pedidos_moradores_raw = part_data.get("pedidos_moradores_plano_diretor", {}).get("pedidos_georreferenciados", [])
    pedidos_gerais = part_data.get("pedidos_moradores_plano_diretor", {}).get("pedidos_gerais_municipio", [])

    total_proposicoes = cur.execute("SELECT COUNT(*) FROM proposicoes_eprocleg").fetchone()[0]
    total_geolocalizadas = cur.execute("SELECT COUNT(*) FROM proposicoes_eprocleg WHERE latitude IS NOT NULL AND longitude IS NOT NULL").fetchone()[0]

    print(f"[Voz do Bairro] Total de proposições no EPROCLEG: {total_proposicoes}")
    print(f"[Voz do Bairro] Proposições geolocalizadas: {total_geolocalizadas}")

    # 2. Compila estatísticas consolidadas por região
    perfis_compilados = []
    for pf in perfis_regionais_raw:
        reg_id = pf.get("id")
        
        # Total da região
        tot_reg = cur.execute(
            "SELECT COUNT(*) FROM proposicoes_eprocleg WHERE regiao_id = ? OR regioes_json LIKE ?",
            (reg_id, f'%"{reg_id}"%')
        ).fetchone()[0]

        # Breakdown de classificações
        rows_class = cur.execute(
            """
            SELECT classificacao_nome, COUNT(*) as qtd
            FROM proposicoes_eprocleg
            WHERE regiao_id = ? OR regioes_json LIKE ?
            GROUP BY classificacao_nome
            ORDER BY qtd DESC
            """,
            (reg_id, f'%"{reg_id}"%')
        ).fetchall()

        indicacoes = 0
        requerimentos = 0
        pls = 0
        outras = 0
        for r in rows_class:
            c_nom = (r["classificacao_nome"] or "").upper()
            qtd = r["qtd"]
            if "INDICAÇÃO" in c_nom or "INDICACAO" in c_nom:
                indicacoes += qtd
            elif "REQUERIMENTO" in c_nom:
                requerimentos += qtd
            elif "PROJETO DE LEI" in c_nom:
                pls += qtd
            else:
                outras += qtd

        # Top temas da região
        rows_temas = cur.execute(
            """
            SELECT tema_principal, COUNT(*) as qtd
            FROM proposicoes_eprocleg
            WHERE (regiao_id = ? OR regioes_json LIKE ?) AND tema_principal IS NOT NULL AND tema_principal != ''
            GROUP BY tema_principal
            ORDER BY qtd DESC
            LIMIT 5
            """,
            (reg_id, f'%"{reg_id}"%')
        ).fetchall()

        temas_rank = []
        for rt in rows_temas:
            t_id = rt["tema_principal"]
            qtd = rt["qtd"]
            pct = round((qtd / tot_reg * 100.0), 1) if tot_reg > 0 else 0.0
            temas_rank.append({
                "tema_id": t_id,
                "tema_nome": TEMAS_LABELS.get(t_id, t_id.replace("_", " ").title()),
                "quantidade": qtd,
                "percentual": pct
            })

        # Distribuição temporal recente por ano
        rows_anos = cur.execute(
            """
            SELECT ano_documento, COUNT(*) as qtd
            FROM proposicoes_eprocleg
            WHERE (regiao_id = ? OR regioes_json LIKE ?) AND ano_documento >= 2017
            GROUP BY ano_documento
            ORDER BY ano_documento ASC
            """,
            (reg_id, f'%"{reg_id}"%')
        ).fetchall()
        serie_temporal = {str(r["ano_documento"]): r["qtd"] for r in rows_anos}

        perfis_compilados.append({
            "id": reg_id,
            "nome_regiao": pf.get("nome_regiao"),
            "centroide_lat": pf.get("centroide_lat"),
            "centroide_lon": pf.get("centroide_lon"),
            "raio_m": pf.get("raio_m"),
            "palavras_chave": pf.get("palavras_chave", []),
            "estatisticas": {
                "total_proposicoes": tot_reg,
                "indicacoes": indicacoes,
                "requerimentos": requerimentos,
                "projetos_de_lei": pls,
                "outras": outras,
                "temas_ranking": temas_rank,
                "serie_temporal": serie_temporal
            }
        })

    # 3. Compila todas as proposições geolocalizadas (para busca por raio de 1.800m)
    rows_geo = cur.execute(
        """
        SELECT id, titulo, classificacao_nome, nro_documento, ano_documento,
               nro_protocolo, data_protocolo, descricao, autor_principal,
               tema_principal, regiao_id, latitude, longitude, url_eprocleg
        FROM proposicoes_eprocleg
        WHERE latitude IS NOT NULL AND longitude IS NOT NULL
        ORDER BY ano_documento DESC, data_protocolo DESC
        """
    ).fetchall()

    proposicoes_geo = []
    for rg in rows_geo:
        dt_raw = rg["data_protocolo"] or ""
        # Formata dia e hora
        dt_formatada = ""
        hora_formatada = ""
        if "T" in dt_raw:
            parts = dt_raw.split("T")
            dt_formatada = parts[0]
            hora_formatada = parts[1][:5] if len(parts) > 1 else ""
        elif len(dt_raw) >= 10:
            dt_formatada = dt_raw[:10]

        proposicoes_geo.append({
            "id": rg["id"],
            "titulo": rg["titulo"],
            "classificacao": rg["classificacao_nome"],
            "nro_documento": rg["nro_documento"],
            "ano": rg["ano_documento"],
            "nro_protocolo": rg["nro_protocolo"],
            "data_iso": dt_raw,
            "data_formatada": dt_formatada,
            "hora_formatada": hora_formatada,
            "autor": (rg["autor_principal"] or "Câmara Municipal").strip(),
            "tema_id": rg["tema_principal"],
            "tema_nome": TEMAS_LABELS.get(rg["tema_principal"], rg["tema_principal"]),
            "regiao_id": rg["regiao_id"],
            "descricao_completa": (rg["descricao"] or "").strip(),
            "descricao_resumida": " ".join((rg["descricao"] or "").split())[:240],
            "lat": round(float(rg["latitude"]), 6),
            "lng": round(float(rg["longitude"]), 6),
            "url_eprocleg": rg["url_eprocleg"]
        })

    print(f"[Voz do Bairro] Processadas {len(proposicoes_geo)} proposições com coordenadas GPS.")

    # 4. Estrutura final consolidada
    payload = {
        "metadata": {
            "fonte_primaria": "Câmara Municipal de São Roque (EPROCLEG)",
            "fonte_secundaria": "Audiências Públicas do Plano Diretor (2024–2026)",
            "total_proposicoes_banco": total_proposicoes,
            "total_geolocalizadas": len(proposicoes_geo),
            "total_perfis_regionais": len(perfis_compilados),
            "total_pedidos_audiencias": len(pedidos_moradores_raw),
            "periodo_cobertura": "2017–2026",
            "gerado_em": "2026-11-16T00:10:00-03:00"
        },
        "perfis_regionais": perfis_compilados,
        "pedidos_audiencias_publicas": pedidos_moradores_raw,
        "pedidos_gerais_municipio": pedidos_gerais,
        "proposicoes_geolocalizadas": proposicoes_geo
    }

    with open(OUTPUT_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    sz_kb = os.path.getsize(OUTPUT_JSON_PATH) / 1024
    print(f"[Voz do Bairro] Arquivo gerado com sucesso em '{OUTPUT_JSON_PATH}' ({sz_kb:.1f} KB)")

if __name__ == "__main__":
    main()
