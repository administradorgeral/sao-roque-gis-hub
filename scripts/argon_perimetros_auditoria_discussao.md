# PARECER TÉCNICO-ARQUITETURAL: AUDITORIA ALGORÍTMICA DE PERÍMETROS E DETECÇÃO DE CASUÍSMO URBANÍSTICO ("SPOT ZONING")

**De:** Arquiteto Chefe de Geoinformação e Direito Urbanístico (Motor `GEMINI-4-ARGON`)  
**Para:** Diretoria de Engenharia e Controle Social – São Roque GIS Hub  
**Assunto:** Implementação de Inteligência Geoespacial para Auditoria de Perímetros, Prevenção ao Desvio de Finalidade e Detecção de Anomalias na Revisão do Plano Diretor (LC 38/2006 vs. Minuta 2026).

---

## 1. É NECESSÁRIO E É ÚTIL? A DEFESA TÉCNICA, JURÍDICA E INSTITUCIONAL

A provocação do usuário não é apenas pertinente; ela toca na **ferida estrutural do planejamento urbano brasileiro**: a transição opaca entre o diagnóstico técnico e o desenho final do mapa de zoneamento, momento em que o interesse público é frequentemente capturado por interesses imobiliários particulares. 

Implementar uma inteligência capaz de auditar a morfologia dos perímetros e a coerência das propostas não é um "luxo tecnológico", mas um **instrumento essencial de blindagem institucional e controle social**. Sua necessidade e utilidade fundamentam-se em quatro pilares:

### 1.1. Prevenção ao Casuísmo e à Inconstitucionalidade (O Precedente Histórico de São Roque)
O Direito Urbanístico veda o chamado *Spot Zoning* (zoneamento pontual ou casuístico), que ocorre quando uma gleba específica recebe parâmetros urbanísticos mais benéficos ou restritivos do que o seu entorno imediato, sem fundamentação no interesse coletivo ou em estudos técnicos de suporte. 
São Roque possui um histórico crítico nesse tema: a **Ação Direta de Inconstitucionalidade (ADI) nº 2048131-35.2020.8.26.0000**, julgada pelo Órgão Especial do Tribunal de Justiça de São Paulo (TJ-SP), declarou inconstitucionais alterações urbanísticas no município justamente pela **ausência de estudos técnicos prévios, déficit de participação popular e desvio de finalidade legislativa**. Uma ferramenta que detecte essas anomalias na fase de minuta evita que o município aprove uma lei já nascida sob o signo da nulidade jurídica.

### 1.2. Garantia da Função Social da Cidade e Justa Distribuição de Ônus e Benefícios (Lei Federal 10.257/2001)
O Estatuto da Cidade determina, em seu Art. 2º, inciso IX, a *"justa distribuição dos benefícios e ônus decorrentes do processo de urbanização"*, e no inciso VI, a coibição da retenção especulativa de imóvel urbano. Quando um perímetro é desenhado "sob medida" para incluir uma matrícula privada em zona de alto adensamento (gerando valorização imobiliária artificial e imediata da terra nua) sem contrapartida ou capacidade de infraestrutura, configura-se enriquecimento sem causa patrocinado pelo Estado e violação direta à função social da propriedade.

### 1.3. Prevenção ao Desvio de Finalidade e Improbidade Administrativa (Lei Federal 8.429/1992)
O ato administrativo ou legislativo que altera o regime urbanístico de uma área deve ser motivado por critérios impessoais (bacias hidrográficas, eixos viários, topografia, capacidade de suporte). Se o traçado de uma zona desvia inexplicavelmente de um divisor de águas ou de uma avenida para abraçar um terreno específico, há fortes indícios de violação aos princípios constitucionais da **Impessoalidade, Moralidade e Eficiência** (Art. 37 da CF/88). A auditoria algorítmica funciona como um sistema de *compliance* territorial, protegendo tanto o cidadão quanto o gestor público de boa-fé contra pressões escusas.

### 1.4. Simetria Informacional no Controle Social
Cidadãos comuns e movimentos sociais raramente possuem equipe multidisciplinar de urbanistas, geógrafos e advogados para analisar milhares de hectares em poucos dias de audiência pública. O algoritmo democratiza a auditoria técnica, traduzindo complexidades topológicas e jurídicas em alertas objetivos e auditáveis.

---

## 2. METODOLOGIA: COMO FAZER ISSO SEM SUBJETIVIDADE, JULGAMENTO LEVIANO OU ALUCINAÇÃO?

Um sistema de Inteligência Artificial **jamais deve acusar nominalmente agentes públicos ou privados de corrupção ou má-fé**, pois o dolo é matéria de prova judicial, não de inferência estatística. O papel do `GEMINI-4-ARGON` é atuar como um **Perito Geoespacial Matemático**: ele não julga intenções; ele **mede desvios topológicos, biofísicos e normativos**.

