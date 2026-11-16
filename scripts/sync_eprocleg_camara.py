#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
SÃO ROQUE GIS HUB · SINCRONIZAÇÃO DA CÂMARA MUNICIPAL (EPROCLEG / open-data-leg)
===============================================================================
Execução: python scripts/sync_eprocleg_camara.py [--anos 2017,2026] [--limite N]
Agendamento sugerido: diário

Fonte oficial (API pública GraphQL do portal legislativo):
  POST https://legislativo.camarasaoroque.sp.gov.br/api/open-data-leg/public/graphql
  headers: id-cliente: Y21zYW9yb3F1ZQ==  |  id-tenant: cmsaoroque

Campos reais mapeados: processo { id descricao titulo nroDocumento anoDocumento
nroProcesso anoProcesso nroProtocolo dataProtocolo cadastro nroProcesso
classificacao { nome } autores { nome } latitude longitude dataPublicacao }

Fluxo:
  1. pagina todas as proposições do ano mais recente até o mais antigo desejado;
  2. faz upsert em data/camara_eprocleg_sao_roque.db (mantendo GPS e região já
     geocodificados, quando existirem);
  3. recompila data/voz_do_bairro_resumo.json (build_community_voice_index.py).
===============================================================================
"""

import argparse
import datetime
import json
import os
import sqlite3
import subprocess
import sys
import time
import unicodedata
import urllib.error
import urllib.request

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(ROOT_DIR, "data", "camara_eprocleg_sao_roque.db")
COMPILER_SCRIPT = os.path.join(ROOT_DIR, "scripts", "build_community_voice_index.py")

API = "https://legislativo.camarasaoroque.sp.gov.br/api/open-data-leg/public/graphql"
PAGINA = "https://legislativo.camarasaoroque.sp.gov.br/portal-legislativo/proposicoes/detalhe/{id}?cliente=cmsaoroque"
HEADERS = {
    "User-Agent": "SaoRoqueGISHub/2.0 (Territorial Intelligence Ingestion)",
    "Content-Type": "application/json",
    "Accept": "application/json",
    "id-cliente": "Y21zYW9yb3F1ZQ==",
    "id-tenant": "cmsaoroque",
}

# Macrotemas (mantidos em sincronia com build_community_voice_index.py)
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
    "RISCO_ENCOSTA_MURO_DEFESA_CIVIL": "Risco de Encosta, Muros e Defesa Civil",
    "OUTROS": "Outras Matérias Municipais",
}

TEMA_KEYWORDS = [
    ("ZELADORIA_VIARIA_ASFALTO", ("tapa-buraco", "tapa buraco", "asfalto", "pavimenta", "recape", "buraco", "sarjeta", "guia", "calcamento", "calçamento")),
    ("TRANSITO_MOBILIDADE_CALCADAS", ("transito", "mobilidade", "calcada", "semaforo", "faixa de pedestre", "estacionamento", "lombada", "abrigo", "rotatoria")),
    ("LIMPEZA_ROCADA_LIXO_ECOPONTO", ("limpeza", "rocada", "lixo", "entulho", "ecoponto", "capina", "coleta", "varricao")),
    ("ILUMINACAO_ENERGIA_CPFL", ("iluminacao", "lampada", "poste", "energia", "cpfl", "fiacao", "luminaria")),
    ("SAUDE_EDUCACAO_ASSISTENCIA", ("saude", "upa", "posto de saude", "creche", "escola", "educacao", "medico", "vacina", "ubs", "hospital", "assistencia social")),
    ("LAZER_ESPORTE_CULTURA_TURISMO", ("praca", "lazer", "esporte", "quadra", "cultura", "turismo", "parque", "playground", "evento")),
    ("DRENAGEM_ENCHENTE_CORREGOS", ("drenagem", "enchente", "alagamento", "corrego", "galeria", "boca de lobo", "chuva", "piscinao")),
    ("AGUA_ESGOTO_SABESP_POCO", ("esgoto", "sabesp", "agua", "poco artesiano", "vazamento", "saneamento", "fossa")),
    ("MEIO_AMBIENTE_ZONEAMENTO_FISCALIZACAO", ("meio ambiente", "zoneamento", "fiscalizacao", "desmatamento", "poda", "arvore", "plano diretor", "lei complementar")),
    ("SEGURANCA_GCM_MONITORAMENTO", ("seguranca", "gcm", "guarda municipal", "camera", "monitoramento", "vigilancia")),
    ("RISCO_ENCOSTA_MURO_DEFESA_CIVIL", ("encosta", "deslizamento", "muro", "defesa civil", "risco", "erosao", "voçoroca", "vocoroca")),
]

QUERY = """
query Proposicoes($page: Int!, $size: Int!, $filters: [ProcessoLegislativoFilterInput!]) {
  proposicoes(page: $page, size: $size, filters: $filters) {
    id
    processo {
      id
      descricao
      titulo
      nroDocumento
      anoDocumento
      nroProcesso
      anoProcesso
      nroProtocolo
      dataProtocolo
      dataPublicacao
      cadastro
      classificacao { id descricao }
      autores { nome }
      latitude
      longitude
    }
  }
}
"""


def norm(text):
    if not text:
        return ""
    t = unicodedata.normalize("NFD", str(text))
    return "".join(c for c in t if unicodedata.category(c) != "Mn").lower()


def classificar_tema(*textos):
    alvo = norm(" ".join(t for t in textos if t))
    for tema, palavras in TEMA_KEYWORDS:
        if any(norm(p) in alvo for p in palavras):
            return tema
    return "OUTROS"


def gql(page, size, ano, tentativas=3):
    body = json.dumps({
        "query": QUERY,
        "variables": {
            "page": page,
            "size": size,
            "filters": [{"key": "ANO", "value": f"[{ano},{ano}]"}],
        },
    }).encode("utf-8")
    for tentativa in range(tentativas):
        try:
            req = urllib.request.Request(API, data=body, headers=HEADERS, method="POST")
            with urllib.request.urlopen(req, timeout=120) as resp:
                dados = json.loads(resp.read().decode("utf-8", "replace"))
            if dados.get("errors"):
                print(f"[Sync EPROCLEG] GraphQL erro (ano {ano}, pág {page}): {dados['errors'][0].get('message')}")
            return ((dados.get("data") or {}).get("proposicoes") or [])
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
            print(f"[Sync EPROCLEG] Falha na página {page} do ano {ano} (tentativa {tentativa + 1}): {e}")
            time.sleep(2 * (tentativa + 1))
    return []


def pagina_ano(ano, tamanho=50, limite=None, max_paginas=400):
    coletados = []
    for page in range(max_paginas):
        itens = gql(page, tamanho, ano)
        if not itens:
            break
        coletados.extend(itens)
        print(f"[Sync EPROCLEG] {ano} pág {page + 1}: +{len(itens)} (total {len(coletados)})")
        if len(itens) < tamanho or (limite and len(coletados) >= limite):
            break
        time.sleep(0.4)
    return coletados[:limite] if limite else coletados


def ensure_columns(conn):
    cur = conn.cursor()
    existentes = {c[1] for c in cur.execute("PRAGMA table_info(proposicoes_eprocleg)")}
    for col, tipo in (
        ("coletado_em", "TEXT"),
        ("status_tramitacao", "TEXT"),
        ("data_publicacao", "TEXT"),
        ("fonte", "TEXT"),
        ("tema_nome", "TEXT"),
    ):
        if col not in existentes:
            cur.execute(f"ALTER TABLE proposicoes_eprocleg ADD COLUMN {col} {tipo}")
    conn.commit()


def upsert(conn, itens):
    cur = conn.cursor()
    inseridos = atualizados = 0
    agora = datetime.datetime.now().isoformat(timespec="seconds")

    for it in itens:
        proc = it.get("processo") or {}
        doc_id = proc.get("id") or it.get("id")
        if not doc_id:
            continue

        ementa = (proc.get("descricao") or "").strip()
        titulo = (proc.get("titulo") or "").strip() or f"Processo {doc_id}"
        autores = proc.get("autores") or []
        autor = "; ".join(a.get("nome") for a in autores if a.get("nome")) or "Câmara Municipal"
        classificacao = (proc.get("classificacao") or {}).get("descricao") or "Proposição"
        tema = classificar_tema(titulo, ementa, classificacao)
        data_protocolo = proc.get("dataProtocolo") or proc.get("cadastro") or ""
        ano = proc.get("anoDocumento") or (int(data_protocolo[:4]) if data_protocolo[:4].isdigit() else None)
        latitude = proc.get("latitude")
        longitude = proc.get("longitude")

        existente = cur.execute(
            "SELECT id, regiao_id, latitude, longitude FROM proposicoes_eprocleg WHERE id = ?", (doc_id,)
        ).fetchone()

        valores = (
            proc.get("nroDocumento") or proc.get("nroProtocolo"),
            ano,
            data_protocolo,
            titulo,
            classificacao,
            ementa,
            autor,
            tema,
            TEMAS_LABELS.get(tema, tema),
            PAGINA.format(id=doc_id),
            agora,
            None,
            proc.get("dataPublicacao"),
            "open-data-leg/graphql",
        )

        if existente:
            # Não sobrescreve coordenadas nem região já geocodificadas
            novo_lat = existente["latitude"] if existente["latitude"] is not None else latitude
            novo_lng = existente["longitude"] if existente["longitude"] is not None else longitude
            cur.execute(
                """UPDATE proposicoes_eprocleg SET nro_documento=?, ano_documento=?, data_protocolo=?,
                   titulo=?, classificacao_nome=?, descricao=?, autor_principal=?, tema_principal=?,
                   tema_nome=?, url_eprocleg=?, coletado_em=?, status_tramitacao=?, data_publicacao=?,
                   fonte=?, latitude=?, longitude=? WHERE id=?""",
                valores + (novo_lat, novo_lng, doc_id),
            )
            atualizados += 1
        else:
            cur.execute(
                """INSERT INTO proposicoes_eprocleg
                   (nro_documento, ano_documento, data_protocolo, titulo, classificacao_nome, descricao,
                    autor_principal, tema_principal, tema_nome, url_eprocleg, coletado_em,
                    status_tramitacao, data_publicacao, fonte, latitude, longitude, id)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                valores + (latitude, longitude, doc_id),
            )
            inseridos += 1

    conn.commit()
    return inseridos, atualizados


