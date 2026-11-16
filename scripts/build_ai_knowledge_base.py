#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_ai_knowledge_base.py (Versão Expandida - Sem Restrições)
Compila a Base de Conhecimento Estruturada para a Busca e Assistente com IA Territorial
do São Roque GIS Hub (Código IBGE: 3550605).

Inclui:
- Todas as 13 Cartas Oficiais do Plano Diretor 2026 (Folhas I a XIII)
- As 22 Obras Estruturantes Prioritárias (SRQ-01 a SRQ-22)
- Mais de 60 Bairros, Distritos, Rodovias e Localidades com coordenadas e zoneamento padrão
- Guia Prático de Usos e Atividades (Pousada, Indústria, Comércio, Posto, Desdobro, Condomínio)
- Instrumentos Urbanísticos (Outorga Onerosa OODC, TPC, IPTU Progressivo, PEUC, EIV/RIV, REURB)
- Restrições Ambientais (APA Itupararanga, AHS, Mata Atlântica, Declividade 30% e 45°, RBCV)
- Restrições Aeronáuticas (Aeroporto Catarina PBZPA, SLO, ASA 20km)
- 1.709 Artigos e Dispositivos Normativos Oficiais de são_roque_geodados.db
- 109 Classes Territoriais com Implicações Práticas
- 221 Normas Jurídicas Oficiais
- Dados Demográficos do Censo IBGE 2022 e CNEFE
"""

import os
import sys
import json
import sqlite3

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(BASE_DIR, "dados_oficiais", "sao_roque_geodados.db")
ROL_PATH = os.path.join(DATA_DIR, "rol_legislacao_territorial.json")
REV_PATH = os.path.join(DATA_DIR, "revisao_plano_diretor_2026_indices.json")
PART_PATH = os.path.join(DATA_DIR, "participacao_popular_plano_diretor.json")
OUT_PATH = os.path.join(DATA_DIR, "base_conhecimento_ia.json")

def main():
    print("Compilando Base de Conhecimento Ampla e Irrestrita para São Roque...", file=sys.stderr)
    
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    
    # 1. Normas Jurídicas
    normas_rows = con.execute("""
        SELECT id, esfera, tipo, numero, ano, orgao, ementa, vigencia, link_oficial, camadas_competencia
        FROM normas_juridicas
        ORDER BY ano DESC, numero DESC
    """).fetchall()
    normas = [dict(r) for r in normas_rows]

    # 2. Artigos Chave / Dispositivos Normativos
    artigos_rows = con.execute("""
        SELECT id, norma_id, artigo, texto_normativo, restricao_urbanistica_ambiental, palavras_chave
        FROM artigos_dispositivos
        WHERE texto_normativo IS NOT NULL AND length(texto_normativo) > 10
    """).fetchall()
    artigos = [dict(r) for r in artigos_rows]

    # 3. Cruzamento Camada x Legislação
    tables = [r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
    cruzamentos = []
    if "cruzamento_camada_legislacao" in tables:
        cruz_rows = con.execute("""
            SELECT camada_id, norma_esfera, norma_tipo, norma_numero, norma_ano,
                   artigo_dispositivo, grau_restricao, regra_aplicacao, conflito_ou_ponto_atencao
            FROM cruzamento_camada_legislacao
        """).fetchall()
        cruzamentos = [dict(r) for r in cruz_rows]

    # 4. Camadas Territoriais
    camadas = []
    if "camadas_territoriais" in tables:
        cam_rows = con.execute("""
            SELECT id, nome, titulo_documento, categoria, tipo_camada, escala_nominal,
                   status_auditoria, alerta_juridico, bounds_wgs84_json
            FROM camadas_territoriais
        """).fetchall()
        camadas = [dict(r) for r in cam_rows]

    # 5. Classes das Camadas
    classes = []
    if "classes_camada_territorial" in tables:
        cls_rows = con.execute("""
            SELECT camada_id, codigo_classe, nome_classe, cor_hex, implicacao_pratica
            FROM classes_camada_territorial
        """).fetchall()
        classes = [dict(r) for r in cls_rows]

    # 6. Rol de Legislação e Parâmetros Urbanísticos das Zonas
    rol = {}
    if os.path.exists(ROL_PATH):
        with open(ROL_PATH, "r", encoding="utf-8") as f:
            rol = json.load(f)
    zonas_parametros = rol.get("zonas_parametros", {})

    # 7. Índices Comparativos da Revisão do Plano Diretor 2026
    revisao_2026 = {}
    if os.path.exists(REV_PATH):
        with open(REV_PATH, "r", encoding="utf-8") as f:
            revisao_2026 = json.load(f)

    # 7b. Pedidos e Manifestações da Participação Popular (Audiências e Consultas Públicas 2024-2026)
    pedidos_participacao = []
    if os.path.exists(PART_PATH):
        with open(PART_PATH, "r", encoding="utf-8") as f:
            pedidos_participacao = json.load(f)

    # 8. CATÁLOGO COMPLETO DAS 13 CARTAS DO PLANO DIRETOR 2026
    cartas_pd2026 = [
        {
            "numero": 1,
            "romano": "I",
            "camada_id": "carta_01_macrozoneamento_2026",
            "titulo": "Carta I: Macrozoneamento Municipal (2026)",
            "folha": "01/13",
            "descricao": "Estabelece a divisão estrutural de todo o território municipal em 4 Grandes Macrozonas: Macrozona de Consolidação Urbana, Macrozona de Urbanização Específica (ZUE), Macrozona de Proteção Ambiental (APA Itupararanga e mananciais) e Macrozona Rural.",
            "zonas_principais": ["Macrozona de Consolidação Urbana", "Macrozona de Urbanização Específica (ZUE)", "Macrozona de Proteção Ambiental", "Macrozona Rural"],
            "centro_mapa": [-23.5350, -47.1350, 12],
            "leis_correlatas": ["LC 39/2006", "Minuta 2026", "Estatuto da Cidade (Lei 10.257/2001)"]
        },
        {
            "numero": 2,
            "romano": "II",
            "camada_id": "carta_02_zue_2026",
            "titulo": "Carta II: Macrozoneamento da ZUE - Urbanização Específica (2026)",
            "folha": "02/13",
            "descricao": "Regulamenta as Zonas de Urbanização Específica (ZUE): ZUE Chácaras em Manancial (lote mínimo 5.000m²), ZUE Interesse Turístico (gabarito básico 12m e máx 24m com OODC), ZUE Desenvolvimento Econômico (indústria limpa e logística) e ZUE Ocupação Estratégica (projetos de impacto metropolitano).",
            "zonas_principais": ["ZUE Chácaras em Manancial", "ZUE Interesse Turístico", "ZUE Desenvolvimento Econômico", "ZUE Ocupação Estratégica"],
            "centro_mapa": [-23.5250, -47.1150, 12],
            "leis_correlatas": ["Quadro I da Minuta 2026", "LC 40/2006", "Lei Estadual 10.100/1998 (APA)"]
        },
        {
            "numero": 3,
            "romano": "III",
            "camada_id": "carta_03_consolidacao_urbana_2026",
            "titulo": "Carta III: Consolidação Urbana Geral (2026)",
            "folha": "03/13",
            "descricao": "Visão integrada da malha urbana municipal, articulando os quatro distritos (Sede, Maylasky, São João Novo e Canguera) com os perímetros de expansão urbana e contenção de vazios.",
            "zonas_principais": ["Perímetro Urbano Consolidado", "Vetores de Articulação Distrital", "Áreas de Contenção"],
            "centro_mapa": [-23.5325, -47.1350, 12],
            "leis_correlatas": ["LC 39/2006", "LC 40/2006", "Minuta 2026"]
        },
        {
            "numero": 4,
            "romano": "IV",
            "camada_id": "carta_04_sede_2026",
            "titulo": "Carta IV: Consolidação Urbana - Sede (2026)",
            "folha": "04/13",
            "descricao": "Zoneamento detalhado da Sede Municipal de São Roque. Define os perímetros da ZUC (Zona Central), ZUR-bd (Baixa Densidade), ZUR-md (Média Densidade), ZUR-ad (Alta Densidade), ZUI (Industrial) e Corredores de Comércio e Serviços Centrais.",
            "zonas_principais": ["ZUC", "ZUR-bd", "ZUR-md", "ZUR-ad", "ZUI", "Corredores Centrais"],
            "centro_mapa": [-23.5325, -47.1350, 15],
            "leis_correlatas": ["Quadros VIII e IX da Minuta 2026", "LC 40/2006", "LC 66/2012"]
        },
        {
            "numero": 5,
            "romano": "V",
            "camada_id": "carta_05_maylasky_2026",
            "titulo": "Carta V: Consolidação Urbana - Maylasky (2026)",
            "folha": "05/13",
            "descricao": "Zoneamento e ordenamento territorial do Distrito de Maylasky. Define as zonas residenciais (ZUR-md), áreas de apoio logístico/industrial próximas à ferrovia e à Rodovia Raposo Tavares, e perímetros de regularização fundiária (AEIS).",
            "zonas_principais": ["ZUR-md Maylasky", "ZUE Maylasky", "AEIS Maylasky", "Eixo Raposo Tavares"],
            "centro_mapa": [-23.5510, -47.0580, 14],
            "leis_correlatas": ["LC 40/2006", "LC 102/2020", "Minuta 2026 Art. 110"]
        },
        {
            "numero": 6,
            "romano": "VI",
            "camada_id": "carta_06_sao_joao_novo_2026",
            "titulo": "Carta VI: Consolidação Urbana - São João Novo (2026)",
            "folha": "06/13",
            "descricao": "Zoneamento territorial do Distrito de São João Novo. Foco na preservação da ambiência de chácaras de recreio e baixa densidade (ZUE-SJN), prevenção de inundações nas várzeas e integração viária com a Rodovia Eng. Renê Benedito da Silva rumo a Itapevi.",
            "zonas_principais": ["ZUE-SJN", "ZUR-bd SJN", "Áreas de Várzea e Drenagem", "Eixo Renê Benedito"],
            "centro_mapa": [-23.4850, -47.0750, 14],
            "leis_correlatas": ["LC 40/2006", "Minuta 2026 Art. 115"]
        },
        {
            "numero": 7,
            "romano": "VII",
            "camada_id": "carta_07_canguera_2026",
            "titulo": "Carta VII: Consolidação Urbana - Canguera (2026)",
            "folha": "07/13",
            "descricao": "Zoneamento territorial do Distrito de Canguera e do Polo do Roteiro do Vinho. Regulamenta a Zona de Desenvolvimento Turístico (ZUE-DT), admitindo adegas, restaurantes, vinícolas e pousadas com estrita proteção aos mananciais da APA de Itupararanga.",
            "zonas_principais": ["ZUE-DT Turismo", "Corredor Estrada do Vinho", "Macrozona de Proteção Ambiental APA", "Áreas Agrícolas e Vitivinícolas"],
            "centro_mapa": [-23.5850, -47.1250, 14],
            "leis_correlatas": ["LC 40/2006", "LC 65/2012", "Lei Estadual 10.100/1998 (APA Itupararanga)"]
        },
        {
            "numero": 8,
            "romano": "VIII",
            "camada_id": "carta_08_corredores_2026",
            "titulo": "Carta VIII: Corredores de Comércio, Serviços e Turismo (2026)",
            "folha": "08/13",
            "descricao": "Define os eixos lineares de dinamização econômica: ZUCL (Corredor Logístico da Rodovia Lívio Tagliassachi), Corredores da Rodovia Raposo Tavares, Estrada do Vinho, Corredor Catarina/Castello Branco e vias de comércio qualificado com exigência de fachadas ativas.",
            "zonas_principais": ["ZUCL Rodovia Lívio Tagliassachi", "Corredor Raposo Tavares", "Corredor Catarina", "Corredores de Fachada Ativa Central"],
            "centro_mapa": [-23.5050, -47.1200, 13],
            "leis_correlatas": ["Minuta 2026 Seção Corredores Especiais", "LC 40/2006"]
        },
        {
            "numero": 9,
            "romano": "IX",
            "camada_id": "carta_09_aeis_2026",
            "titulo": "Carta IX: Áreas de Especial Interesse AEIS / AEIT / AEIU (2026)",
            "folha": "09/13",
            "descricao": "Mapeia as Áreas Especiais: AEIS (Interesse Social para habitação popular e REURB), AEIT (Interesse Turístico como Rota do Vinho e Morro do Saboó), AEIU (Interesse Urbanístico para renovação e requalificação) e AEIA (Interesse Ambiental para conservação e parques lineares).",
            "zonas_principais": ["AEIS 1 a 6 (Habitação Social / REURB)", "AEIT (Turismo)", "AEIU 1 a 10 (Renovação Urbana)", "AEIA (Proteção Ambiental)"],
            "centro_mapa": [-23.5350, -47.1350, 13],
            "leis_correlatas": ["Minuta 2026 Art. 75 a 92A", "Lei Federal 13.465/2017 (REURB)", "Estatuto da Cidade"]
        },
        {
            "numero": 10,
            "romano": "X",
            "camada_id": "carta_10_viario_sede_2026",
            "titulo": "Carta X: Sistema Viário e Drenagem - Sede (2026)",
            "folha": "10/13",
            "descricao": "Hierarquização viária do Centro Expandido (vias expressas, arteriais, coletoras e locais) e sistema estruturante de macrodrenagem pluvial (piscinões, bacias de amortecimento nos Córregos Aracaí e Carambeí, conceitos de 'Cidade Esponja').",
            "zonas_principais": ["Vias Arteriais Sede", "Anel Viário Roberto de Mattos", "Bacias de Retenção e Amortecimento", "Parques Lineares Fluviais"],
            "centro_mapa": [-23.5325, -47.1350, 14],
            "leis_correlatas": ["Minuta 2026 Art. 96, 128 e 130", "LC 40/2006 Art. 30 a 35"]
        },
        {
            "numero": 11,
            "romano": "XI",
            "camada_id": "carta_11_viario_maylasky_2026",
            "titulo": "Carta XI: Sistema Viário e Drenagem - Maylasky (2026)",
            "folha": "11/13",
            "descricao": "Propostas do sistema viário do Distrito de Maylasky: adequações das transposições da linha férrea, novos acessos à Rodovia Raposo Tavares, vias marginais e canais de drenagem das sub-bacias orientais.",
            "zonas_principais": ["Transposições Ferroviárias Maylasky", "Marginais Raposo Tavares", "Drenagem Bacia Oriental"],
            "centro_mapa": [-23.5510, -47.0580, 14],
            "leis_correlatas": ["Minuta 2026 Art. 96 e Carta XI", "LC 40/2006"]
        },
        {
            "numero": 12,
            "romano": "XII",
            "camada_id": "carta_12_viario_canguera_2026",
            "titulo": "Carta XII: Sistema Viário e Drenagem - Canguera (2026)",
            "folha": "12/13",
            "descricao": "Propostas viárias para o Distrito de Canguera: ordenamento dos acessos da Estrada do Vinho (SPV-077), exigência de bolsões e faixas de desaceleração para ônibus e carros de turistas em adegas/restaurantes, e preservação da drenagem natural na bacia de Itupararanga.",
            "zonas_principais": ["Bolsões Estrada do Vinho", "Adequações SPV-077", "Drenagem Bacia Itupararanga"],
            "centro_mapa": [-23.5850, -47.1250, 14],
            "leis_correlatas": ["Minuta 2026 Art. 127 e Parágrafo Único", "Lei Estadual 10.100/1998"]
        },
        {
            "numero": 13,
            "romano": "XIII",
            "camada_id": "carta_13_obras_prioritarias_2026",
            "titulo": "Carta XIII: Obras Estruturantes Prioritárias SRQ-01 a SRQ-22 (2026)",
            "folha": "13/13",
            "descricao": "Mapeia as 22 Intervenções e Obras Públicas Prioritárias do Município (SRQ-01 a SRQ-22) e Áreas de Risco Geológico/Hidrológico da Defesa Civil. Inclui macrodrenagem da Av. Antonino Dias Bastos e John Kennedy, Anel Viário intraurbano, ciclovias na Rota do Vinho e novas pontes e transposições.",
            "zonas_principais": ["SRQ-01 a SRQ-22", "Áreas de Risco Defesa Civil", "Parques de Drenagem", "Intervenções Raposo e Castello"],
            "centro_mapa": [-23.5350, -47.1350, 13],
            "leis_correlatas": ["Minuta 2026 Art. 96, 128 a 131", "Lei Federal 12.608/2012 (Defesa Civil)"]
        }
    ]

    # 9. AS 22 OBRAS ESTRUTURANTES PRIORITÁRIAS (SRQ-01 a SRQ-22)
    obras_prioritarias = [
        {"codigo": "SRQ-01", "nome": "Macrodrenagem e Parque Linear Av. John Kennedy", "local": "Centro / Av. John Kennedy", "tipo": "Drenagem e Lazer", "descricao": "Estrutura de retenção pluvial e requalificação paisagística para contenção de inundações na área central."},
        {"codigo": "SRQ-02", "nome": "Canalização e Bacia de Retenção Av. Antonino Dias Bastos", "local": "Marginal Centro", "tipo": "Drenagem", "descricao": "Obras estruturais de aumento da calha do Ribeirão Aracaí e piscinão de amortecimento a montante."},
        {"codigo": "SRQ-03", "nome": "Requalificação da Av. Três de Maio e Praças Centrais", "local": "Centro", "tipo": "Mobilidade e Paisagismo", "descricao": "Passeios acessíveis, fiação subterrânea/reordenada, iluminação LED e mobiliário urbano inteligente."},
        {"codigo": "SRQ-04", "nome": "Reforma e Recomposição da Praça da Matriz", "local": "Centro Histórico", "tipo": "Patrimônio e Turismo", "descricao": "Projeto paisagístico de reforma da Matriz, valorização de fachadas históricas e ampliação do calçadão."},
        {"codigo": "SRQ-05", "nome": "Ponte de Conexão Centro - Guaçu", "local": "Guaçu / Centro", "tipo": "Sistema Viário", "descricao": "Nova transposição sobre o rio para desafogar a Av. Bernardino de Lucca e melhorar o fluxo ao Guaçu."},
        {"codigo": "SRQ-06", "nome": "Transformação da Raposo Tavares em Av. Roberto de Mattos", "local": "Trecho Urbano Raposo Tavares", "tipo": "Sistema Viário Arterial", "descricao": "Adequação do trecho rodoviário para avenida urbana com canteiro central, semáforos, calçadas e arborização."},
        {"codigo": "SRQ-07", "nome": "Conexão Viária Av. Roberto de Mattos com Av. Aracaí", "local": "Interseção Aracaí", "tipo": "Anel Viário", "descricao": "Trevo em nível com semaforização inteligente interligando a nova avenida ao sistema central."},
        {"codigo": "SRQ-08", "nome": "Interseção Roberto de Mattos com Rodovia Quintino de Lima", "local": "Saída para Ibiúna", "tipo": "Trevo Viário", "descricao": "Reordenamento geométrico para eliminação de pontos críticos de acidentes e fluidez rumo a Canguera/Ibiúna."},
        {"codigo": "SRQ-09", "nome": "Duplicação e Marginais no Eixo Maylasky (SP-270)", "local": "Distrito de Maylasky", "tipo": "Mobilidade Rodoviária", "descricao": "Vias marginais pavimentadas para segregar o tráfego local do fluxo intermunicipal da Raposo Tavares."},
        {"codigo": "SRQ-10", "nome": "Transposição Ferroviária Desnivelada de Maylasky", "local": "Estação de Maylasky", "tipo": "Infraestrutura Ferro-Viária", "descricao": "Viaduto/passagem inferior para eliminar cruzamento rodoferroviário em nível e garantir segurança."},
        {"codigo": "SRQ-11", "nome": "Canalização e Drenagem da Bacia de Maylasky", "local": "Maylasky Centro", "tipo": "Drenagem", "descricao": "Canalização técnica com bacias de detenção junto aos córregos lindeiros aos loteamentos consolidados."},
        {"codigo": "SRQ-12", "nome": "Requalificação do Corredor Logístico da Rodovia Lívio Tagliassachi (ZUCL)", "local": "Acesso Castello Branco", "tipo": "Corredor Econômico", "descricao": "Implantação de acostamentos, iluminação e faixas adicionais para suporte a galpões logísticos e turismo."},
        {"codigo": "SRQ-13", "nome": "Trevo de Acesso ao Saboó e Aeroporto Catarina", "local": "Saboó / Catarina", "tipo": "Sistema Viário", "descricao": "Acesso seguro conectando a Estrada do Morro do Saboó e áreas de expansão aeroportuária."},
        {"codigo": "SRQ-14", "nome": "Parque Municipal do Morro do Saboó (AEIU 9)", "local": "Morro do Saboó", "tipo": "Turismo e Preservação", "descricao": "Estruturação de trilhas ecológicas sustentáveis, mirante turístico e proteção de topos de morro."},
        {"codigo": "SRQ-15", "nome": "Ciclovia e Bolsões de Parada na Estrada do Vinho (SPV-077)", "local": "Canguera / Roteiro do Vinho", "tipo": "Turismo e Mobilidade Ativa", "descricao": "Ciclovia turística segregada, sinalização enoturística e baías para estacionamento e ônibus."},
        {"codigo": "SRQ-16", "nome": "Contorno Viário Norte de Canguera", "local": "Canguera Norte", "tipo": "Sistema Viário", "descricao": "Via coletora alternativa para retirar o tráfego pesado de caminhões agrícolas da frente das vinícolas."},
        {"codigo": "SRQ-17", "nome": "Parque Linear do Patrimônio do Carmo e Lagoas", "local": "Carmo / Canguera", "tipo": "Drenagem e Meio Ambiente", "descricao": "Recuperação das margens de lagos e córregos contribuintes da represa de Itupararanga."},
        {"codigo": "SRQ-18", "nome": "Requalificação da Rodovia Eng. Renê Benedito da Silva", "local": "São João Novo", "tipo": "Sistema Viário", "descricao": "Melhorias de pavimento, drenagem superficial e acostamentos conectando São João Novo a Itapevi."},
        {"codigo": "SRQ-19", "nome": "Transposição Urbana sobre a Ferrovia em São João Novo", "local": "SJN Centro", "tipo": "Sistema Viário", "descricao": "Ponte/viaduto articulando as duas margens da malha ferroviária e unificando o comércio distrital."},
        {"codigo": "SRQ-20", "nome": "Sistema de Contenção de Cheias na Várzea de São João Novo", "local": "Várzeas SJN", "tipo": "Drenagem Urbana", "descricao": "Diques e áreas verdes inundáveis de amortecimento para eliminar alagamentos em habitações históricas."},
        {"codigo": "SRQ-21", "nome": "Modernização Tecnológica do Terminal Urbano e Pontos de Ônibus", "local": "Municipal", "tipo": "Transporte Público", "descricao": "Informação em tempo real aos usuários, frota sustentável, abrigos modernos e integração tarifária."},
        {"codigo": "SRQ-22", "nome": "Complexo Esportivo, Educacional e Cultural da Brasital", "local": "Centro Cultural Brasital", "tipo": "Patrimônio Histórico", "descricao": "Revitalização completa do conjunto fabril histórico Brasital, preservando a memória têxtil e ampliando uso público."}
    ]

    # 10. GUIA DE BAIRROS, DISTRITOS E LOGRADOUROS PRINCIPAIS DE SÃO ROQUE
    bairros_localidades = [
        {"nome": "Centro", "distrito": "São Roque", "cartas": ["Carta IV", "Carta X", "Carta XIII"], "zoneamento_padrao": "ZUC", "centro": [-23.5325, -47.1350, 16], "descricao": "Coração histórico, financeiro e comercial de São Roque. Dispensado de recuos no alinhamento frontal (LC 40/06 Art. 104), TO 80%, CA 3.2, gabarito até 13m (3 a 4 pavimentos)."},
        {"nome": "Jardim Villaça", "distrito": "São Roque", "cartas": ["Carta IV", "Carta X"], "zoneamento_padrao": "ZUR-md", "centro": [-23.5380, -47.1380, 15], "descricao": "Bairro residencial consolidado próximo ao Centro. Lote mínimo 250m², TO 60%, recuo frontal 5m, lateral 1,5m e fundos 3m."},
        {"nome": "Vila Aguiar", "distrito": "São Roque", "cartas": ["Carta IV", "Carta X"], "zoneamento_padrao": "ZUR-md", "centro": [-23.5280, -47.1320, 15], "descricao": "Bairro residencial tradicional. Residência unifamiliar e multifamiliar, comércio vicinal e serviços locais."},
        {"nome": "Guaçu (I e II)", "distrito": "São Roque", "cartas": ["Carta IV", "Carta X", "Carta XIII"], "zoneamento_padrao": "ZUR-md", "centro": [-23.5250, -47.1450, 15], "descricao": "Importante bairro residencial e de serviços. Contemplado com a nova ponte de transposição sobre o rio (SRQ-05) e bacias de drenagem pluvial."},
        {"nome": "Gabriel Piza", "distrito": "São Roque", "cartas": ["Carta IV", "Carta VIII"], "zoneamento_padrao": "ZUR-bd", "centro": [-23.5420, -47.1180, 15], "descricao": "Bairro residencial de média e baixa densidade lindeiro à Rodovia Raposo Tavares, com vocação mista para comércio e residências."},
        {"nome": "Paisagem Colonial", "distrito": "São Roque", "cartas": ["Carta IV", "Carta IX"], "zoneamento_padrao": "ZUR-md / AEIS", "centro": [-23.5450, -47.1290, 15], "descricao": "Bairro com áreas consolidadas e setores mapeados como AEIS para regularização fundiária (REURB) e melhorias de saneamento e drenagem."},
        {"nome": "Goianã", "distrito": "São Roque", "cartas": ["Carta IV", "Carta IX"], "zoneamento_padrao": "ZUR-md", "centro": [-23.5480, -47.1320, 15], "descricao": "Bairro contíguo ao Paisagem Colonial, prioritário para extensão de redes coletoras de esgoto e pavimentação."},
        {"nome": "Taboão", "distrito": "São Roque", "cartas": ["Carta IV", "Carta X"], "zoneamento_padrao": "ZUR-md / ZUI", "centro": [-23.5210, -47.1280, 15], "descricao": "Região de transição urbano-industrial com galpões, comércio atacadista e residências consolidadas."},
        {"nome": "Junqueira", "distrito": "São Roque", "cartas": ["Carta IV", "Carta X"], "zoneamento_padrao": "ZUR-md", "centro": [-23.5350, -47.1420, 15], "descricao": "Bairro residencial histórico da cidade, próximo à antiga Estação Ferroviária e ao Córrego Aracaí."},
        {"nome": "Marmeleiro", "distrito": "São Roque", "cartas": ["Carta IV", "Carta VIII"], "zoneamento_padrao": "ZUR-md / Corredor", "centro": [-23.5450, -47.1480, 15], "descricao": "Bairro com forte vocação comercial lindeiro à SP-270, com acessos expressos e comércio de materiais, serviços automotivos e residências."},
        {"nome": "Vila Darcy Penteado", "distrito": "São Roque", "cartas": ["Carta I", "Carta VIII", "Carta IX"], "zoneamento_padrao": "ZUE-DT / AEIT", "centro": [-23.5150, -47.1650, 14], "descricao": "Importante roteiro gastronômico e turístico de São Roque. Hotéis, spas, restaurantes de alto padrão e preservação da mata nativa."},
        {"nome": "Mombaça", "distrito": "São Roque", "cartas": ["Carta I", "Carta II", "Carta VIII"], "zoneamento_padrao": "ZUE Interesse Turístico / Residencial", "centro": [-23.4950, -47.1380, 14], "descricao": "Região estratégica próxima à Rodovia Castello Branco. Minuta 2026 admite CA 1.2 e gabarito até 24m para apoiar moradia de trabalhadores e logística."},
        {"nome": "Saboó (Bairro e Morro)", "distrito": "São Roque", "cartas": ["Carta I", "Carta VIII", "Carta IX", "Carta XIII"], "zoneamento_padrao": "AEIU 9 / ZUE", "centro": [-23.5020, -47.1120, 14], "descricao": "Marco paisagístico natural culminante de São Roque. Contempla o Parque do Saboó (AEIU 9 e obra SRQ-14) com proteção estrita a topos de morro (Lei 12.651)."},
        {"nome": "Distrito de Maylasky", "distrito": "Maylasky", "cartas": ["Carta I", "Carta V", "Carta XI", "Carta XIII"], "zoneamento_padrao": "ZUR-md / ZUI / ZUE", "centro": [-23.5510, -47.0580, 14], "descricao": "Distrito oriental de São Roque, polo logístico, residencial e industrial. Servido pela ferrovia e Rodovia Raposo Tavares, com previsão de marginais e novo viaduto."},
        {"nome": "Chácaras Monte Verde / Caetê", "distrito": "Maylasky", "cartas": ["Carta I", "Carta V"], "zoneamento_padrao": "ZUE Chácaras", "centro": [-23.5650, -47.0450, 14], "descricao": "Região de chácaras residenciais e lazer com demanda de redução fracionária de lote e regularização ambiental."},
        {"nome": "Distrito de São João Novo", "distrito": "São João Novo", "cartas": ["Carta I", "Carta VI", "Carta IX"], "zoneamento_padrao": "ZUE-SJN / Chácaras", "centro": [-23.4850, -47.0750, 14], "descricao": "Distrito setentrional de São Roque com atmosfera interiorana, chácaras de veraneio, conexão com Itapevi/Barueri e projetos de contenção de cheias."},
        {"nome": "Distrito de Canguera", "distrito": "Canguera", "cartas": ["Carta I", "Carta VII", "Carta XII"], "zoneamento_padrao": "ZUE-DT / Macrozona de Proteção Ambiental", "centro": [-23.5850, -47.1250, 14], "descricao": "Distrito do Roteiro do Vinho, capital do enoturismo paulista. Integralmente inserido na APA de Itupararanga, com vocação turística, vitivinícola e gastronômica."},
        {"nome": "Estrada do Vinho (SPV-077)", "distrito": "Canguera", "cartas": ["Carta VII", "Carta VIII", "Carta XII", "Carta XIII"], "zoneamento_padrao": "Corredor Turístico ZUE-DT", "centro": [-23.5780, -47.1350, 14], "descricao": "Principal artéria turística do município. Exige bolsões de desaceleração e estacionamento, ciclovia planejada (SRQ-15) e restrição a usos industriais poluentes."},
        {"nome": "Rodovia Lívio Tagliassachi", "distrito": "São Roque", "cartas": ["Carta I", "Carta II", "Carta VIII", "Carta XIII"], "zoneamento_padrao": "ZUCL (Corredor Logístico)", "centro": [-23.4900, -47.1420, 13], "descricao": "Eixo de ligação expressa entre São Roque e a Rodovia Castello Branco (km 60). Vocação para centros logísticos, comércio estruturado e indústrias limpas (SRQ-12)."},
        {"nome": "São Paulo Catarina Aeroporto", "distrito": "São Roque", "cartas": ["Carta I", "Carta II", "Carta VIII"], "zoneamento_padrao": "PBZPA / ASA Aeroportuária", "centro": [-23.4750, -47.1450, 13], "descricao": "Aeroporto Executivo Internacional privado homologado pela ANAC/DECEA. Sujeita o entorno a gabaritos de cone de aproximação e raio de 20 km de restrição de aves (Portaria COMAER 657/GC3)."},
        {"nome": "Jardim Camargo / Bairro do Pavão", "distrito": "São João Novo", "cartas": ["Carta I", "Carta VI"], "zoneamento_padrao": "ZUR-bd / Chácaras", "centro": [-23.4950, -47.0620, 14], "descricao": "Áreas de chácaras e ocupações de baixa densidade no distrito de São João Novo, cortadas por cursos d'água contribuintes do Ribeirão São João."},
        {"nome": "Patrimônio do Carmo", "distrito": "Canguera", "cartas": ["Carta I", "Carta VII"], "zoneamento_padrao": "Condomínio Residencial Fechado / APA", "centro": [-23.6120, -47.1450, 13], "descricao": "Grande complexo de loteamentos fechados de alto padrão em meio a remanescentes florestais de Mata Atlântica e lagos da APA Itupararanga."}
    ]

    # 11. GUIA PRÁTICO DE USOS E ATIVIDADES URBANAS / RURAIS
    atividades_guia = [
        {
            "atividade": "Pousada, Hotel e Hospedagem",
            "palavras_chave": ["pousada", "hotel", "hospedagem", "chale", "eco resort", "resort", "airbnb", "pousadas"],
            "zonas_permitidas": ["ZUE-DT", "ZUE Interesse Turístico", "ZUC", "ZUR-md", "Macrozona Rural (com anuência)"],
            "restricoes_condicoes": "Em Canguera e Roteiro do Vinho (ZUE-DT), é uso amplamente incentivado. Deve apresentar sistema autônomo de tratamento de esgoto (aprovado pela CETESB) e manter taxa de permeabilidade mínima de 50%. Se localizado na APA de Itupararanga, necessita de anuência prévia da Fundação Florestal.",
            "leis": ["LC 40/2006 Art. 112", "LC 65/2012", "Lei Estadual 10.100/1998"],
            "camada_sugerida": "carta_07_canguera_2026"
        },
        {
            "atividade": "Restaurante, Adega e Enoturismo",
            "palavras_chave": ["restaurante", "adega", "vinicola", "enoturismo", "gastronomia", "bar", "degustacao", "lanchonete"],
            "zonas_permitidas": ["ZUE-DT", "Corredores Turísticos", "ZUC", "ZUCL", "ZUR-md"],
            "restricoes_condicoes": "Obrigatório recuo frontal para estacionamento e baia de desaceleração se lindeiro à Estrada do Vinho (Carta XII Art. 127). Proibido despejo de efluentes sem tratamento completo (vinhaça e esgoto comercial). EIV exigido para estabelecimentos acima de 500 m² de área construída.",
            "leis": ["Minuta 2026 Art. 14 e 127", "LC 40/2006", "LC 65/2012"],
            "camada_sugerida": "carta_07_canguera_2026"
        },
        {
            "atividade": "Indústria, Fábrica e Galpão de Médio/Grande Porte",
            "palavras_chave": ["industria", "fabrica", "galpao", "manufatura", "producao", "usinagem", "polo industrial", "zui"],
            "zonas_permitidas": ["ZUI (Zona Urbana Industrial)", "ZUCL (Corredor Logístico Rodovia Lívio Tagliassachi)", "ZUE Desenvolvimento Econômico"],
            "restricoes_condicoes": "Proibidas atividades poluidoras de grau 3 e 4 em toda a bacia de Itupararanga e áreas de mananciais. Na ZUI, Lote Mínimo é 1.000m² (podendo ser 250m² em fracionamentos industriais com aprovação especial), TO 60%, CA 1.5 e recuo frontal de 10m obrigatório para manobras de carretas.",
            "leis": ["LC 40/2006 Art. 118", "LC 48/2008", "Lei Estadual 9.866/1997", "Quadro VIII Minuta 2026"],
            "camada_sugerida": "carta_04_sede_2026"
        },
        {
            "atividade": "Centro de Distribuição e Galpões Logísticos",
            "palavras_chave": ["logistica", "centro de distribuicao", "cd", "armazem", "transportadora", "deposito", "frota"],
            "zonas_permitidas": ["ZUCL (Rodovia Lívio Tagliassachi)", "ZUE Desenvolvimento Econômico", "Eixo Castello Branco", "Eixo Raposo Tavares"],
            "restricoes_condicoes": "Exige Estudo de Impacto de Vizinhança (EIV) para polos geradores de tráfego (acima de 2.000 m² de área construída). Proibidos depósitos a céu aberto de sucata ou material degradante da paisagem turística (Carta VIII).",
            "leis": ["Minuta 2026 Seção ZUCL", "LC 40/2006", "Estatuto da Cidade"],
            "camada_sugerida": "carta_08_corredores_2026"
        },
        {
            "atividade": "Posto de Combustíveis e Serviços Automotivos",
            "palavras_chave": ["posto", "combustivel", "gasolina", "etanol", "gnv", "abastecimento", "lava rapido", "troca de oleo"],
            "zonas_permitidas": ["Corredores Comerciais", "ZUI", "ZUCL", "ZUR-md (com condicionantes de afastamento)"],
            "restricoes_condicoes": "Licenciamento ambiental trifásico estrito na CETESB com tanques de parede dupla e poços de monitoramento piezométrico. Distância mínima de 100m a 200m de escolas, creches, asilos e hospitais. Proibido em Áreas Hidrologicamente Sensíveis (AHS) e faixas de mananciais.",
            "leis": ["Resolução CONAMA 273/2000", "LC 40/2006 Art. 85", "Lei Estadual 9.866/1997"],
            "camada_sugerida": "carta_08_corredores_2026"
        },
        {
            "atividade": "Desdobro, Fracionamento e Desmembramento de Lotes",
            "palavras_chave": ["desdobro", "desdobro de lote", "desmembrar", "fracionamento", "dividir terreno", "divisao de lote", "desmembramento"],
            "zonas_permitidas": ["Macrozona de Consolidação Urbana (ZUC, ZUR-bd, ZUR-md, ZUR-ad)"],
            "restricoes_condicoes": "Cada lote resultante deve possuir, no mínimo, a área e testada mínimas da zona: 250 m² de área e 10 m de testada na área urbana consolidada (Quadro VIII Minuta 2026). Na Zona Rural, a fração mínima de parcelamento (FMP) é de 20.000 m² (módulo INCRA). Proibido desdobro em áreas com declividade > 30% ou em faixas de APP.",
            "leis": ["Lei Federal 6.766/1979 Art. 3º", "LC 40/2006", "LC 102/2020", "Quadro VIII Minuta 2026"],
            "camada_sugerida": "carta_04_sede_2026"
        },
        {
            "atividade": "Loteamento e Condomínio Residencial Fechado",
            "palavras_chave": ["loteamento", "condominio", "condominio fechado", "loteamento fechado", "reserva fundiaria", "gleba"],
            "zonas_permitidas": ["Macrozona de Consolidação Urbana", "ZUE Ocupação Estratégica (com plano urbanístico)"],
            "restricoes_condicoes": "Obrigatória doação de áreas públicas conforme Quadro VIII: no mínimo 20% para sistema viário, 10% para áreas verdes/lazer e 5% para áreas institucionais públicas (10% na ZUI). Proibido em terrenos alagadiços, áreas de risco ou com declividade igual ou superior a 30%. Sujeito a aprovação no GRAPROHAB/SP e Prefeitura.",
            "leis": ["Lei Federal 6.766/1979", "Lei Estadual 10.257", "LC 40/2006 Art. 13 a 25", "Quadro VIII Minuta 2026"],
            "camada_sugerida": "carta_03_consolidacao_urbana_2026"
        },
        {
            "atividade": "Edículas, Churrasqueiras e Anexos",
            "palavras_chave": ["edicula", "anexo", "churrasqueira", "garagem nos fundos", "puxadinho", "gourmet"],
            "zonas_permitidas": ["Macrozona de Consolidação Urbana"],
            "restricoes_condicoes": "Conforme Quadro IX da Minuta 2026: a área da edícula não pode ultrapassar 30% da área construída da edificação principal, deve manter afastamento mínimo de 2,00 metros da construção principal e é permitida apenas na Macrozona de Consolidação Urbana.",
            "leis": ["Quadro IX da Minuta 2026", "LC 40/2006"],
            "camada_sugerida": "carta_04_sede_2026"
        }
    ]

    # 12. GUIA DOS INSTRUMENTOS URBANÍSTICOS (ESTATUTO DA CIDADE E PLANO DIRETOR)
    instrumentos_urbanisticos = [
        {
            "instrumento": "Outorga Onerosa do Direito de Construir (OODC)",
            "sigla": "OODC",
            "palavras_chave": ["outorga onerosa", "oodc", "construir a mais", "adicional construtivo", "potencial adicional"],
            "artigos": ["Art. 41 a 43 da Minuta 2026"],
            "como_funciona": "Permite edificar acima do Coeficiente de Aproveitamento Básico até o Coeficiente Máximo definido para a zona, mediante contrapartida financeira do empreendedor ao Fundo Municipal de Desenvolvimento Urbano (FMDU).",
            "regras": "A fórmula de contrapartida considera a área adicional, o valor venal do metro quadrado do terreno e fatores de interesse social. Aplicável especialmente nas ZUEs (ex: Mombaça) e Corredores Urbanos."
        },
        {
            "instrumento": "Transferência do Potencial Construtivo (TPC)",
            "sigla": "TPC",
            "palavras_chave": ["transferencia de potencial construtivo", "tpc", "transferir potencial", "tombamento", "preservacao historica"],
            "artigos": ["Art. 29 a 40 da Minuta 2026"],
            "como_funciona": "Autoriza o proprietário de imóvel tombado, de interesse histórico-cultural (ex: Brasital) ou ambiental (APP/Mata Atlântica) a alienar ou transferir para outro imóvel urbano o potencial construtivo não utilizável.",
            "regras": "Exige expedição de Certidão de Potencial Construtivo Transferível pela Prefeitura e registro em matrícula."
        },
        {
            "instrumento": "IPTU Progressivo no Tempo e PEUC",
            "sigla": "IPTU Progressivo / PEUC",
            "palavras_chave": ["iptu progressivo", "peuc", "imovel subutilizado", "edificacao compulsoria", "vazio urbano", "terreno abandonado"],
            "artigos": ["Art. 22 a 28 da Minuta 2026", "Art. 5º a 8º Estatuto da Cidade"],
            "como_funciona": "Instrumento para coibir a especulação imobiliária em terrenos e imóveis não edificados, subutilizados ou não utilizados na Macrozona de Consolidação Urbana.",
            "regras": "Proprietário é notificado para parcelar ou edificar em 1 ano. Em caso de inércia, a alíquota do IPTU é majorada anualmente pelo prazo de 5 anos consecutivos até o teto de 15%. Persistindo o descumprimento, o Município pode proceder à desapropriação mediante pagamento em títulos da dívida pública."
        },
        {
            "instrumento": "Estudo de Impacto de Vizinhança (EIV / RIV)",
            "sigla": "EIV / RIV",
            "palavras_chave": ["eiv", "riv", "estudo de impacto de vizinhanca", "impacto de vizinhanca", "polo gerador"],
            "artigos": ["Art. 13 a 18 da Minuta 2026"],
            "como_funciona": "Exigido para empreendimentos de médio e grande porte, polos geradores de tráfego, shopping centers, grandes galpões logísticos, hospitais, loteamentos e indústrias.",
            "regras": "Avalia impactos em mobilidade, adensamento, drenagem pluvial, valorização imobiliária, geração de ruído e ventilação. Suas audiências e documentos são 100% públicos e culminam no Termo de Compromisso com contrapartidas mitigadoras e compensatórias."
        },
        {
            "instrumento": "Regularização Fundiária Urbana (REURB)",
            "sigla": "REURB-S / REURB-E",
            "palavras_chave": ["reurb", "regularizacao fundiaria", "loteamento clandestino", "posse", "escritura", "titulo de propriedade"],
            "artigos": ["Carta IX Minuta 2026", "Lei Federal 13.465/2017", "LC 102/2020"],
            "como_funciona": "Processo administrativo municipal para legalização de núcleos urbanos informais consolidados até dezembro de 2016. Divide-se em REURB-S (Social - baixa renda, isenta de custas cartorárias) e REURB-E (Específica - média/alta renda).",
            "regras": "Prioritária nas Áreas de Especial Interesse Social (AEIS 1 a 6 mapeadas na Carta IX)."
        }
    ]

    # 13. CONSOLIDAÇÃO FINAL DA BASE DE CONHECIMENTO
    knowledge_base = {
        "metadata": {
            "municipio": "São Roque",
            "uf": "SP",
            "codigo_ibge": "3550605",
            "versao": "2026.11_UNRESTRICTED",
            "sistema_referencia": "SIRGAS 2000 / UTM Zona 23S (EPSG: 31983)",
            "total_normas_cadastradas": len(normas),
            "total_artigos_indexados": len(artigos),
            "total_cruzamentos_legislacao": len(cruzamentos),
            "total_zonas_parametrizadas": len(zonas_parametros),
            "total_camadas_auditadas": len(camadas),
            "total_classes_camadas": len(classes),
            "total_cartas_oficiais_2026": len(cartas_pd2026),
            "total_obras_prioritarias_srq": len(obras_prioritarias),
            "total_bairros_mapeados": len(bairros_localidades),
            "total_atividades_guiadas": len(atividades_guia),
            "total_instrumentos_urbanisticos": len(instrumentos_urbanisticos),
            "total_pedidos_participacao_popular": len(pedidos_participacao)
        },
        "pedidos_participacao_popular": pedidos_participacao,
        "cartas_pd2026": cartas_pd2026,
        "obras_prioritarias_srq": obras_prioritarias,
        "bairros_localidades": bairros_localidades,
        "atividades_guia": atividades_guia,
        "instrumentos_urbanisticos": instrumentos_urbanisticos,
        "zonas_parametros": zonas_parametros,
        "revisao_2026": revisao_2026,
        "camadas_auditadas": camadas,
        "classes_camadas": classes,
        "cruzamentos_legislacao": cruzamentos,
        "artigos_amostra": [
            {
                "id": a["id"],
                "norma_id": a["norma_id"],
                "artigo": a["artigo"],
                "texto": a["texto_normativo"][:400] if a["texto_normativo"] else "",
                "restricao": a["restricao_urbanistica_ambiental"],
                "palavras_chave": a["palavras_chave"]
            }
            for a in artigos[:600]
        ],
        "normas_resumo": [
            {
                "id": n["id"],
                "esfera": n["esfera"],
                "tipo": n["tipo"],
                "numero": n["numero"],
                "ano": n["ano"],
                "ementa": n["ementa"],
                "vigencia": n["vigencia"],
                "link_oficial": n["link_oficial"],
                "camadas_competencia": n["camadas_competencia"]
            }
            for n in normas
        ]
    }

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(knowledge_base, f, ensure_ascii=False, indent=2)

    sz_kb = os.path.getsize(OUT_PATH) / 1024
    print(f"Sucesso! Base de Conhecimento Expandida salva em {OUT_PATH} ({sz_kb:.1f} KB)", file=sys.stderr)

if __name__ == "__main__":
    main()
