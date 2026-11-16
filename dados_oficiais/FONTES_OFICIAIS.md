# Registro e Proveniência de Fontes Oficiais — São Roque (SP)
**Código IBGE:** 3550605 | **Datum Oficial:** SIRGAS 2000 (EPSG: 31983 - UTM Fuso 23S)

Este repositório documenta de forma auditável e transparente todas as fontes oficiais federais, estaduais e municipais que alimentam a Central de Inteligência Cartográfica de São Roque.

---

## 1. Esfera Municipal (Prefeitura da Estância Turística de São Roque)

### Camada 0: Território Municipal Contínuo e Regime de Estância Turística
* **Base Legal:** Lei Orgânica Municipal nº 1.801/1990, Lei Estadual nº 6.899/1990, Lei Complementar Estadual nº 1.261/2015, Constituição do Estado de SP (Art. 146 e 180), LC nº 39/2006 (Plano Diretor) e LC nº 140/2025 (PDTur).
* **Órgão Responsável:** IBGE / Prefeitura da Estância Turística de São Roque.
* **Escala Nominal:** 1:50.000 / Padrão de Exatidão Cartográfica (PEC) Classe A.
* **Arquivo Original Fornecido:** `sao_roque_3550605_setores_CD2022.kmz` (360.835 bytes).
* **Arquivo GeoJSON Integrado:** `data/territorio_municipal_sao_roque_web.geojson` (261.222 bytes).
* **Estatística da Geometria:**
  * **Polígono Contínuo Unificado:** 188 setores censitários oficiais dissolvidos sem frestas ou sobreposições.
  * **Área Total Calculada:** **30.701,47 hectares** (307,01 km²).
  * **Perímetro Municipal:** **115,35 km**.
  * **Regime Especial:** Base territorial da governança de Estância Turística, repasses do DADETUR, deliberações do COMTUR e obrigatoriedade de revisão trienal do Plano Diretor de Turismo.

### Camada 1: Zoneamento Urbano e Rural Oficial (Plano Diretor Municipal 2006 - Homologado)
* **Base Legal:** Lei Complementar Municipal nº 40/2006 e Decretos Regulamentadores.
* **Órgão Responsável:** Prefeitura da Estância Turística de São Roque (Divisão de Planejamento e Gestão Territorial).
* **Escala Nominal:** 1:10.000 / Padrão de Exatidão Cartográfica (PEC) Classe A (Decreto Federal nº 89.817/1984).
* **Arquivo Original Fornecido:** `PMD2006 - Zoneamento.kmz` (220.404 bytes).
* **Arquivo Histórico Arquivado:** `dados_oficiais/municipal/PMD2006_Zoneamento.kmz`.
* **Hash SHA-256 (KMZ Original):** `627bd2b87b1138987fd1a1e0c210e6d01619b3a3e2fadc4044b4e100e19183ae`.
* **Arquivo GeoJSON Integrado:** `data/pmsr_zoneamento_pmd2006.geojson` (1.518.293 bytes).
* **Hash SHA-256 (GeoJSON Integrado):** `31f6ae7db0f36f521339ace91e881193b57e98d6833a62038933df8b040e3216`.
* **Estatística da Geometria:**
  * **31 Zonas Territoriais** categorizadas (Central, Densidade Alta, Média, Baixa, Consolidação Urbana, Industrial, Preservação, Rural, ZUCAer, ZUE Turístico/Vinho, ZUE Econômico/Raposo Tavares, ZUE Chácaras de SJN e ZUE Chácaras em Manancial).
  * **14.974 Vértices Geodésicos Reais** (zero caixas sintéticas ou simplificações artificiais).