def main():
    hoje = datetime.date.today().year
    parser = argparse.ArgumentParser()
    parser.add_argument("--anos", default=f"2017,{hoje}", help="intervalo de anos, ex.: 2017,2026")
    parser.add_argument("--limite", type=int, default=None, help="limite de registros por ano")
    parser.add_argument("--sem-compilar", action="store_true")
    args = parser.parse_args()

    ini, fim = (int(x) for x in args.anos.split(","))
    print(f"[Sync EPROCLEG] Sincronizando proposições {ini}–{fim} via API pública do portal legislativo.")

    total_inseridos = total_atualizados = total_itens = 0
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    ensure_columns(conn)

    for ano in range(fim, ini - 1, -1):
        itens = pagina_ano(ano, limite=args.limite)
        if not itens:
            print(f"[Sync EPROCLEG] {ano}: nenhuma proposição retornada.")
            continue
        ins, atu = upsert(conn, itens)
        total_itens += len(itens)
        total_inseridos += ins
        total_atualizados += atu
        print(f"[Sync EPROCLEG] {ano}: {len(itens)} recebidas | {ins} novas | {atu} atualizadas")

    total_banco = conn.execute("SELECT COUNT(*) FROM proposicoes_eprocleg").fetchone()[0]
    conn.close()
    print(f"[Sync EPROCLEG] Concluído: {total_itens} recebidas, {total_inseridos} novas, "
          f"{total_atualizados} atualizadas, {total_banco} no banco.")

    if not args.sem_compilar:
        print("[Sync EPROCLEG] Recompilando índice da Voz do Bairro...")
        res = subprocess.run([sys.executable, COMPILER_SCRIPT], capture_output=True, text=True, encoding="utf-8")
        print(res.stdout.strip() or res.stderr.strip())
        if res.returncode != 0:
            sys.exit(res.returncode)


if __name__ == "__main__":
    main()