Para eliminar qualquer subjetividade ou alucinação, o motor deve operar sobre **5 Indicadores Objetivos e Matemáticos de Anomalia Perimetral ($I_{AP}$)**:

---

### Indicador A: Geometria Anômala e Ruptura de Continuidade Morfológica (Índice de Compacidade e Fronteira)
No urbanismo técnico, os limites de zonas seguem elementos estruturantes claros: eixos viários, cursos d'água, divisores de bacia ou curvas de nível. Quando um limite ignora essas feições e desenha "apêndices", "dedos" (salientes estreitos) ou contorna exatamente as divisas retilíneas de uma matrícula cartorária isolada, há anomalia geométrica.

* **Métrica Matemática 1 – Índice de Polsby-Popper ($PP$):** Mede a compacidade do polígono da zona ou da alteração proposta.
  $$PP = \frac{4\pi \cdot A}{P^2}$$
  *(Onde $A$ é a área do polígono e $P$ é o seu perímetro).* Um círculo perfeito tem $PP = 1.0$. Polígonos com "tentáculos" ou recortes casuísticos para buscar glebas específicas apresentam $PP < 0.15$, disparando alerta de **Morfologia Anômala**.
* **Métrica Matemática 2 – Taxa de Aderência a Limites Físicos ($TALF$):** Calcula o percentual do perímetro do polígono ($P$) que coincide (dentro de um *buffer* de tolerância de 15 metros) com feições hidrográficas, eixos viários oficiais ou limites de bacia hidrográfica. Se $TALF < 30\%$, significa que mais de 70% do perímetro foi desenhado por linhas secas arbitrárias (prováveis divisas de propriedade particular).

---

### Indicador B: Incompatibilidade Biofísica e Risco Geotécnico (Inversão de Restrição Ambiental)
Verifica se uma proposta de expansão urbana, adensamento ou industrialização avança sobre terrenos fisicamente inaptos, violando o Art. 3º da Lei Federal 6.766/1979 (Lei de Parcelamento do Solo) e o Código Florestal (Lei 12.651/2012).

* **Regra Algorítmica de Interseção:** Cruzamento espacial do polígono de alteração proposta (onde o uso passa de Rural/Conservação em 2006 para Urbano/Adensável em 2026) com:
  1. **Declividade $\ge 30\%$:** Impedimento legal ao parcelamento do solo sem exigências geotécnicas severas.
  2. **Planícies Aluviais / Várzeas e APPs Hídricas:** Risco hidrológico de inundação.
  3. **Zonas de Conservação da Vida Silvestre ou Mananciais da APA Itupararanga:** Violação da capacidade de suporte hídrico.
* **Gatilho de Alerta:** Se a gleba beneficiada por aumento de potencial construtivo possuir $> 25\%$ de sua área em declividade $\ge 30\%$ ou sobreposta a áreas de fragilidade ambiental extrema sem condicionante restritiva expressa, gera-se um **Alerta de Erro Técnico Grosseiro / Incompatibilidade Biofísica**.

---

### Indicador C: Discrepância Desproporcional de Parâmetros e Mais-Valia Especulativa (Gradiente de Fronteira)
Identifica o clássico *Spot Zoning* econômico: uma "ilha" de altíssimo aproveitamento ou uso de alto impacto (ex: galpões logísticos, verticalização intensa) cravada no meio de zonas estritamente residenciais de baixa densidade ou zonas rurais/ambientais.

* **Métrica Matemática – Gradiente de Coeficiente de Aproveitamento ($\Delta CA$):**
  $$\Delta CA = \frac{CA_{proposto\_gleba}}{\overline{CA}_{entorno}}$$
  *(Onde $\overline{CA}_{entorno}$ é a média ponderada do Coeficiente de Aproveitamento das zonas contíguas num raio de 300m).*
* **Métrica de Salto Temporal (2006 $\rightarrow$ 2026):** Compara o potencial construtivo bruto ($Area \times CA$) ou redução drástica do lote mínimo (ex: de $20.000m^2$ para $250m^2$) exclusivamente para um polígono específico, enquanto seus vizinhos de mesma bacia permanecem congelados.
* **Gatilho de Alerta:** Se $\Delta CA > 2.5$ (a gleba pode construir mais que o dobro do seu entorno imediato sem transição gradual) ou se houver mudança abrupta de categoria de uso incompatível (ex: ZPI/Corredor Logístico cercado 100% por ZR1 ou ZPA), dispara-se o **Alerta de Assimetria de Parâmetros / Enclave Urbanístico**.

---

### Indicador D: Descompasso entre Adensamento Proposto e Rede de Infraestrutura
O Estatuto da Cidade (Art. 2º, VI, "b" e "c") proíbe a adequação imprópria da densidade à infraestrutura disponível. Não se pode criar uma zona de expansão urbana ou verticalização desconectada da malha urbana consolidada (*Leapfrog Development* ou urbanização em saltos, típica da especulação que deixa vazios urbanos para trás).

