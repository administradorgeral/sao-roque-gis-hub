# Diretrizes de Inteligência Territorial e Normativa · São Roque GIS Hub
**Código IBGE:** 3550605 | **Datum Oficial:** SIRGAS 2000 (EPSG: 31983 - UTM Fuso 23S)
**Repositório Base:** `dados_oficiais/sao_roque_geodados.db`

---

## 📌 Lembrete Permanente para IAs e Desenvolvedores

> [!IMPORTANT]
> **1. Princípio Fundamental de Ordenamento do Território:**
> No Plano Diretor e no WebGIS de São Roque, **nenhuma lei e nenhum mapa operam de forma isolada**. 
> Todo e qualquer ponto do território municipal é regido pela convergência de múltiplos diplomas legais (Zoneamento, Código de Obras, Código Florestal, Lei de Mananciais, Defesa Civil, Parcelamento do Solo e Código Tributário).
> 
> **2. Pirâmide das Leis (Hierarquia de Kelsen e Prevalência Automática):**
> O ordenamento jurídico segue hierarquia estrita:
> * 🔺 **Nível 1 · Federal (Teto Normativo e Normas Gerais):** CF/88, Código Florestal (Lei 12.651), Lei do Parcelamento do Solo (Lei 6.766), Estatuto da Cidade (Lei 10.257), Adaptação Climática (Lei 14.904/24), Qualidade do Ar (Lei 14.850/24), Mercado de Carbono (Lei 15.042/24).
> * 🔺 **Nível 2 · Estadual (Condicionantes Regionais e Bacias):** Lei de Proteção aos Mananciais (Lei Estadual 9.866/97 - Bacia de Itupararanga), GRAPROHAB, CETESB.
> * 🔺 **Nível 3 · Municipal (Interesse Local e Execução):** Plano Diretor (LC 39/2006), Lei de Zoneamento (LC 40/2006), Código de Obras (LC 41/2006).
> 
> **Regra de Ouro:** A norma municipal **suplementa** o interesse local, mas **jamais pode ser mais permissiva** ou afrouxar restrições federais ou estaduais protetivas (*in dubio pro natura*). Se houver conflito, a lei municipal que colidir com a norma federal ou estadual é nula por inconstitucionalidade (como no caso real da LC 125/2022 de São Roque, derrubada pelo TJSP na ADIN 2048131).
> 
> **Regra Obrigatória:** Sempre que novos mapas (camadas vetoriais ou matriciais) ou novas leis forem adicionados ao sistema, é **terminantemente obrigatório** registrar os metadados de amarração bidirecional conforme os protocolos abaixo.

---

## 1. Protocolo para Inclusão de Novos Mapas / Camadas

Ao ingerir uma nova camada cartográfica (ex.: Mapa de Declividade, Hidrografia, Áreas de Risco CPRM/IPT, APM Itupararanga, Curvas de Nível):

1. **Vincular Leis de Competência:**
   * Toda camada deve declarar quais diplomas legais e artigos regulamentam as suas feições.
   * *Exemplo (Declividade):* Deve amarrar à `LC 40/2006` (Art. 13 - Veda loteamento > 30%), `Lei Federal 6.766/1979` e `GRAPROHAB`.
   * *Exemplo (MDT/Altimetria):* Deve amarrar à `Lei Federal 12.651/2012` (APP Topo de Morro para cotas > 970m na Serra de São Roque).
2. **Definir Grau de Restrição:**
   * Classificar a incidência de cada dispositivo:
     * **Impeditiva:** Veda expressamente parcelamento ou edificação.
     * **Condicionante:** Exige estudo geotécnico, contenção, outorga ou parâmetros específicos.
     * **Diretiva:** Estabelece orientação de planejamento e greide viário.
3. **Formato Geodésico:**
   * Datum obrigatório: SIRGAS 2000 / Projeção UTM Fuso 23 Sul (EPSG: 31983) ou WGS84 (EPSG: 4326) com precisão métrica (zero caixas sintéticas).

---

## 2. Protocolo para Inclusão de Novas Leis / Normas Jurídicas

Ao cadastrar uma nova lei (Municipal, Estadual ou Federal):

1. **Preenchimento do Âmbito Territorial (`ambito_territorial`):**
   * A lei deve explicitar com clareza **qual recorte do mapa ela rege**:
     * `🏙️ Zona Urbana e ZUEs` (ex.: LC 40/2006)
     * `🏗️ Código de Obras` (ex.: LC 41/2006)
     * `🍇 Rota do Vinho (ZUE-DT)` (ex.: LC 40/2006 Art. 71 e LC 66/2012)
     * `🛣️ Eixo Rodovia Castello Branco (ZUE-OE)` (ex.: LC 48/2008 e LC 65/2012)
     * `🛣️ Eixo Rodovia Raposo Tavares (ZUCAer / ZUE-DE)` (ex.: LC 57/2009)
     * `💧 Bacia de Proteção a Mananciais (APM Itupararanga)` (ex.: Lei Estadual 9.866/1997)
     * `🌳 Áreas de Preservação Permanente (APPs de Rios e Morros)` (ex.: Lei Federal 12.651/2012)
     * `🛡️ Áreas Suscetíveis a Risco Geológico e Adaptação Climática` (ex.: Lei Federal 12.608/2012 e Lei Federal 14.904/2024)
     * `🌍 Políticas Climáticas, Mercado de Carbono e Qualidade do Ar` (ex.: Lei Federal 12.187/2009 - PNMC, Lei Federal 15.042/2024 - SBCE, Lei Federal 14.850/2024 - Ar, Lei Federal 14.902/2024 - Mover)
     * `🚜 Zona Rural Municipal` (ex.: Estatuto da Terra / INCRA - FMP 20.000 m²)
     * `🌐 Todo o Território Municipal` (ex.: Plano Diretor LC 39/2006, IPTU Lei 2.669/2002)
2. **Identificação das Zonas Afetadas (`zonas_afetadas`):**
   * Listar as siglas e nomenclaturas das zonas do zoneamento territorial que a norma incide diretamente.
3. **Link Oficial e Texto Integral:**
   * Manter o link pericial oficial da Câmara Municipal de São Roque, ALESP ou Planalto.
   * Salvar a íntegra compilada em Markdown em `dados_oficiais/legislacao/`.
4. **Reexecução do Compilador:**
   * Executar `python scripts/compilar_rol_legislacao.py` para atualizar o catálogo estático `data/rol_legislacao_territorial.json`.

---

## 3. Comportamento no Clique em Qualquer Ponto do Território

Ao clicar em qualquer ponto do mapa (`map.on('click')` ou via marcador interativo `📍`):
1. O sistema identifica o contorno/polígono da zona sob o cursor (`ZUC`, `ZUR-ad`, `ZUR-md`, `ZUR-bd`, `ZCU`, `ZUE-DT`, `ZUE-CM`, `ZUI`, `ZUPA`, `ZR`, etc.).
2. O modal de inspeção de atributos (`AttributeModal`) deve exibir obrigatoriamente:
   * **Identificação:** Zona, Sigla, Denominação, Área e Perímetro.
   * **Parâmetros Urbanísticos Oficiais:** Taxa de Ocupação Máxima, Coeficiente de Aproveitamento, Gabarito Máximo de Altura, Lote Mínimo e Recuos.
   * **Rol de Leis Aplicáveis a este Ponto:** Tabela com cada norma incidente, artigo específico, âmbito territorial e link oficial da Câmara/Prefeitura.
