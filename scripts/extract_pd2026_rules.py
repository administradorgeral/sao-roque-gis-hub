import json
import re
import pypdfium2 as pdfium

print("=== EXTRAÇÃO ESTRUTURADA DAS NORMAS E ÍNDICES DO PLANO DIRETOR 2026 ===")

lc40_pdf = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\minuta_pd2026\desmembrado\04_minuta_lc40_zoneamento_uso_ocupacao.pdf"
doc = pdfium.PdfDocument(lc40_pdf)

# 1. Extrair texto completo e mapear artigos
full_text = []
articles = {}
current_art = None

for p_idx, page in enumerate(doc):
    tp = page.get_textpage()
    txt = tp.get_text_range(0, tp.count_chars())
    full_text.append(txt)

all_txt = "\n".join(full_text)

# Regex para artigos
art_matches = list(re.finditer(r'(Art\.\s*(\d+)[°ºo\.]?)([\s\S]*?)(?=(Art\.\s*\d+[°ºo\.]?)|$)', all_txt))
print(f"Total de Artigos identificados na LC 40/2026: {len(art_matches)}")

# 2. Estrutura dos Quadros Urbanísticos de 2026
quadros_data = {
    "QUADRO_I_ZUE_INDICES": {
        "titulo": "Quadro I - Parâmetros e Índices Urbanísticos da Macrozona de Urbanização Específica (ZUE)",
        "zonas": {
            "ZUE_CHACARAS_MANANCIAL": {
                "nome": "ZUE - Chácaras em Manancial",
                "lote_minimo_m2": 5000,
                "testada_minima_m": 50,
                "taxa_ocupacao_max": 0.50,
                "coeficiente_aproveitamento_lote": 1.0,
                "taxa_permeabilidade_min": 0.50,
                "gabarito_altura_m": 30.0,
                "observacao": "Usos admitidos CS, TL, IT, RG e RL. Loteamentos anteriores mantêm TO com gabarito de 8m."
            },
            "ZUE_INTERESSE_TURISTICO": {
                "nome": "ZUE - Interesse Turístico",
                "taxa_ocupacao_max": 0.50,
                "gabarito_basico_m": 12.0,
                "gabarito_maximo_m": 24.0,
                "coeficiente_aproveitamento_max": 1.2,
                "perimetro_especial_mombaca": "No Bairro Mombaça, admite CA 1.2 e gabarito 24m para residencial multifamiliar de apoio a trabalhadores da Castello Branco.",
                "outorga_onerosa": "Elevação de CA e Gabarito acima do básico condicionada a Outorga Onerosa do Direito de Construir (OODC)."
            },
            "ZUE_DESENVOLVIMENTO_ECONOMICO": {
                "nome": "ZUE - Desenvolvimento Econômico",
                "vocacao": "Indústria limpa, logística, serviços e comércio estruturado.",
                "restricao": "Vedado aterro sanitário e cemitério."
            },
            "ZUE_OCUPACAO_ESTRATEGICA": {
                "nome": "ZUE - Ocupação Estratégica",
                "vocacao": "Projetos de impacto metropolitano e integração regional.",
                "restricao": "Vedado aterro sanitário e cemitério."
            }
        }
    },
    "QUADRO_VIII_PARCELAMENTO_URBANO": {
        "titulo": "Quadro VIII - Limitações de Parcelamento do Solo na Macrozona de Consolidação Urbana",
        "zonas": {
            "ZUR_bd": {
                "nome": "ZUR-bd (Zona Urbana Residencial de Baixa Densidade)",
                "sistema_viario_min_pct": 20.0,
                "area_verde_min_pct": 10.0,
                "area_institucional_min_pct": 5.0,
                "lote_minimo_m2": 250,
                "testada_minima_m": 10.0
            },
            "ZUR_md": {
                "nome": "ZUR-md (Zona Urbana Residencial de Média Densidade)",
                "sistema_viario_min_pct": 20.0,
                "area_verde_min_pct": 10.0,
                "area_institucional_min_pct": 5.0,
                "lote_minimo_m2": 250,
                "testada_minima_m": 10.0
            },
            "ZUR_ad": {
                "nome": "ZUR-ad (Zona Urbana Residencial de Alta Densidade)",
                "sistema_viario_min_pct": 20.0,
                "area_verde_min_pct": 10.0,
                "area_institucional_min_pct": 5.0,
                "lote_minimo_m2": 250,
                "testada_minima_m": 10.0
            },
            "ZUC": {
                "nome": "ZUC (Zona Urbana Central)",
                "area_institucional_min_pct": 5.0,
                "lote_minimo_m2": 250,
                "testada_minima_m": 10.0
            },
            "ZUI": {
                "nome": "ZUI (Zona Urbana Industrial)",
                "sistema_viario_max_pct": 15.0,
                "area_verde_min_pct": 10.0,
                "area_institucional_min_pct": 10.0,
                "lote_minimo_m2": 250,
                "testada_minima_m": 10.0
            }
        }
    },
    "QUADRO_IX_RECUOS_OBRIGATORIOS": {
        "titulo": "Quadro IX - Exigências de Recuos Obrigatórios das Edificações",
        "zonas": {
            "ZUR_bd": {"recuo_frontal_m": 5.0, "recuo_lateral_m": 1.5, "recuo_fundo_m": 3.0},
            "ZUR_md": {"recuo_frontal_m": 5.0, "recuo_lateral_m": 1.5, "recuo_fundo_m": 3.0},
            "ZUR_ad": {"recuo_frontal_m": 5.0, "recuo_lateral_m": 1.5, "recuo_fundo_m": 3.0},
            "ZUC": {"recuo_frontal_m": 0.0, "recuo_lateral_m": 0.0, "recuo_fundo_m": 0.0, "nota": "Alinhamento com logradouro conforme partido do centro histórico"},
            "ZUI": {"recuo_frontal_m": 10.0, "recuo_lateral_m": 3.0, "recuo_fundo_m": 5.0}
        },
        "regras_edícula": {
            "area_maxima_pct": 30.0,
            "distancia_minima_construcao_principal_m": 2.0,
            "zonas_permitidas": "Apenas na Macrozona de Consolidação Urbana"
        }
    },
    "CORREDORES_ESPECIAIS": {
        "ZUCL": {
            "nome": "ZUCL - Corredor Logístico",
            "eixos": ["Rodovia Lívio Tagliassachi", "Principais acessos viários estruturantes"],
            "usos_permitidos": ["Comércio", "Serviços", "Logística", "Armazenagem", "Turismo", "Indústrias compatíveis"],
            "exigencias": "Tratamento qualificado de fachadas, proibição de depósitos de sucata e armazenamento a céu aberto que firam a paisagem e o turismo."
        }
    },
    "INTERVENCOES_PRIORITARIAS_SRQ": {
        "total_projetos": 22,
        "codigo_intervalo": "SRQ-01 a SRQ-22",
        "principais_obras": [
            {"codigo": "SRQ-01 a SRQ-07", "descricao": "Obras de macrodrenagem e qualificação do Centro (Av. Antonino Dias Bastos, Av. John Kennedy, Av. 3 de Maio)"},
            {"codigo": "SRQ-08 a SRQ-15", "descricao": "Requalificação do Sistema Viário de Maylasky e acessos à Raposo Tavares"},
            {"codigo": "SRQ-16 a SRQ-22", "descricao": "Mobilidade e ciclovias integradas na Rota do Vinho (Canguera) e conexão São João Novo"}
        ]
    }
}

out_json = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\data\revisao_plano_diretor_2026_indices.json"
with open(out_json, "w", encoding="utf-8") as f:
    json.dump(quadros_data, f, ensure_ascii=False, indent=2)

print(f"✓ Salvo arquivo JSON estruturado de parâmetros: {out_json}")
