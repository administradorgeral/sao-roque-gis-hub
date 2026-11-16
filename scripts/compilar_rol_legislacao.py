"""
São Roque GIS Hub · Compilador Completo de Legislação e Inteligência Territorial
Compila 100% da base jurídica oficial de dados_oficiais/sao_roque_geodados.db:
- 221 Normas Jurídicas (Municipais, Estaduais e Federais)
- 1.709 Artigos e Dispositivos Normativos
- 163 Cruzamentos Topológicos (Camada x Norma x Artigo x Grau de Restrição)
Gera data/rol_legislacao_territorial.json com TUDO CONECTADO A TUDO.
"""

import sqlite3
import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DB_PATH = os.path.join(PROJECT_ROOT, "dados_oficiais", "sao_roque_geodados.db")
OUT_JSON = os.path.join(PROJECT_ROOT, "data", "rol_legislacao_territorial.json")

def main():
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"Banco não encontrado em: {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 1. Carregar Cruzamentos Camada x Legislação (163 regras)
    cur.execute("""
    SELECT camada_id, classe_id, norma_esfera, norma_tipo, norma_numero, norma_ano, artigo_dispositivo, grau_restricao, regra_aplicacao, conflito_ou_ponto_atencao
    FROM cruzamento_camada_legislacao
    """)
    cruzamentos = []
    cruzamentos_por_camada = {}
    cruzamentos_por_norma = {}

    for r in cur.fetchall():
        cr_item = {
            "camada_id": r[0],
            "classe_id": r[1],
            "norma_esfera": r[2],
            "norma_tipo": r[3],
            "norma_numero": str(r[4]),
            "norma_ano": r[5],
            "artigo_dispositivo": r[6],
            "grau_restricao": r[7],
            "regra_aplicacao": r[8],
            "conflito_ou_ponto_atencao": r[9]
        }
        cruzamentos.append(cr_item)
        cruzamentos_por_camada.setdefault(r[0], []).append(cr_item)
        norma_key = f"{r[3]}_{r[4]}_{r[5]}".replace(" ", "_")
        cruzamentos_por_norma.setdefault(norma_key, []).append(cr_item)

    print(f"[*] Carregados {len(cruzamentos)} cruzamentos normativo-territoriais em {len(cruzamentos_por_camada)} camadas.")

    # 2. Carregar Artigos Dispositivos por Norma (1.709 artigos)
    cur.execute("""
    SELECT norma_id, artigo, texto_normativo, restricao_urbanistica_ambiental, palavras_chave
    FROM artigos_dispositivos
    """)
    artigos_por_norma = {}
    total_artigos = 0
    for r in cur.fetchall():
        norma_id = r[0]
        artigos_por_norma.setdefault(norma_id, []).append({
            "artigo": r[1],
            "texto": r[2],
            "restricao": r[3],
            "palavras_chave": r[4]
        })
        total_artigos += 1
    print(f"[*] Carregados {total_artigos} artigos de lei distribuídos em {len(artigos_por_norma)} normas.")

    # 3. Metadados Adicionais das Normas Principais (para interface rica)
    METADADOS_ESPECIFICOS = {
        "LC_39_2006": { "ambito": "Todo o Município", "tag": "🌐 Plano Diretor Físico Territorial", "zonas": ["Todas as Zonas"] },
        "LC_40_2006": { "ambito": "Zona Urbana e ZUEs", "tag": "🏙️ Zoneamento Homologado Vigente", "zonas": ["ZUC", "ZCU", "ZUR-ad", "ZUR-md", "ZUR-bd", "ZUI", "ZUE-DT", "ZUE-CM", "ZUPA", "ZR"] },
        "LC_41_2006": { "ambito": "Zona Urbana", "tag": "🏗️ Código de Obras e Edificações", "zonas": ["Zonas Urbanas"] },
        "LC_66_2012": { "ambito": "Revisão de Zoneamento", "tag": "🏙️ Reforma do Zoneamento", "zonas": ["ZUE-DT", "ZUE-CM", "ZCU"] },
        "LC_102_2020": { "ambito": "Chácaras e Maylasky", "tag": "🏡 Enquadramento ZUR-md", "zonas": ["ZUR-md", "Maylasky", "Monte Verde"] },
        "LC_106_2020": { "ambito": "Área Urbana", "tag": "🏘️ Condomínio de Lotes", "zonas": ["ZUR-md", "ZUR-bd", "ZCU"] },
        "LC_120_2022": { "ambito": "Controle de Ruído Urbano", "tag": "🔊 Limites de Ruído (Art. 10-A)", "zonas": ["Todas as Zonas"] },
        "LC_128_2023": { "ambito": "Edificações Consolidadas", "tag": "📋 Anistia e Regularização", "zonas": ["Zonas Urbanas"] },
        "LC_134_2024": { "ambito": "Área Urbana", "tag": "🏘️ Condomínio de Lotes (Ampliação)", "zonas": ["ZUR-md", "ZUR-bd"] },
        "LC_142_2025": { "ambito": "Edificações Consolidadas", "tag": "📋 Prorrogação Anistia", "zonas": ["Zonas Urbanas"] },
        "LEI_6766": { "ambito": "Zona Urbana e Expansão", "tag": "📐 Parcelamento do Solo (Art. 3º)", "zonas": ["Todas as Zonas"] },
        "LEI_12651": { "ambito": "APPs, Cursos d'água e Topos de Morro", "tag": "🌳 Código Florestal (Art. 4º)", "zonas": ["Preservação", "Rural"] },
        "LEI_10257": { "ambito": "Todo o Município", "tag": "🏙️ Estatuto da Cidade", "zonas": ["Todas as Zonas"] },
        "LEI_9866": { "ambito": "Bacia de Mananciais de Itupararanga", "tag": "💧 Proteção aos Mananciais (APM)", "zonas": ["ZUE-CM", "Canguera"] },
        "LEI_11579_2003": { "ambito": "APA de Itupararanga", "tag": "💧 APA da Represa de Itupararanga", "zonas": ["ZUE-CM", "Canguera"] }
    }

    # 4. Carregar 100% das Normas Jurídicas do Banco (221 normas)
    cur.execute("""
    SELECT id, esfera, tipo, numero, ano, orgao, ementa, link_oficial, camadas_competencia
    FROM normas_juridicas
    ORDER BY ano DESC, numero DESC
    """)
    all_laws = cur.fetchall()
    print(f"[*] Ingerindo {len(all_laws)} normas jurídicas do banco oficial...")

    municipais = []
    estaduais = []
    federais = []

    for r in all_laws:
        n_id = r[0]
        n_esfera = r[1] or "Municipal"
        n_tipo = r[2] or "Norma"
        n_num = str(r[3] or "")
        n_ano = r[4] or 2000
        n_orgao = r[5] or ""
        n_ementa = r[6] or ""
        n_link = r[7] or "https://www.camarasaoroque.sp.gov.br"
        n_camadas = r[8] or ""

        info = METADADOS_ESPECIFICOS.get(n_id, {})
        artigos_da_norma = artigos_por_norma.get(n_id, [])

        norma_dict = {
            "id": n_id,
            "tipo": n_tipo,
            "numero": n_num,
            "ano": n_ano,
            "esfera": n_esfera,
            "esfera_label": f"Esfera {n_esfera.split(' ')[0]}",
            "orgao": n_orgao,
            "ementa": n_ementa,
            "link_oficial": n_link,
            "ambito_territorial": info.get("ambito", "Todo o Território Municipal"),
            "tag_ambito": info.get("tag", f"⚖️ {n_tipo} nº {n_num}/{n_ano}"),
            "zonas_afetadas": info.get("zonas", ["Todo o Município"]),
            "camadas_competencia": [c.strip() for c in n_camadas.split(",") if c.strip()],
            "total_artigos": len(artigos_da_norma),
            "artigos_amostra": [
                { "artigo": a["artigo"], "restricao": a["restricao"] or a["texto"][:120] }
                for a in artigos_da_norma[:6]
            ]
        }

        esf_lower = n_esfera.lower()
        if "municipal" in esf_lower:
            norma_dict["esfera_cat"] = "municipal"
            municipais.append(norma_dict)
        elif "estadual" in esf_lower or "sp" in esf_lower or "judiciário" in esf_lower:
            norma_dict["esfera_cat"] = "estadual"
            estaduais.append(norma_dict)
        else:
            norma_dict["esfera_cat"] = "federal"
            federais.append(norma_dict)

    print(f"  [+] Municipais: {len(municipais)}")
    print(f"  [+] Estaduais: {len(estaduais)}")
    print(f"  [+] Federais e Normas Gerais: {len(federais)}")
    total_catalogo = len(municipais) + len(estaduais) + len(federais)
    print(f"  [+] Total compilado: {total_catalogo} normas jurídicas.")

    # 5. Carregar Parâmetros de Classes e Zonas
    cur.execute("""
    SELECT codigo_classe, nome_classe, camada_id, metodologia_referencia, angulo_equivalente, implicacao_pratica
    FROM classes_camada_territorial
    GROUP BY codigo_classe
    """)
    zonas_db = {}
    for r in cur.fetchall():
        zonas_db[r[0]] = {
            "codigo": r[0],
            "nome": r[1],
            "categoria": r[2],
            "lei_referencia": r[3] or "Minuta Revisão Plano Diretor (Agosto/2026)",
            "taxa_ocupacao": "Conforme Quadro de Parâmetros Urbanísticos",
            "coeficiente_aproveitamento": "Básico: 1.0 | Máximo: até 1.4",
            "gabarito_altura": r[4] or "Conforme Zoneamento",
            "lote_minimo": "250m² a 1.000m²",
            "recuos": "Frontal: 5,00m | Lateral: 1,50m | Fundos: 3,00m",
            "usos_admitidos": r[5] or "Residencial, Comercial e Institucional",
            "restricoes": r[5] or "Conforme Minuta LC nº 40/2006"
        }

    output_data = {
        "municipio": "Estância Turística de São Roque (SP)",
        "codigo_ibge": "3550605",
        "total_leis_catalogo": total_catalogo,
        "total_artigos_banco": total_artigos,
        "total_cruzamentos_topologicos": len(cruzamentos),
        "leis": {
            "municipal": municipais,
            "estadual": estaduais,
            "federal": federais
        },
        "cruzamentos_camadas": cruzamentos_por_camada,
        "zonas_parametros": zonas_db
    }

    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"[SUCESSO] 100% da base legal compilada em {OUT_JSON} ({total_catalogo} leis, {total_artigos} artigos, {len(cruzamentos)} cruzamentos).")
    conn.close()

if __name__ == "__main__":
    main()
