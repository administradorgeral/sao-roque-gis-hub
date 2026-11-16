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

Além das 658 proposições com pino GPS, o arquivo agora leva:
 - 'proposicoes_por_regiao': TODAS as proposições indexadas por região
   parlamentar (com e sem GPS), para que a Seção 5 use o histórico completo;
 - 'logradouros_indexados': logradouros extraídos das ementas, com regiões
   associadas, permitindo casar protocolos pela mesma rua.
===============================================================================
"""

import datetime
import json
import os
import re
import sqlite3
import sys
import unicodedata

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(ROOT_DIR, "data", "camara_eprocleg_sao_roque.db")
PART_JSON_PATH = os.path.join(ROOT_DIR, "data", "participacao_cidada_camara_clima.json")
OUTPUT_JSON_PATH = os.path.join(ROOT_DIR, "data", "voz_do_bairro_resumo.json")

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
    "SEGURANCA_PUBLICA_GCM": "Segurança Pública, GCM e Câmeras",
    "RISCO_ENCOSTA_MURO_DEFESA_CIVIL": "Risco de Encosta, Muros e Defesa Civil",
    "OUTROS": "Outras Matérias Municipais",
}

# Extração de logradouro citado na ementa
STREET_RE = re.compile(
    r"\b(?:rua|avenida|av\.?|travessa|tv\.?|alameda|estrada|estr\.?|rodovia|rod\.?|praça|praca|largo|viela|beco)\s+"
    r"((?:[A-Za-zÀ-ÿ0-9'.\u2019\-]+\s?){1,6})",
    re.IGNORECASE,
)
STREET_STOPWORDS = {
    "de", "da", "do", "das", "dos", "e", "no", "na", "em", "para", "ao", "a", "o",
    # conector de cruzamento: "rua Pedro Vaz com a avenida Tiradentes" -> "Pedro Vaz"
    "com", "esquina", "esq", "entre", "ate", "até", "proximo", "próximo", "prox",
    "sentido", "bairro", "jd", "jardim", "vila", "rua", "avenida", "av", "travessa",
    "municipal", "municipais", "publica", "publicas", "pública", "públicas",
}
# Limite de proposições por região e de anos no catálogo único. A base completa
# fica no SQLite; o JSON é o recorte carregado pelo navegador (deve ficar <5 MB).
MAX_PROPS_PER_REGION = 120
ANOS_CATALOGO = 3
# A busca por logradouro precisa do texto da ementa; a busca por região não.
# Guardamos a ementa curta por padrão e o texto completo só quando a proposição
# cita um logradouro (logradouro_id), para não inflar o JSON baixado pelo site.


REFERENCIADOS = set()


NORM_MAP = str.maketrans({"'": "", "\u2019": "", "`": "", ".": "", "-": " "})


def norm(text):
    """Minúsculo, sem acento, sem apóstrofo/ponto (Del'Acqua -> delacqua)."""
    if not text:
        return ""
    t = unicodedata.normalize("NFD", str(text))
    t = "".join(c for c in t if unicodedata.category(c) != "Mn").lower()
    return " ".join(t.translate(NORM_MAP).split()).strip()


def fix_mojibake(text):
    """Corrige strings duplamente codificadas (UTF-8 lido como cp1252)."""
    if not text:
        return ""
    if "Ã" not in text and "Â" not in text:
        return text
    try:
        return text.encode("cp1252").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return text


def split_text(value, short_len, full_len):
    """Devolve [resumida, complemento] sem repetir caracteres no JSON."""
    if not value:
        return ["", ""]
    short = value[:short_len]
    rest = value[short_len:full_len] if len(value) > short_len else ""
    return [short, rest]


def extract_street(descricao):
    """Tenta extrair o logradouro principal da ementa (nome próprio após a sigla)."""
    if not descricao:
        return None
    for m in STREET_RE.finditer(descricao):
        raw = m.group(1).strip(" .,-")
        words = raw.split()
        kept = []
        for w in words:
            if norm(w) in STREET_STOPWORDS and kept:
                break
            kept.append(w)
            if len(kept) >= 5:
                break
        name = " ".join(kept).strip(" .,-\u2019")
        if len(norm(name)) >= 4 and norm(name) not in STREET_STOPWORDS:
            return name
    return None


def fmt_date(dt_raw):
    dt_formatada = ""
    hora_formatada = ""
    if not dt_raw:
        return dt_formatada, hora_formatada
    if "T" in dt_raw:
        parts = dt_raw.split("T")
        dt_formatada = parts[0]
        hora_formatada = parts[1][:5] if len(parts) > 1 else ""
    elif len(dt_raw) >= 10:
        dt_formatada = dt_raw[:10]
    return dt_formatada, hora_formatada


def build_proposicao(row):
    """Row -> dict compacto (arrays posicionais) usado nas buscas por região,
    logradouro e GPS. Arrays economizam ~60% do arquivo compilado."""
    dt_formatada, hora_formatada = fmt_date(row["data_protocolo"] or "")
    descricao = " ".join((fix_mojibake(row["descricao"] or "")).split())
    lat = row["latitude"]
    lng = row["longitude"]
    return {
        "id": row["id"],
        "titulo": fix_mojibake(row["titulo"] or "")[:180],
        "classificacao": fix_mojibake(row["classificacao_nome"] or ""),
        "nro_documento": row["nro_documento"],
        "ano": row["ano_documento"],
        "nro_protocolo": row["nro_protocolo"],
        "data_formatada": dt_formatada,
        "hora_formatada": hora_formatada,
        "autor": (fix_mojibake(row["autor_principal"]) or "Câmara Municipal").strip()[:70],
        "tema_id": row["tema_principal"],
        "tema_nome": TEMAS_LABELS.get(row["tema_principal"], (row["tema_principal"] or "").replace("_", " ").title()),
        "regiao_id": row["regiao_id"] or "",
        "descricao_completa": descricao[:700],
        "descricao_resumida": descricao[:240],
        "lat": round(float(lat), 6) if lat is not None else None,
        "lng": round(float(lng), 6) if lng is not None else None,
        "gps": lat is not None and lng is not None,
        "url_eprocleg": row["url_eprocleg"],
    }


def main():
    print("[Voz do Bairro] Iniciando compilação do índice de inteligência comunitária...")
    if not os.path.exists(DB_PATH):
        print(f"[ERRO] Banco {DB_PATH} não encontrado!")
        sys.exit(1)

    conn = sqlite3.connect(DB_PATH)
    conn.text_factory = lambda b: b.decode("utf-8", "replace")
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
    pedidos_moradores_raw = [
        {**p, "local_alvo": fix_mojibake(p.get("local_alvo")), "pedido_dos_moradores": fix_mojibake(p.get("pedido_dos_moradores"))}
        for p in pedidos_moradores_raw
    ]

    total_proposicoes = cur.execute("SELECT COUNT(*) FROM proposicoes_eprocleg").fetchone()[0]
    total_geolocalizadas = cur.execute(
        "SELECT COUNT(*) FROM proposicoes_eprocleg WHERE latitude IS NOT NULL AND longitude IS NOT NULL"
    ).fetchone()[0]

    print(f"[Voz do Bairro] Total de proposições no EPROCLEG: {total_proposicoes}")
    print(f"[Voz do Bairro] Proposições geolocalizadas: {total_geolocalizadas}")

    # 2. Compila estatísticas consolidadas por região
    perfis_compilados = []
    for pf in perfis_regionais_raw:
        reg_id = pf.get("id")

        # Total da região
        tot_reg = cur.execute(
            "SELECT COUNT(*) FROM proposicoes_eprocleg WHERE regiao_id = ? OR regioes_json LIKE ?",
            (reg_id, f'%"{reg_id}"%'),
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
            (reg_id, f'%"{reg_id}"%'),
        ).fetchall()

        indicacoes = requerimentos = pls = outras = 0
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
            (reg_id, f'%"{reg_id}"%'),
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
                "percentual": pct,
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
            (reg_id, f'%"{reg_id}"%'),
        ).fetchall()
        serie_temporal = {str(r["ano_documento"]): r["qtd"] for r in rows_anos}

        perfis_compilados.append({
            "id": reg_id,
            "nome_regiao": fix_mojibake(pf.get("nome_regiao")),
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
                "serie_temporal": serie_temporal,
            },
        })

    # 3. Proposições geolocalizadas (busca por raio de 1.800m)
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
    proposicoes_geo = [build_proposicao(r) for r in rows_geo]
    print(f"[Voz do Bairro] Processadas {len(proposicoes_geo)} proposições com coordenadas GPS.")

    # 4. TODAS as proposições por região (com e sem GPS) + índice de logradouros
    rows_all = cur.execute(
        """
        SELECT id, titulo, classificacao_nome, nro_documento, ano_documento,
               nro_protocolo, data_protocolo, descricao, autor_principal,
               tema_principal, regiao_id, regioes_json, latitude, longitude, url_eprocleg
        FROM proposicoes_eprocleg
        WHERE ano_documento >= ?
        ORDER BY ano_documento DESC, data_protocolo DESC
        """,
        (datetime.date.today().year - ANOS_CATALOGO + 1,),
    ).fetchall()

    # Catálogo único de proposições (cada uma aparece só uma vez no arquivo)
    catalogo = {}
    com_logradouro = set()
    ids_por_regiao = {pf["id"]: [] for pf in perfis_compilados}
    logradouros = {}

    for row in rows_all:
        prop = build_proposicao(row)
        try:
            regioes = json.loads(row["regioes_json"] or "[]")
        except (TypeError, ValueError):
            regioes = []
        if prop["regiao_id"] and prop["regiao_id"] not in regioes:
            regioes.append(prop["regiao_id"])

        street = extract_street(prop["descricao_completa"])
        if street:
            key = norm(street)
            if key not in logradouros:
                logradouros[key] = {"nome": street, "total": 0, "regioes": []}
            entry = logradouros[key]
            prop["logradouro_id"] = "log:%s" % key.replace(" ", "_")
            com_logradouro.add(prop["id"])
            if len(norm(street)) > len(norm(entry["nome"])):
                entry["nome"] = street
            entry["total"] += 1
            for reg in regioes:
                if reg and reg not in entry["regioes"]:
                    entry["regioes"].append(reg)
            # Garante que toda rua citada tenha seus protocolos no catálogo,
            # mesmo os mais antigos (fora da janela ANOS_CATALOGO).
            REFERENCIADOS.add(prop["id"])

        catalogo.setdefault(prop["id"], prop)
        for reg in regioes:
            bucket = ids_por_regiao.setdefault(reg, [])
            if len(bucket) < MAX_PROPS_PER_REGION:
                bucket.append(prop["id"])

    # Sets de ids indexados (região/logradouro) para descartar o resto do catálogo
    ids_regiao = {i for bucket in ids_por_regiao.values() for i in bucket}
    # Mesma normalização de chave usada no catálogo (str, sem .0 em ids numéricos)
    ids_gps = {str(p["id"]).replace(".0", "") for p in proposicoes_geo}
    referenciados = ids_regiao | ids_gps | com_logradouro | REFERENCIADOS
    catalogo = {i: p for i, p in catalogo.items() if i in referenciados}

    indexadas = len(catalogo)
    # 1.215 logradouros com 2+ protocolos; o restante (1 protocolo cada) só serve
    # como "árvore" de prefixos para casar a rua do ponto com o histórico.
    logradouros_indexados = {
        k: {"nome": v["nome"], "total": v["total"], "regioes": v["regioes"]}
        for k, v in logradouros.items()
        if v["total"] >= 2
    }
    logradouros_arvore = sorted(
        (v["nome"] for v in logradouros.values() if v["total"] == 1),
        key=len,
        reverse=True,
    )
    print(f"[Voz do Bairro] Proposições no catálogo (regiões + ruas + GPS): {indexadas}")
    print(f"[Voz do Bairro] Logradouros indexados: {len(logradouros_indexados)}")

    # Catálogo enxuto: sem descricao_completa (só o resumo) — o texto longo fica
    # exclusivamente em proposicoes_geolocalizadas, evitando 4 MB de duplicata.
    catalogo_enxuto = []
    for prop in catalogo.values():
        enxuto = {k: v for k, v in prop.items() if k not in ("descricao_completa", "logradouro_id")}
        catalogo_enxuto.append(enxuto)

    # 5. Estrutura final consolidada
    payload = {
        "metadata": {
            "fonte_primaria": "Câmara Municipal de São Roque (EPROCLEG)",
            "fonte_secundaria": "Audiências Públicas do Plano Diretor (2024–2026)",
            "total_proposicoes_banco": total_proposicoes,
            "total_geolocalizadas": len(proposicoes_geo),
            "total_indexadas_por_regiao": indexadas,
            "total_logradouros": len(logradouros_indexados),
            "total_logradouros_arvore": sum(1 for v in logradouros.values() if v["total"] == 1),
            "total_perfis_regionais": len(perfis_compilados),
            "total_pedidos_audiencias": len(pedidos_moradores_raw),
            "periodo_cobertura": "2017–2026",
            "gerado_em": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
        },
        "perfis_regionais": perfis_compilados,
        "pedidos_audiencias_publicas": pedidos_moradores_raw,
        "pedidos_gerais_municipio": pedidos_gerais,
        "proposicoes_geolocalizadas": proposicoes_geo,
        "proposicoes_catalogo": catalogo_enxuto,
        "proposicoes_por_regiao": ids_por_regiao,
        "logradouros_indexados": logradouros_indexados,
        "logradouros_arvore": logradouros_arvore,
    }

    with open(OUTPUT_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, separators=(",", ":"))

    sz_kb = os.path.getsize(OUTPUT_JSON_PATH) / 1024
    print(f"[Voz do Bairro] Arquivo gerado com sucesso em '{OUTPUT_JSON_PATH}' ({sz_kb:.1f} KB)")


if __name__ == "__main__":
    main()
