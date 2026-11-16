# São Roque GIS Hub · Central de Inteligência Territorial

WebGIS moderno com **arquitetura 100% full-screen imersiva**, componentizada e desacoplada para visualização e consulta de dados geográficos oficiais do município de **São Roque (SP) — Código IBGE: 3550605**.

## 📌 Especificações Técnicas e Cartográficas
* **Datum Oficial:** SIRGAS 2000 (Sistema de Referência Geocêntrico para as Américas)
* **Projeção Cartográfica:** Universal Transversa de Mercator (UTM) Fuso 23 Sul (EPSG: 31983)
* **Motor Cartográfico:** Leaflet 1.9.4 + Proj4js 2.9.0
* **Padrão de Interface:** Canvas Full-Screen Imersivo + Card Flutuante de Camadas (`FloatingPanel`)
* **Barra de Pesquisa com IA Territorial:** Busca em linguagem natural (`/` ou `Ctrl+K`) com motor RAG semântico (221 normas, 1.709 artigos, 33 camadas e parâmetros urbanísticos) com gatilhos espaciais no mapa
* **Botão de Fontes:** Discreto no rodapé do card de camadas para máxima transparência institucional sem poluir a visão
* **Seleção no Mapa:** Marcador interativo de ponto (`📍`) com arrasto em tempo real e conversão métrica instantânea
* **Conformidade Legal:** Decreto Federal 89.817/1984 (Padrão de Exatidão Cartográfica) e ABNT NBR 13.133
* **Arquitetura:** Componentes ES6 desacoplados e reativos (`LayerManager`, `FloatingPanel`, `AttributeModal`, `AISearchEngine`)
* **Hospedagem:** interface estática no GitHub Pages; consultas Gemini protegidas por um Cloudflare Worker

---

## 🏛️ Camadas Oficiais Integradas

### 1. Esfera Municipal