### Camada 2: Minuta do Plano Diretor 2006 (Estudo Técnico Prévio / Minuta Técnica de Zoneamento)
* **Base Técnica:** Levantamento e Minuta Técnica Preliminar de Zoneamento para Elaboração do PMD 2006.
* **Órgão Responsável:** Prefeitura da Estância Turística de São Roque / Equipe Técnica de Planejamento Urbano.
* **Escala Nominal:** 1:10.000 / Padrão de Exatidão Cartográfica (PEC) Classe A (Decreto Federal nº 89.817/1984).
* **Arquivo Original Fornecido:** `minutaPMD2006 - Zoneamento.kmz` (211.619 bytes).
* **Arquivo Histórico Arquivado:** `dados_oficiais/municipal/minutaPMD2006_Zoneamento.kmz`.
* **Hash SHA-256 (KMZ Original):** `66908ef3a4df5ffa7a7177d5344cced9d4e787a39d4c93afc74c6af9f144b177`.
* **Arquivo GeoJSON Integrado:** `data/pmsr_zoneamento_minuta_pmd2006.geojson` (1.496.087 bytes).
* **Hash SHA-256 (GeoJSON Integrado):** `6dbd3aa8f9e1b62171587dcc51c91d9da4e00a0a71fb6c4328303004a4abbe55`.
* **Estatística da Geometria:**
  * **33 Zonas/Polígonos Territoriais** com cálculo oficial de área em hectares e m², perímetro e codificação GID municipal.
  * **14.638 Vértices Geodésicos Reais** com estilos e paleta cromática original preservada.
  * Presença de zonas temáticas prévias como ZUPA (Zona de Uso Predominantemente Agrícola/Ambiental), ZUE Ocupação Estratégica, ZUE Chácaras Manancial e ZUE Atividades Especiais da Raposo Tavares.

---

## 2. Esfera Estadual (São Paulo)

### A. Secretaria de Meio Ambiente, Infraestrutura e Logística (SEMIL) / SIGRH
* **Atribuição:** Delimitação da Área de Proteção e Recuperação aos Mananciais (APM) da Bacia Hidrográfica da Represa de Itupararanga.
* **Base Legal:** Lei Estadual nº 9.866/1997 e Lei Estadual nº 11.579/2003.
* **Escala Nominal:** 1:25.000 / PEC Classe A.

### B. Instituto Geográfico e Cartográfico (IGC / IDE-SP)
* **Atribuição:** Cartografia básica oficial do Estado de São Paulo, curvas de nível e sistema viário de alta precisão.
* **Escala Nominal:** 1:10.000 (Mapeamento Paulista).

---

## 3. Esfera Federal

### A. Instituto Brasileiro de Geografia e Estatística (IBGE)
* **Atribuição:** Malhas territoriais municipais e distritais oficiais, setores censitários e cadastro nacional de endereços (CNEFE 2022).
* **Base Legal:** Lei Federal nº 5.534/1968 e Resoluções da Presidência do IBGE.
* **Escala Nominal:** 1:50.000 / PEC Classe A.
* **Endpoint da API Oficial:** `https://servicodados.ibge.gov.br/api/v3/malhas/municipios/3550605?formato=application/vnd.geo+json&qualidade=maxima`

### B. Serviço Geológico do Brasil (SGB / CPRM)
* **Atribuição:** Cartografia e setorização oficial de áreas de risco geológico (R1 a R4: deslizamentos e inundações).
* **Base Legal:** Lei Federal nº 12.608/2012 (Política Nacional de Proteção e Defesa Civil - PNPDEC).
* **Escala Nominal:** 1:5.000 / PEC Classe A.
* **Repositório Institucional:** RIGEO / CPRM (Doc 24301 - Mapeamento de São Roque 2023).

### C. Comando da Aeronáutica (COMAER / DECEA) e Agência Nacional de Aviação Civil (ANAC)
* **Atribuição:** Servidões Aeronáuticas, Planos de Zona de Proteção de Aeródromos (PBZPA), Planos de Zoneamento de Ruído (PBZR) e Área de Segurança Aeroportuária (ASA - 20 km de raio).
* **Base Legal:** Lei Federal nº 7.565/1986 (CBA Arts. 43 a 47), Lei Federal nº 12.725/2012, Instrução do Comando da Aeronáutica ICA 11-408 e Regulamento Brasileiro da Aviação Civil RBAC nº 161.
* **Aeródromo de Referência:** São Paulo Catarina Aeroporto Executivo Internacional (SBJH), Pista 13/31 (2.470 m x 45 m), km 62 da Rodovia Castello Branco.
* **Arquivo GeoJSON Integrado:** `data/zona_protecao_aeroportuaria_catarina_web.geojson` (129.536 bytes).
* **Estatística da Geometria:**
  * Pista 13/31 com 2.470 m de extensão.
  * Cone de aproximação, decolagem e transição de 16 km de envergadura com restrição de gabarito (SLO) e zoneamento acústico.
  * Área de Segurança Aeroportuária (ASA de raio 20 km) cobrindo **21.648,44 hectares** (70,51% do território de São Roque) com proibição de lixões e controle de fauna e queimadas.
