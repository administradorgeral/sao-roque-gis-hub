with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

target = """              <div id="legend-territorio-municipal" class="zone-legend-grid" aria-hidden="true">
                <span class="zone-chip" title="Território integral do Município da Estância Turística de São Roque (30.701,47 ha)"><span class="zone-dot" style="background: #D4AF37; border: 1px solid #1E293B;"></span> Estância Turística (30.701 ha)</span>
                <span class="zone-chip" title="Linha divisória e perimétrica de São Roque (115,35 km)"><span class="zone-dot" style="background: #1E293B;"></span> Perímetro Municipal (115,35 km)</span>
              </div>
            </div>
          </div>"""

distritos_cards = """              <div id="legend-territorio-municipal" class="zone-legend-grid" aria-hidden="true">
                <span class="zone-chip" title="Território integral do Município da Estância Turística de São Roque (30.701,47 ha)"><span class="zone-dot" style="background: #D4AF37; border: 1px solid #1E293B;"></span> Estância Turística (30.701 ha)</span>
                <span class="zone-chip" title="Linha divisória e perimétrica de São Roque (115,35 km)"><span class="zone-dot" style="background: #1E293B;"></span> Perímetro Municipal (115,35 km)</span>
              </div>
            </div>
          </div>

          <!-- Camada: Distritos Municipais (IBGE 2022 / Lei Orgânica nº 1.801/90) -->
          <div class="layer-card" style="margin-bottom: 10px;">
            <div class="layer-card-top">
              <div class="layer-info">
                <div class="layer-bullet" style="background: #2563EB;"></div>
                <div class="layer-texts">
                  <span class="layer-name">Distritos Municipais (IBGE 2022)</span>
                  <span class="layer-tag">4 Distritos Oficiais · 30.701 ha · Divisão Administrativa</span>
                  <div style="display: flex; gap: 4px; flex-wrap: wrap; margin-top: 4px;">
                    <span class="badge-audit badge-blue" title="Divisão Territorial e Distrital">🏛️ Lei Orgânica nº 1.801/90</span>
                    <span class="badge-audit badge-purple" title="Base Cartográfica Contínua do Censo Demográfico">📊 IBGE Censo 2022</span>
                    <span class="badge-audit badge-green" title="Descentralização e Gestão de Serviços Públicos">📍 4 Distritos</span>
                  </div>
                </div>
              </div>
              <label class="switch" title="Alternar visualização dos distritos municipais">
                <input type="checkbox" id="toggle-distritos" aria-label="Ativar ou desativar camada de distritos municipais">
                <span class="slider"></span>
              </label>
            </div>

            <div class="layer-controls">
              <div class="opacity-box full-width">
                <span class="opacity-label">Opacidade</span>
                <input type="range" id="opacity-distritos" class="opacity-range" min="0.1" max="1" step="0.05" value="0.70" aria-label="Ajustar opacidade da camada de distritos">
              </div>
            </div>

            <!-- Legenda Rápida dos Distritos (Acordeão) -->
            <div class="legend-accordion">
              <button class="legend-toggle" type="button" aria-expanded="false" aria-controls="legend-distritos">
                <span class="legend-toggle-text">📊 Ver Distritos</span>
                <span class="legend-icon">▼</span>
              </button>
              <div id="legend-distritos" class="zone-legend-grid" aria-hidden="true">
                <span class="zone-chip" title="Distrito Sede de São Roque (12.336,51 ha / 40,18% · 92 setores)"><span class="zone-dot" style="background: #2563EB;"></span> São Roque - Sede (12.336 ha)</span>
                <span class="zone-chip" title="Distrito de Canguera (8.639,17 ha / 28,14% · 43 setores)"><span class="zone-dot" style="background: #059669;"></span> Canguera (8.639 ha)</span>
                <span class="zone-chip" title="Distrito de São João Novo (6.409,34 ha / 20,88% · 26 setores)"><span class="zone-dot" style="background: #7C3AED;"></span> São João Novo (6.409 ha)</span>
                <span class="zone-chip" title="Distrito de Mailasqui (3.316,45 ha / 10,80% · 27 setores)"><span class="zone-dot" style="background: #D97706;"></span> Mailasqui (3.316 ha)</span>
              </div>
            </div>
          </div>

          <!-- Camada: Setores Censitários (IBGE Censo 2022) -->
          <div class="layer-card" style="margin-bottom: 10px;">
            <div class="layer-card-top">
              <div class="layer-info">
                <div class="layer-bullet" style="background: #64748B;"></div>
                <div class="layer-texts">
                  <span class="layer-name">Setores Censitários (IBGE Censo 2022)</span>
                  <span class="layer-tag">188 Setores (134 Urbanos / 54 Rurais) · Malha Demográfica</span>
                  <div style="display: flex; gap: 4px; flex-wrap: wrap; margin-top: 4px;">
                    <span class="badge-audit badge-blue" title="Sigilo Estatístico e Censo Demográfico Nacional">⚖️ Lei Federal 5.534/68</span>
                    <span class="badge-audit badge-purple" title="Microdados Censitários Oficiais">📈 Censo IBGE 2022</span>
                    <span class="badge-audit badge-green" title="Distribuição de Moradores e Domicílios">👥 188 Setores</span>
                  </div>
                </div>
              </div>
              <label class="switch" title="Alternar visualização dos setores censitários">
                <input type="checkbox" id="toggle-setores-censitarios" aria-label="Ativar ou desativar camada de setores censitários">
                <span class="slider"></span>
              </label>
            </div>

            <div class="layer-controls">
              <div class="opacity-box full-width">
                <span class="opacity-label">Opacidade</span>
                <input type="range" id="opacity-setores-censitarios" class="opacity-range" min="0.1" max="1" step="0.05" value="0.65" aria-label="Ajustar opacidade da camada de setores censitários">
              </div>
            </div>

            <!-- Legenda Rápida dos Setores Censitários (Acordeão) -->
            <div class="legend-accordion">
              <button class="legend-toggle" type="button" aria-expanded="false" aria-controls="legend-setores-censitarios">
                <span class="legend-toggle-text">📊 Ver Situação Censitária</span>
                <span class="legend-icon">▼</span>
              </button>
              <div id="legend-setores-censitarios" class="zone-legend-grid" aria-hidden="true">
                <span class="zone-chip" title="Setores Censitários de Situação Urbana (134 setores)"><span class="zone-dot" style="background: #3B82F6;"></span> Urbana (134 setores)</span>
                <span class="zone-chip" title="Setores Censitários de Situação Rural (54 setores)"><span class="zone-dot" style="background: #10B981;"></span> Rural (54 setores)</span>
              </div>
            </div>
          </div>

          <!-- Camada: Sistema Viário e Logradouros (3.241 Ruas) -->
          <div class="layer-card" style="margin-bottom: 10px;">
            <div class="layer-card-top">
              <div class="layer-info">
                <div class="layer-bullet" style="background: #475569;"></div>
                <div class="layer-texts">
                  <span class="layer-name">Sistema Viário e Logradouros (3.241 Ruas)</span>
                  <span class="layer-tag">4.868 Vias · Rodovias, Estradas do Vinho & Ruas Locais</span>
                  <div style="display: flex; gap: 4px; flex-wrap: wrap; margin-top: 4px;">
                    <span class="badge-audit badge-red" title="Código de Trânsito Brasileiro">🚗 CTB (Lei 9.503/97)</span>
                    <span class="badge-audit badge-orange" title="Hierarquia Viária, Recuos e Larguras Mínimas">📐 LC nº 40/2006</span>
                    <span class="badge-audit badge-blue" title="OpenStreetMap / DER-SP / CCR ViaOeste">🗺️ Malha Viária 2026</span>
                  </div>
                </div>
              </div>
              <label class="switch" title="Alternar visualização do sistema viário e logradouros">
                <input type="checkbox" id="toggle-logradouros" aria-label="Ativar ou desativar camada de logradouros">
                <span class="slider"></span>
              </label>
            </div>

            <div class="layer-controls">
              <div class="opacity-box full-width">
                <span class="opacity-label">Opacidade</span>
                <input type="range" id="opacity-logradouros" class="opacity-range" min="0.1" max="1" step="0.05" value="0.85" aria-label="Ajustar opacidade do sistema viário">
              </div>
            </div>

            <!-- Legenda Rápida do Sistema Viário (Acordeão) -->
            <div class="legend-accordion">
              <button class="legend-toggle" type="button" aria-expanded="false" aria-controls="legend-logradouros">
                <span class="legend-toggle-text">📊 Ver Hierarquia Viária</span>
                <span class="legend-icon">▼</span>
              </button>
              <div id="legend-logradouros" class="zone-legend-grid" aria-hidden="true">
                <span class="zone-chip" title="Rodovias Principais (SP-280 Castello Branco, SP-270 Raposo Tavares, SP-053 Quintino de Lima)"><span class="zone-dot" style="background: #DC2626;"></span> Rodovias Principais</span>
                <span class="zone-chip" title="Avenidas Coletoras, Estradas Turísticas e Roteiro do Vinho"><span class="zone-dot" style="background: #D97706;"></span> Avenidas & Roteiro do Vinho</span>
                <span class="zone-chip" title="Ruas Locais, Residenciais e Vias Secundárias"><span class="zone-dot" style="background: #64748B;"></span> Ruas Locais & Residenciais</span>
              </div>
            </div>
          </div>"""

# Normalize line endings
normalized_content = content.replace("\r\n", "\n")
normalized_target = target.replace("\r\n", "\n")

if normalized_target in normalized_content:
    new_content = normalized_content.replace(normalized_target, distritos_cards.replace("\r\n", "\n"))
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(new_content)
    print("SUCCESS: index.html updated successfully with 3 new layer cards!")
else:
    print("ERROR: target not found in index.html")