#### A. Zoneamento Oficial Homologado (PMD 2006)
* **Instrumento Legal:** Lei Complementar Municipal nº 40/2006
* **Formato:** GeoJSON vetorizado de precisão ([`data/pmsr_zoneamento_pmd2006.geojson`](file:///C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/data/pmsr_zoneamento_pmd2006.geojson), 1.52 MB)
* **Origem:** KML/KMZ homologado pela Prefeitura da Estância Turística de São Roque
* **Composição:** 31 zonas territoriais (Central, Densidade Alta, Média, Baixa, ZUCAer, ZUE Turístico/Vinho, Raposo Tavares, Industrial, Preservação, Rural)
* **Densidade Geométrica:** 14.974 vértices geodésicos reais
* **Hash SHA-256 do GeoJSON:** `31f6ae7db0f36f521339ace91e881193b57e98d6833a62038933df8b040e3216`

#### B. Minuta Prévia do Zoneamento (Estudo Técnico PMD 2006)
* **Base Técnica:** Estudo Preliminar e Minuta Técnica Preparatória da PMSR
* **Formato:** GeoJSON vetorizado de precisão ([`data/pmsr_zoneamento_minuta_pmd2006.geojson`](file:///C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/data/pmsr_zoneamento_minuta_pmd2006.geojson), 1.50 MB)
* **Origem:** `minutaPMD2006 - Zoneamento.kmz` fornecido pela PMSR
* **Composição:** 33 zonas/polígonos com cálculo oficial de áreas (ha/m²), perímetros e códigos cadastrais GID
* **Densidade Geométrica:** 14.638 vértices geodésicos reais
* **Hash SHA-256 do GeoJSON:** `6dbd3aa8f9e1b62171587dcc51c91d9da4e00a0a71fb6c4328303004a4abbe55`

---

## ⚙️ Configuração da API do Google Gemini

O São Roque GIS Hub usa o **gemini-4-argon** para respostas de IA territorial.

### Configuração rápida:

1. **Crie o arquivo .env:**
   ```bash
   cp .env.example .env
   ```

2. **Obtenha sua API key:**
   - Acesse: https://aistudio.google.com/apikey
   - Copie a key gerada

3. **Configure no .env:**
   ```
   GEMINI_API_KEY=sua_api_key_aqui
   ```

4. **No browser (GitHub Pages ou local):**
   - Abra o console do navegador (F12)
   - Execute:
     ```javascript
     localStorage.setItem('SR_GEMINI_API_KEY', 'sua_api_key_aqui')
     ```
   - Recarregue a página

### Para desenvolvimento local:

Use o script de carregamento:
```bash
node scripts/load-env.js
```

Ou no HTML, inclua antes do `app.js`:
```html
<script type="module" src="scripts/load-env.js"></script>
```

---

## 📂 Estrutura de Diretórios
```
sao-roque-gis-hub/
├── index.html                   # Interface WebGIS full-screen imersiva
├── css/
│   └── style.css                # Estilos modernos, glassmorphism e responsividade
├── js/
│   ├── app.js                   # Orquestrador central da aplicação
│   ├── config.js                # Projeções, basemaps e metadados de camadas
│   ├── modules/
│   │   ├── layer-manager.js     # Gerenciador desacoplado de camadas e opacidade
│   │   ├── floating-panel.js    # Card flutuante desacoplado (Abas: Mapas | Legislação)
│   │   ├── attribute-modal.js   # Modal pericial e seguro contra XSS
│   │   └── legislation-catalog.js # Rol de leis e inteligência territorial
│   └── layers/                  # Módulos independentes por camada geográfica
├── dados_oficiais/              # Repositório de rastreabilidade e proveniência legal
│   ├── sao_roque_geodados.db    # Banco SQLite oficial (187 normas, 1.688 artigos, 30 zonas)
│   ├── DIRETRIZES_INTELIGENCIA_TERRITORIAL.md # Protocolo de amarração espacial-normativa
│   ├── FONTES_OFICIAIS.md       # Dossiê descritivo das fontes municipais, estaduais e federais
│   ├── REGISTRO_FONTES.json     # Catálogo estruturado em JSON com hashes e leis
│   ├── legislacao/              # 57 arquivos Markdown com íntegra compilada de leis
│   └── municipal/               # Arquivos vetoriais originais arquivados (KMZ / KML)
├── data/                        # Camadas oficiais em GeoJSON e catálogo de leis
│   ├── pmsr_zoneamento_pmd2006.geojson
│   ├── pmsr_zoneamento_minuta_pmd2006.geojson
│   └── rol_legislacao_territorial.json # Rol de leis e parâmetros urbanísticos
└── scripts/                     # Scripts de processamento e auditoria de dados
    ├── compilar_rol_legislacao.py
    ├── analisar_kmz_pmd2006.py
    └── converter_pmd2006_kml_to_geojson.py
```

---

## 🚀 Como Executar Localmente
```bash
python -m http.server 8000
```
Acesse no seu navegador: [http://localhost:8000](http://localhost:8000)

Para testar o Gemini localmente, defina `GEMINI_API_KEY` apenas no ambiente do
terminal e execute `python scripts/dev_server.py`. O servidor atende somente em
`127.0.0.1`; não coloque a chave no código nem a envie pelo navegador.

## 🌐 Publicação no GitHub Pages

O workflow `Deploy to GitHub Pages` publica o site automaticamente quando há
push na branch `main`. Para ativar a publicação pela primeira vez:

1. No GitHub, abra **Settings → Pages**.
2. Em **Build and deployment → Source**, selecione **GitHub Actions**.
3. Envie as alterações para `main` ou execute manualmente o workflow em
   **Actions → Deploy to GitHub Pages → Run workflow**.

Após a primeira publicação, o site ficará disponível em
`https://administradorgeral.github.io/sao-roque-gis-hub/`. O workflow envia
apenas os arquivos necessários ao site e omite o GeoJSON bruto de declividade,
que não é utilizado pela aplicação web.

### Consultas Gemini no site público

O GitHub Pages é estático e não pode guardar uma chave Gemini com segurança.
As consultas usam um Cloudflare Worker como proxy; a chave fica apenas como
segredo do Worker. Se o Worker ou sua configuração não estiver disponível, a
interface informa o erro e **não** substitui a resposta por uma resposta local.

1. Revogue credenciais que tenham sido compartilhadas em chats ou commits.
2. Em **GitHub → Settings → Secrets and variables → Actions**, crie os secrets
   `CLOUDFLARE_API_TOKEN` (permissão de editar Workers) e
   `CLOUDFLARE_ACCOUNT_ID`.
3. Envie os arquivos do Worker para `main`; o workflow **Deploy Gemini Worker**
   publicará `sao-roque-gis-gemini`.
4. No painel Cloudflare, abra o Worker e adicione `GEMINI_API_KEY` como **secret**
   em **Settings → Variables and Secrets**. Nunca use uma variável pública nem
   adicione a chave ao repositório.
5. Copie a URL `workers.dev` exibida pela Cloudflare. Em **GitHub → Settings →
   Secrets and variables → Actions → Variables**, crie `GEMINI_WORKER_URL` com
   essa URL (por exemplo, `https://sao-roque-gis-gemini.<subdominio>.workers.dev`).
6. Execute novamente o workflow **Deploy to GitHub Pages**. Sem essa variável,
   o site mostrará que o Gemini não está configurado, em vez de usar fallback.

O Worker restringe chamadas à origem do GitHub Pages e limita cada endereço IP
a 10 consultas por minuto. Esse limite é aproximado; configure também um limite
de gastos no Cloudflare e monitore o uso da API Gemini.
