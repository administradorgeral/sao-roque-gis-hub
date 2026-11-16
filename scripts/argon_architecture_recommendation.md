# Arquitetura de Refatoração do Motor de IA Territorial: São Roque GIS Hub

Como arquiteto de software e especialista em IA Geoespacial e Direito Urbanístico, apresento a arquitetura definitiva para substituir respostas estáticas e superficiais por um motor de **Raciocínio Geoespacial e Jurídico Exaustivo (Deep Territorial RAG)**.

---

## 1. Decomposição Ontológica de Perguntas Amplas e Conceituais

Quando um usuário pergunta *"O que é ruim?"*, *"Quais as fragilidades?"* ou *"O que é proibido?"*, um sistema de busca tradicional por palavras-chave falha porque a palavra *"ruim"* não existe no texto da lei.

Para resolver isso, implementaremos um **Classificador de Intenção e Expansor de Consulta (Query Expansion Ontology)** antes da busca no banco SQLite (`sao_roque_geodados.db`). Perguntas avaliativas ou conceituais negativas serão automaticamente mapeadas e decompostas em **5 Eixos Estruturais de Diagnóstico Territorial**:

```
                     [ Pergunta: "O que é ruim?" ]
                                   │
                    (Expansor Ontológico de Consulta)
                                   ▼
 ┌─────────────────┬───────────────┼───────────────┬─────────────────┐
 ▼                 ▼               ▼               ▼                 ▼
[Eixo 1: Físico] [Eixo 2: Redes] [Eixo 3: Uso]   [Eixo 4: Lei]     [Eixo 5: Social]
- Declividade>30% - Vias s/ saída - Conflito Ind. - Vedações Art.   - Audiências Púb.
- APP / Várzeas   - Tráfego Pesado- Déficit Esgoto- Multas / Embargo- Reclamações
- Risco Geológico - SRQ-01..SRQ-22- ZUI saturada  - Incompatibilidade- Déficit Equip.
```

### Matriz de Mapeamento Técnico:
1. **Eixo Físico-Ambiental (Vulnerabilidades e Riscos):**
   * *Fontes:* Carta 02 (Suscetibilidade/Risco Geológico), Camadas de Declividade (>30% e >45%), APPs Hídricas (buffers de 30m/50m), APAs (Itupararanga) e Reserva da Biosfera do Cinturão Verde.
   * *Critério:* Áreas impróprias ao parcelamento (Lei Federal 6.766/79, Art. 3º).
2. **Eixo de Infraestrutura, Mobilidade e Conectividade (Gargalos):**
   * *Fontes:* Carta 06 (Sistema Viário), Matriz de 22 Obras Prioritárias (`SRQ-01` a `SRQ-22`).
   * *Critério:* Conflito entre tráfego logístico/industrial e malha urbana histórica; estradas vicinais sem pavimentação ou drenagem; gargalos na Raposo Tavares (SP-270) e Lívio Tagliassachi.
3. **Eixo de Conflitos de Uso do Solo e Saneamento (Pressão Antrópica):**
   * *Fontes:* Cruzamento das 28 Zonas (Carta 04) com rede de esgotamento sanitário e captação hídrica.
   * *Critério:* Loteamentos clandestinos/irregulares (ZEIS de Regularização vs. Zonas Rurais), ocupação de cabeceiras de drenagem sem rede coletora, estagnação de vazios urbanos especulativos.
4. **Eixo Normativo-Jurídico (Vedações, Restrições e Penalidades):**
   * *Fontes:* 1.709 artigos jurídicos (Plano Diretor 2026, Lei de Uso e Ocupação do Solo, Código de Obras e Posturas).
   * *Critério:* Usos expressamente **Proibidos / Incompatíveis**, índices de aproveitamento zerados, taxas de permeabilidade mínimas rígidas (ex: 70% a 80% em zonas ambientais) e sanções administrativas.
5. **Eixo Socioterritorial (Vetor de Participação Popular):**
   * *Fontes:* Base vetorial das Audiências Públicas e contribuições comunitárias.
   * *Critério:* Dores reais apontadas pelos moradores (falta de equipamentos públicos, transporte coletivo deficitário nos bairros afastados como Canguera, São João Novo e Mailasqui, insegurança viária).

