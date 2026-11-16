import sqlite3
import json

db_path = r'C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\dados_oficiais\sao_roque_geodados.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 1. Inserir camada mestre
cursor.execute("""
INSERT OR REPLACE INTO camadas_territoriais (
    id, nome, titulo_documento, categoria, arquivo_origem, tipo_camada,
    escala_nominal, datum_projecao, data_elaboracao,
    responsavel_tecnico, responsavel_crea, desenho_tecnico, desenho_crea,
    fonte_cartografica, status_auditoria,
    bbox_utm_x0, bbox_utm_x1, bbox_utm_y0, bbox_utm_y1,
    bounds_wgs84_json, alerta_juridico
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    "declividade",
    "Declividade do Terreno",
    "ANEXO 4.3.3-1 - MAPA DE DECLIVIDADE DO MUNICÍPIO DE SÃO ROQUE",
    "Geotécnica e Geomorfologia",
    "40537_4_3_3_1 Declividade.pdf",
    "vetor_poligonos",
    "1:50.000",
    "SIRGAS 2000 UTM Zone 23S",
    "11/11/2018",
    "Maurício Scorsatto Sartori (Eng. Florestal)",
    "5.060.532.187",
    "Ana Clara Cerminaro (Analista de Geoprocessamento)",
    "473.423.455",
    "IGC. Instituto Geográfico e Cartográfico de São Paulo. Cartas Planialtimétricas 1:10.000 (Folhas 89 a 98, 1978)",
    "Auditado com Sucesso (Identificado Ponto Cego Legal dos 30% e Confusão 45% vs 45° APP)",
    270308.48, 299278.55, 7382234.44, 7410187.57,
    json.dumps({"sw": [-23.65430, -47.25190], "ne": [-23.40582, -46.96427]}),
    "O mapa original utiliza a classificação pedológica de Lepsch (1983) / Embrapa (agronômica), que agrupa 20% a 45% como 'Forte Ondulado'. Contudo, a Lei Federal nº 6.766/79 (Art. 3º) e a LC Municipal nº 40/2006 (Art. 13 e 43) vedam expressamente o parcelamento e condomínios em rampas > 30%, criando um ponto cego no intervalo de 30% a 45%. Além disso, encostas em APP (Lei 12.651/12, Art. 4º, V) exigem > 45 GRAUS (100%), não 45%."
))

# 2. Inserir classes
classes = [
    ("CL_1_PLANO", "Plano (0 a 3%)", "0° a 1.7°", "#FFFF73", "RGB(255, 255, 115)", "Lepsch (1983) / Embrapa Pedologia", "Apto para edificação, loteamento regular e infraestrutura urbana sem restrição topográfica."),
    ("CL_2_SUAVE", "Suave ondulado (3 a 8%)", "1.7° a 4.6°", "#FFFF00", "RGB(255, 255, 0)", "Lepsch (1983) / Embrapa Pedologia", "Apto para vias públicas e equipamentos comunitários. Exige controle padrão de escoamento superficial."),
    ("CL_3_ONDULADO", "Ondulado (8 a 20%)", "4.6° a 11.3°", "#FFAA00", "RGB(255, 170, 0)", "Lepsch (1983) / Embrapa Pedologia", "Exige terraplenagem contida e drenagem profunda. Rampa viária máxima em São Roque é 15% (LC 40/2006 Art. 32)."),
    ("CL_4_FORTE_ONDULADO", "Forte ondulado (20 a 45%)", "11.3° a 24.2°", "#FF5500", "RGB(255, 85, 0)", "Lepsch (1983) / Embrapa Pedologia", "ZONA DE RESTRIÇÃO SEVERA: No trecho entre 30% e 45%, a legislação municipal e federal PROÍBE parcelamento do solo e condomínios."),
    ("CL_5_MONTANHOSO", "Montanhoso (45 a 75%)", "24.2° a 36.9° (ou > 45° / 100%)", "#E60000", "RGB(230, 0, 0)", "Lepsch (1983) / Embrapa Pedologia", "Risco gravíssimo de escorregamento de massa. Encostas com rampa > 100% (> 45°) constituem APP inalienável (Lei 12.651/12).")
]

cursor.execute("DELETE FROM classes_camada_territorial WHERE camada_id = 'declividade'")
for c in classes:
    cursor.execute("""
    INSERT INTO classes_camada_territorial (
        camada_id, codigo_classe, nome_classe, angulo_equivalente, cor_hex, cor_rgb, metodologia_referencia, implicacao_pratica
    ) VALUES ('declividade', ?, ?, ?, ?, ?, ?, ?)
    """, c)

# 3. Inserir cruzamento jurídico
cursor.execute("DELETE FROM cruzamento_camada_legislacao WHERE camada_id = 'declividade'")
cruzamentos = [
    ("declividade", "Federal", "Lei Ordinária", "6766", 1979, "Art. 3º, parágrafo único, I", "Impeditiva",
     "Não será permitido o parcelamento do solo em terrenos com declividade igual ou superior a 30% (trinta por cento).",
     "PONTO CEGO NO MAPA: A classe 'Forte Ondulado' do PDF agrupa 20% a 45%, ocultando o limite exato dos 30%."),
     
    ("declividade", "Municipal", "Lei Complementar", "40", 2006, "Art. 13, inciso VI", "Impeditiva",
     "É vedado o parcelamento do solo para fins urbanos em terrenos com declividade igual ou superior a 30% em todo o território de São Roque.",
     "Conflito direto com a classe 'Forte Ondulado (20 a 45%)'."),
     
    ("declividade", "Municipal", "Lei Complementar", "40", 2006, "Art. 43, inciso VI", "Impeditiva",
     "É vedada a implantação de condomínios urbanísticos em terrenos com declividade igual ou superior a 30%.",
     "Regra de bloqueio automático para loteamentos fechados."),
     
    ("declividade", "Municipal", "Lei Complementar", "40", 2006, "Art. 32", "Condicionante",
     "A rampa máxima longitudinal das vias públicas projetadas não poderá exceder 15%, admitindo-se 20% em trechos excepcionais de até 50m.",
     "Aplica-se nas classes Ondulado (8-20%) e Forte Ondulado (20-45%)."),
     
    ("declividade", "Federal", "Lei Ordinária", "12651", 2012, "Art. 4º, inciso V", "Impeditiva",
     "Considera-se Área de Preservação Permanente (APP) as encostas ou partes destas com declividade superior a 45° (quarenta e cinco graus, equivalente a 100%).",
     "ALERTA CONCEITUAL: 45° (graus) = 100% de declividade. Não confundir com 45% (que são apenas 24.2°).")
]

for cr in cruzamentos:
    cursor.execute("""
    INSERT INTO cruzamento_camada_legislacao (
        camada_id, norma_esfera, norma_tipo, norma_numero, norma_ano, artigo_dispositivo, grau_restricao, regra_aplicacao, conflito_ou_ponto_atencao
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, cr)

conn.commit()
print("Metadados, classes e cruzamento jurídico de 'declividade' inseridos com sucesso!")
conn.close()
