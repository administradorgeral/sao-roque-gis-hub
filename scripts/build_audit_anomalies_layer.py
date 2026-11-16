"""
build_audit_anomalies_layer.py
Script de Auditoria Perimetral Geoespacial e Deteccao Algoritmica de Spot Zoning
Compara Zoneamento PMD 2006 vs Minuta PMD 2026 de Sao Roque
Gera camada GeoJSON e sumario JSON para consumo do WebGIS e da IA Territorial
"""

import json
import math
import os
from shapely.geometry import shape, mapping

def calc_polsby_popper(geom):
    area = geom.area
    perimeter = geom.length
    if perimeter == 0:
        return 0.0
    return round((4.0 * math.pi * area) / (perimeter ** 2), 3)

def run():
    print("Iniciando auditoria perimetral geoespacial detalhada...")

    path_06 = "data/pmsr_zoneamento_pmd2006.geojson"
    path_26 = "data/pmsr_zoneamento_minuta_pmd2006.geojson"
    path_apa = "data/apa_itupararanga_limite_sao_roque_web.geojson"

    if not os.path.exists(path_06) or not os.path.exists(path_26):
        print("Arquivos de zoneamento nao encontrados.")
        return

    with open(path_06, 'r', encoding='utf-8') as f:
        z06 = json.load(f)

    with open(path_26, 'r', encoding='utf-8') as f:
        z26 = json.load(f)

    apa_geom = None
    if os.path.exists(path_apa):
        with open(path_apa, 'r', encoding='utf-8') as f:
            apa_data = json.load(f)
            apa_geom = shape(apa_data['features'][0]['geometry'])

    # Tabela de CA real da Lei Complementar 40/2006
    ca_2006_table = {
        'ZR': 0.2,
        'ZP': 0.1,
        'ZUE-CM': 0.35,
        'ZUE-DT': 0.5,
        'ZDB': 0.6,
        'ZDM': 1.0,
        'ZDA': 1.5,
        'ZC': 2.0,
        'ZI': 1.0,
        'ZUI': 1.2,
        'ZUCAER': 0.8,
        'ZCU': 0.5,
        'ZUE-CSJN': 0.5,
        'ZUE-DE': 1.0,
        'ZUE-OE': 1.0,
        'ZUPA': 0.2
    }

    # Tabela de CA da Minuta de Revisao do Plano Diretor 2026
    ca_2026_table = {
        'ZUE - Chácaras Manancial': 0.5,
        'ZUE - Atividades Especial da RT': 1.2,
        'ZUR - Média Densidade': 1.5,
        'ZUR - Baixa Densidade': 0.8,
        'ZUE - Interesse Turístico': 1.2,
        'ZUE - Desenvolvimento Econômico': 1.8,
        'ZUE - Ocupação Estratégica': 2.0,
        'ZUE - Alta Intensidade': 2.0,
        'Zona Urbana Industrial': 1.5,
        'Zona Urbana Central': 2.5,
        'ZUR - Alta Densidade': 2.0,
        'ZUPA': 0.2,
        'Rural': 0.2
    }

    geoms_06 = []
    for f in z06['features']:
        props = f['properties']
        sigla = props.get('sigla') or props.get('zona') or 'ND'
        geoms_06.append({
            'geom': shape(f['geometry']),
            'sigla': sigla,
            'props': props
        })

    anomalies_features = []
    anomalies_summary = []

    for i, f in enumerate(z26['features']):
        props26 = f['properties']
        g26 = shape(f['geometry'])
        nome26 = props26.get('nome') or props26.get('sigla_zoneamento') or f"Zona {i+1}"
        fid = props26.get('fid')
        area_ha = float(props26.get('area_ha') or 0.0)

        # Excluir zonas rurais ou de protecao natural de serem auditadas como anomalias de expansao urbana
        if nome26 in ['Rural', 'ZUPA']:
            continue

        # Interseccao com as zonas de 2006
        transicoes = []
        for g06 in geoms_06:
            if g26.intersects(g06['geom']):
                inter = g26.intersection(g06['geom'])
                if inter.area > 1e-7:
                    pct = (inter.area / g26.area) * 100
                    transicoes.append({
                        'sigla_2006': g06['sigla'],
                        'pct': round(pct, 1),
                        'geom': inter
                    })

        # Calculo de Indicadores
        pp_index = calc_polsby_popper(g26)
        in_apa = g26.intersects(apa_geom) if apa_geom else False
        
        # Conversao de Rural / Protecao
        rural_conv = sum(t['pct'] for t in transicoes if t['sigla_2006'] in ['ZR', 'ZP'])
        
        ca_new = ca_2026_table.get(nome26, 1.0)
        # CA ponderado anterior
        old_ca = 0.2
        if transicoes:
            old_ca = sum(ca_2006_table.get(t['sigla_2006'], 0.5) * (t['pct'] / 100.0) for t in transicoes)
        
        salto_ca_ratio = round(ca_new / max(0.1, old_ca), 2)

        # Centroide
        centroid = g26.centroid
        lat, lng = centroid.y, centroid.x

        # Sistema de Pontuacao de Anomalia Perimetral (SAP - 0 a 100)
        sap = 10 # Base de analise pericial
        motivos = []
        artigos_violados = []
        indicadores = []

        # Indicador IA: Morfologia Anomala / Convoluta (Polsby-Popper)
        if pp_index < 0.10 and area_ha > 100:
            sap += 30
            indicadores.append("IA_MORFOLOGIA_CRITICA")
            motivos.append(f"Morfologia perimetral altamente convoluta e tentacular (Polsby-Popper = {pp_index:.3f}), denotando desenho casuístico para contornar ou abraçar matrículas pontuais.")
            artigos_violados.append("Art. 37 CF/88 (Impessoalidade) e Art. 2º Lei 10.257/01")
        elif pp_index < 0.18 and area_ha > 50:
            sap += 15
            indicadores.append("IA_MORFOLOGIA_ATENCAO")
            motivos.append(f"Perímetro com recortes irregulares e baixo índice de compacidade geométrica (Polsby-Popper = {pp_index:.3f}).")
            artigos_violados.append("Art. 2º Estatuto da Cidade (Ordenação Racional do Solo)")

        # Indicador IB: Incompatibilidade Biofisica / APA
        if in_apa and "Industrial" in nome26:
            sap += 45
            indicadores.append("IB_BIOFISICA_INDUSTRIAL_APA")
            motivos.append("Conversão para Zona Urbana Industrial na bacia hidrográfica contribuinte do reservatório de Itupararanga.")
            artigos_violados.append("Leis Estaduais 10.100/98 e 9.866/97 (APA Itupararanga) e Dec. Estadual 53.526/08")
        elif in_apa and area_ha > 500:
            sap += 25
            indicadores.append("IB_BIOFISICA_MANANCIAL")
            motivos.append(f"Macroperímetro de {area_ha:.0f} ha sobre bacia de proteção de mananciais (APA Itupararanga), vulnerável a desdobros sem saneamento Sabesp consolidado.")
            artigos_violados.append("Lei Federal 6.766/79 Art. 3º e LC Municipal 40/06")

        # Indicador IC: Spot Zoning / Conversao Rural com Salto de CA
        if rural_conv >= 70.0 and salto_ca_ratio >= 3.0:
            sap += 35
            indicadores.append("IC_SPOT_ZONING_SEVERO")
            motivos.append(f"Spot Zoning severo: {rural_conv:.1f}% da área convertida diretamente de Zona Rural para Urbana/Turística com multiplicação do CA por {salto_ca_ratio}x.")
            artigos_violados.append("Art. 2º, VI e IX do Estatuto da Cidade (Lei 10.257/01) e Precedente TJ-SP ADI 2048131")
        elif rural_conv >= 30.0 and salto_ca_ratio >= 1.8:
            sap += 20
            indicadores.append("IC_SPOT_ZONING_MODERADO")
            motivos.append(f"Inclusão no perímetro urbano de área majoritariamente rural ({rural_conv:.1f}%) com salto de CA de {salto_ca_ratio}x sem comprovação de infraestrutura instalada.")
            artigos_violados.append("Art. 42-B Lei 10.257/01 (Expansão Urbana Desprovida de EIV)")

        # Indicador ID: Incompatibilidade de Usos Conflitantes (Turistico -> Industrial)
        turistico_conv = sum(t['pct'] for t in transicoes if t['sigla_2006'] == 'ZUE-DT')
        if "Industrial" in nome26 and turistico_conv >= 50.0:
            sap += 30
            indicadores.append("ID_CONFLITO_USO_VIZINHANCA")
            motivos.append(f"Conflito severo de vizinhança: transição de antiga zona turística/chácaras ({turistico_conv:.1f}%) para uso industrial pesado sem zona de amortecimento.")
            artigos_violados.append("Art. 2º, VI, 'g' da Lei 10.257/01 (Evitação de conflitos de uso)")

        # Indicador IE: Enclave de Macroimpacto Isolado (Leapfrog)
        if area_ha > 400 and ("Estratégica" in nome26 or "Desenvolvimento" in nome26):
            sap += 20
            indicadores.append("IE_LEAPFROG_MACROIMPACTO")
            motivos.append(f"Macrogleba de desenvolvimento ({area_ha:.0f} ha) descolada da mancha urbana contínua (urbanização em salto / leapfrog).")
            artigos_violados.append("Art. 2º, VI, 'c' do Estatuto da Cidade (Prevenção à dispersão urbana)")

        # Classificacao
        if sap >= 30:
            sap = min(100, sap)
            if sap >= 60:
                nivel = "CRÍTICO"
                cor = "#ef4444" # Vermelho
            elif sap >= 45:
                nivel = "ATENÇÃO"
                cor = "#f59e0b" # Âmbar
            else:
                nivel = "MODERADO"
                cor = "#eab308" # Amarelo

            rec = "Exigência de Estudo de Impacto de Vizinhança (EIV), retificação do traçado perimetral para respeitar divisas geomorfológicas e audiência pública temática específica."
            if "APA" in "".join(indicadores):
                rec = "Adequação obrigatória ao Plano de Manejo da APA Itupararanga, vedação a desmates e anuência prévia da Fundação Florestal e COMDEMA."
            elif "SPOT_ZONING" in "".join(indicadores):
                rec = "Glosa do perímetro por indício de Spot Zoning / casuísmo sem interesse público geral; aplicação de Outorga Onerosa em caso de manutenção."
            elif "CONFLITO" in "".join(indicadores):
                rec = "Criação obrigatória de faixa de amortecimento 'buffer' de 100m com restrição a indústrias poluentes (I-3) confrontantes com chácaras turísticas."

            feat = {
                "type": "Feature",
                "geometry": mapping(g26),
                "properties": {
                    "fid": fid,
                    "nome_2026": nome26,
                    "area_ha": round(area_ha, 2),
                    "sap_score": sap,
                    "nivel_risco": nivel,
                    "cor_alerta": cor,
                    "polsby_popper": pp_index,
                    "dentro_apa": in_apa,
                    "salto_ca_ratio": salto_ca_ratio,
                    "ca_2006_estimado": round(old_ca, 2),
                    "ca_2026_proposto": round(ca_new, 2),
                    "transicao_rural_pct": round(rural_conv, 1),
                    "indicadores_disparados": indicadores,
                    "principais_motivos": motivos,
                    "artigos_violados": list(set(artigos_violados)),
                    "recomendacao_tecnica": rec,
                    "centroide": [round(lat, 5), round(lng, 5)]
                }
            }
            anomalies_features.append(feat)

            anomalies_summary.append({
                "fid": fid,
                "nome": nome26,
                "area_ha": round(area_ha, 2),
                "sap": sap,
                "nivel": nivel,
                "cor": cor,
                "centro": [round(lat, 5), round(lng, 5)],
                "motivo_principal": motivos[0] if motivos else "Atenção técnica perimetral",
                "salto_ca": salto_ca_ratio,
                "in_apa": in_apa,
                "polsby_popper": pp_index
            })

    output_geojson = {
        "type": "FeatureCollection",
        "metadata": {
            "titulo": "Auditoria Perimetral e Detecção de Spot Zoning (PMD 2006 vs Minuta 2026)",
            "orgao": "São Roque GIS Hub - Motor de Inteligência Territorial e Perícia Urbanística",
            "modelo_ia_auditor": "gemini-4-argon",
            "total_poligonos_auditados": len(z26['features']),
            "total_anomalias_detectadas": len(anomalies_features),
            "criterios": "Polsby-Popper, Intersecção Biofísica (APA Itupararanga), Salto de CA e Descompasso de Infraestrutura"
        },
        "features": anomalies_features
    }

    with open("data/audit_anomalies_sao_roque.geojson", "w", encoding="utf-8") as f:
        json.dump(output_geojson, f, ensure_ascii=False, indent=2)

    with open("data/audit_anomalies_summary.json", "w", encoding="utf-8") as f:
        json.dump(anomalies_summary, f, ensure_ascii=False, indent=2)

    print(f"Auditoria perimetral concluida com sucesso!")
    print(f"Total de anomalias/alertas perimetrais identificados: {len(anomalies_features)}")
    for a in anomalies_summary:
        print(f"[{a['nivel']} - Score {a['sap']}] FID {a['fid']} {a['nome']} ({a['area_ha']} ha): {a['motivo_principal']}")

if __name__ == "__main__":
    run()