---

## 2. Arquitetura Híbrida de RAG Geoespacial (Deep Context Injection)

O segredo para que o modelo `gemini-4-argon` responda com profundidade acadêmica, jurídica e técnica está na **Injeção de Contexto Estruturado Híbrido** (Espacial + Normativo + Social).

### 2.1. Fluxo de Recuperação em Duas Camadas (Dual-Mode Context)
* **Modo A — Com Pin Selecionado (Análise Local + Macro):** O sistema extrai os dados exatos da coordenada `(lat, lng)` clicada no Leaflet (Zona exata, Bacia Hidrográfica, Declividade local, Artigos aplicáveis àquela zona) **E** adiciona o diagnóstico macro do município como pano de fundo.
* **Modo B — Sem Pin Selecionado (Diagnóstico Sistêmico Exaustivo):** O sistema executa queries agregadas nos 5 eixos sobre as 33 camadas, 13 Cartas, 28 Zonas, 22 Obras (`SRQ-01` a `SRQ-22`) e o top-K de artigos restritivos dos 1.709 dispositivos legais.

### 2.2. O Prompt de Sistema Definitivo (`SYSTEM_INSTRUCTION`)

```markdown
Você é o Motor Central de Inteligência Geoespacial e Direito Urbanístico do sistema 'São Roque GIS Hub' (Modelo: gemini-4-argon).
Sua base de conhecimento abrange o Plano Diretor Participativo da Estância Turística de São Roque (2026), 1.709 artigos de legislação urbanística/ambiental, 13 Cartas Oficiais, 33 camadas geográficas, 28 Zonas de Uso e Ocupação do Solo, o plano de 22 Obras Prioritárias (SRQ-01 a SRQ-22) e os vetores de Participação Popular das Audiências Públicas.

DIRETRIZES INEGOCIÁVEIS DE RESPOSTA:
1. PROIBIÇÃO DE RESPOSTAS RASAS: Nunca responda com listas curtas ou genéricas. Toda resposta deve ser exaustiva, rigorosamente técnica, multidisciplinar e fundamentada nos dados fornecidos no contexto.
2. INTERPRETAÇÃO DE PERGUNTAS AMPLAS: Se o usuário perguntar "o que é ruim?", "quais os problemas?", "o que é proibido?" ou similares, você DEVE estruturar a resposta obrigatoriamente nos 5 Eixos de Diagnóstico Territorial:
   - I. Riscos Físico-Ambientais e Restrições Geotécnicas (Cartas e Camadas Ambientais)
   - II. Gargalos de Mobilidade, Logística e Infraestrutura (Obras SRQ-01 a SRQ-22 e Carta Viária)
   - III. Conflitos Fundiários, Uso do Solo e Saneamento (Análise das 28 Zonas e ZEIS)
   - IV. Vedações Normativas, Restrições Legais e Sanções (Citação exata de Artigos, Parágrafos e Índices Urbanísticos: TO, CA, TP, Lote Mínimo, Gabarito)
   - V. Demandas Críticas da Participação Popular (Voz das Audiências Públicas por região/bairro)
3. RIGOR TÉCNICO E CITAÇÃO: Cite sempre o código da Carta (ex: Carta 04 - Macrozoneamento), a sigla da Zona (ex: ZPA, ZEU, ZUI, ZR), o código da obra (ex: SRQ-07) e os números dos Artigos de Lei fornecidos no contexto.
4. INTERATIVIDADE CARTOGRÁFICA (ACTION TAGS): Ao mencionar camadas, cartas, zonas ou coordenadas específicas, insira tags de ação padronizadas para que o front-end Leaflet gere botões interativos:
   - Para ativar camada/carta: [[ACTION:LAYER:id_da_camada|Nome da Camada]]
   - Para focar em coordenada/obra: [[ACTION:FLYTO:lat,lng,zoom|Ver no Mapa: Nome do Local]]
   - Para abrir artigo de lei: [[ACTION:LAW:id_artigo|Ler Art. X]]
5. FORMATAÇÃO RICA: Utilize tabelas Markdown para comparar parâmetros de zonas ou obras, listas hierárquicas e blocos de destaque técnico.
```