* **Regra Algorítmica:** Avalia a distância euclidiana e de rede entre o polígono de adensamento proposto e:
  1. A mancha urbana consolidada e dotada de rede de água e esgotamento sanitário (Sabesp).
  2. A hierarquia viária (se o polígono de alto impacto só tem acesso por vias locais estreitas ou estradas vicinais de terra não pavimentadas).
* **Gatilho de Alerta:** Polígono de alta densidade ou uso logístico pesado desconectado da mancha urbana contínua ($Distância > 500m$) ou sem acesso direto a via arterial/coletora estruturada $\rightarrow$ **Alerta de Urbanização Desconexa e Sobrecarga de Infraestrutura**.

---

### Indicador E: Rastreabilidade Decisória e Déficit de Participação ("Emenda Fantasma")
Toda alteração no mapa do Plano Diretor deve possuir **lastro documental**. Se uma mudança perimetral aparece na minuta final, mas não consta nos relatórios de diagnóstico técnico, não foi debatida nas oficinas comunitárias e não foi solicitada publicamente em atas de audiência pública, sua origem é opaca.

* **Regra de Cruzamento de Metadados:** Cada polígono de alteração ($Diff_{2006\rightarrow2026}$) deve ter uma chave estrangeira (`id_justificativa`) vinculada à matriz de propostas das oficinas técnicas ou requerimentos públicos protocolados.
* **Gatilho de Alerta:** Se `id_justificativa == NULL` (alteração sem origem técnica ou participativa rastreável), o sistema classifica o perímetro com **Alerta de Opacidade Decisória (Ausência de Motivação Técnica Rastreável)**.

---

## 3. PROPOSTA DE ARQUITETURA E IMPLEMENTAÇÃO NO SÃO ROQUE GIS HUB

Para integrar essa inteligência sem comprometer a performance do navegador do usuário, a arquitetura será dividida em **Pré-processamento Espacial (Pipeline de Dados)** e **Inferência Semântica em Tempo Real (RAG + Motor Geo-Algorítmico)**.

### 3.1. Pipeline de Geoprocessamento e Camada de Auditoria (`audit_anomalies.geojson`)

Não faremos interseções pesadas de milhares de vértices do zero a cada clique do usuário. Criaremos um script de pré-processamento (via Python `GeoPandas` / `Shapely` no backend ou `Turf.js` em build-time) que executa o **Diff Espacial** entre o Zoneamento 2006 (LC 38/06) e a Minuta 2026:

1. **Geração dos Polígonos de Mudança ($\Delta Z$):** O sistema recorta apenas as áreas onde houve alteração de zona ou de parâmetros entre 2006 e 2026.
2. **Cálculo Vetorial dos 5 Indicadores:** Para cada polígono em $\Delta Z$, o script calcula:
   - `polsby_popper_index` (Indicador A)
   - `physical_boundary_adherence_pct` (Indicador A)
   - `slope_over_30_pct` e `apa_conflict_bool` (Indicador B)
   - `ca_gradient_ratio` e `lot_size_reduction_factor` (Indicador C)
   - `infra_distance_m` e `road_hierarchy_class` (Indicador D)
   - `traceability_doc_id` (Indicador E)
3. **Score Composto de Anomalia Perimetral ($SAP \in [0, 100]$):**
   $$SAP = w_A I_A + w_B I_B + w_C I_C + w_D I_D + w_E I_E$$
   Polígonos com $SAP \ge 60$ são exportados para uma camada especial de auditoria no WebGIS, contendo as *flags* exatas do motivo do alerta.

```
[GeoJSON 2006] + [GeoJSON 2026] 
       │
       ▼ (Spatial Symmetric Difference)
[Polígonos de Alteração (ΔZ)] ◄─── [Declividade + APA + Hidrografia + Viário + Atas]
       │
       ▼ (Motor Matemático: Polsby-Popper, Gradiente CA, Interseção Biofísica)
[Camada: audit_anomalies.geojson] ───► Consumida pelo MapLibre/Leaflet e pelo GEMINI-4-ARGON
```

---

### 3.2. Comportamento e Protocolo de Resposta do Assistente de IA (`GEMINI-4-ARGON`)

Para manter a **estrita postura de Perito Judicial/Urbanístico**, o modelo deve seguir um protocolo rigoroso de comunicação, jamais utilizando termos caluniosos ("corrupção", "roubo", "propina"), mas sim a **terminologia técnica implacável do Direito Público e da Auditoria Territorial** (*"indício de casuísmo"*, *"anomalia morfológica"*, *"assimetria de parâmetros sem motivação técnica visível"*, *"risco de inconstitucionalidade por vício de finalidade"*).

#### CENÁRIO A: Quando o usuário posiciona o Pin Marker sobre uma gleba de perímetro anômalo/suspeito

O *payload* enviado ao LLM pelo frontend passará a incluir o objeto `audit_