---

## 3. Implementação Completa: Refatoração de `ai-search.js`

Abaixo está o código completo em JavaScript (ES6+) pronto para produção no seu WebGIS. Ele inclui:
1. **Expansor Semântico e Ontológico** para perguntas abertas.
2. **Coletor de Contexto SQLite/Memória** (agregando as 33 camadas, 13 cartas, 28 zonas, obras `SRQ-01`..`SRQ-22`, artigos e participação popular).
3. **Integração Direta com a API Gemini (`gemini-4-argon`)** com suporte a `streamGenerateContent` (ou resposta completa) e **Fallback Local Exaustivo** caso a chave de API não esteja configurada ou o sistema esteja offline.
4. **Renderizador de UI Avançado** que converte Markdown, tabelas e as tags `[[ACTION:...]]` em botões reais que controlam o mapa Leaflet (`map.flyTo`, ativação de GeoJSON/TileLayers).

```javascript
/**
 * SÃO ROQUE GIS HUB - Motor de Inteligência Geoespacial e Jurídica (v4.0)
 * Módulo: ai-search.js
 * Arquitetura: Deep Territorial RAG + Gemini-4-Argon + Leaflet Action Bridge
 */

export class TerritorialAIEngine {
    constructor({ map, dbEngine, layerManager, apiKey = null }) {
        this.map = map;                   // Instância do Leaflet Map
        this.db = dbEngine;               // Instância do SQL.js (sao_roque_geodados.db) ou Store em memória
        this.layerManager = layerManager; // Gerenciador das 33 camadas e 13 cartas
        this.apiKey = apiKey || localStorage.getItem('SRQ_GEMINI_API_KEY') || '';
        this.modelName = 'gemini-4-argon';
        this.activePin = null;            // { lat, lng, properties, zone, articles }

        // Dicionário Ontológico para Expansão de Consultas Amplas/Avaliativas
        this.ontologyMap = {
            negativo_amplo: {
                triggers: [
                    'ruim', 'ruins', 'problema', 'problemas', 'fragilidade', 'fragilidades',
                    'critico', 'crítico', 'defeito', 'negativo', 'pior', 'conflito', 'conflitos',
                    'gargalo', 'gargalos', 'risco', 'riscos', 'proibido', 'proibidos', 'vedado',
                    'ilegal', 'irregular', 'ameaca', 'ameaça', 'vulnerabilidade', 'precario', 'precário'
                ],
                expandedTerms: [
                    // Eixo 1: Físico-Ambiental
                    'declividade', 'alagamento', 'inundação', 'escorregamento', 'erosão', 'APP', 'APA', 'Itupararanga', 'restrição ambiental', 'suscetibilidade',
                    // Eixo 2: Mobilidade e Infraestrutura
                    'congestionamento', 'tráfego pesado', 'via sem saída', 'drenagem', 'pavimentação', 'SRQ-', 'transporte', 'logística',
                    // Eixo 3: Uso do Solo e Saneamento
                    'esgoto', 'saneamento', 'clandestino', 'irregular', 'ZEIS', 'incompatível', 'poluição', 'vazio urbano', 'adensamento',
                    // Eixo 4: Normativo e Vedações
                    'vedado', 'proibido', 'multa', 'embargo', 'infração', 'não permitido', 'inadequado', 'índice', 'taxa de permeabilidade',
                    // Eixo 5: Social / Audiências
                    'reclamação', 'audiência pública', 'demanda', 'falta de', 'carência', 'equipamento público', 'saúde', 'educação'
                ]
            }
        };
    }

    /**
     * Define ou limpa o Pin ativo selecionado pelo usuário no mapa Leaflet
     */
    setActivePin(pinData) {
        this.activePin = pinData;
    }

    /**
     * 1. ANALISADOR DE INTENÇÃO E EXPANSOR ONTOLÓGICO
     * Detecta se a pergunta é conceitual/ampla e aciona a varredura nos 5 Eixos.
     */
    analyzeQueryIntent(userQuery) {
        const normalized = userQuery.to