with open("index.html", "r", encoding="utf-8") as f:
    text = f.read()

old_card = """          <!-- Camada Federal 1: Proteção Aeroportuária e ASA - Aeroporto Catarina (SBJH) -->
          <div class="layer-card">
            <div class="layer-card-top">
              <div class="layer-info">
                <div class="layer-bullet" style="background: #EA580C; border: 1px dashed #0284C7;"></div>
                <div class="layer-texts">
                  <span class="layer-name">Proteção Aeroportuária e ASA (Aeroporto Catarina)</span>
                  <span class="layer-tag">Servidões Aeronáuticas · Pista 13/31 · PBZPA / PBZR · ASA 20 km</span>
                  <div style="display: flex; gap: 4px; flex-wrap: wrap; margin-top: 3px;">
                    <span class="badge-audit badge-orange" title="Código Brasileiro de Aeronáutica (Arts. 43-47)">✈️ CBA (Lei 7.565/86)</span>
                    <span class="badge-audit badge-purple" title="Instrução do Comando da Aeronáutica - Gabarito e SLO">📐 DECEA / ICA 11-408</span>
                    <span class="badge-audit badge-blue" title="Plano de Zoneamento de Ruído ANAC">🔇 RBAC 161 (Ruído)</span>
                    <span class="badge-audit badge-green" title="Lei do Perigo Aviário / ASA de 20 km">🦅 Lei 12.725/12 (ASA 20km)</span>
                  </div>
                </div>
              </div>
              <label class="switch" title="Alternar visualização da proteção aeroportuária e ASA do Aeroporto Catarina">
                <input type="checkbox" id="toggle-zona-protecao-aeroportuaria-catarina" aria-label="Ativar ou desativar proteção aeroportuária">
                <span class="slider"></span>
              </label>
            </div>

            <div class="layer-controls">
              <div class="opacity-box full-width">
                <span class="opacity-label">Opacidade</span>
                <input type="range" id="opacity-zona-protecao-aeroportuaria-catarina" class="opacity-range" min="0.1" max="1" step="0.05" value="0.70" aria-label="Ajustar opacidade da camada de proteção aeroportuária">
              </div>
            </div>

            <!-- Legenda Rápida Aeroportuária (Acordeão) -->
            <div class="legend-accordion">
              <button class="legend-toggle" type="button" aria-expanded="false" aria-controls="legend-zona-protecao-aeroportuaria-catarina">
                <span class="legend-toggle-text">📊 Ver Legenda Aeronáutica</span>
                <span class="legend-icon">▼</span>
              </button>
              <div id="legend-zona-protecao-aeroportuaria-catarina" class="zone-legend-grid" aria-hidden="true">
                <span class="zone-chip" title="Pista 13/31 do Aeroporto Executivo Internacional Catarina (2.470 m x 45 m)"><span class="zone-dot" style="background: #0284C7;"></span> Pista 13/31 (SBJH)</span>
                <span class="zone-chip" title="Cone de aproximação, decolagem e transição (ICA 11-408) e Ruído (RBAC 161)"><span class="zone-dot" style="background: #EA580C;"></span> Cone de Proteção / SLO / Ruído</span>
                <span class="zone-chip" title="Área de Segurança Aeroportuária - Raio de 20 km (Lei 12.725/12 - 21.648 ha em São Roque)"><span class="zone-dot" style="background: #F59E0B;"></span> ASA Raio 20 km (Risco Aviário)</span>
              </div>
            </div>
          </div>"""

new_card = """          <!-- Camada Federal 1: Proteção Aeroportuária, Helipontos e TMA (DECEA / ANAC) -->
          <div class="layer-card">
            <div class="layer-card-top">
              <div class="layer-info">
                <div class="layer-bullet" style="background: #EA580C; border: 1.5px solid #0284C7;"></div>
                <div class="layer-texts">
                  <span class="layer-name">Proteção Aeroportuária e Helipontos (DECEA / ANAC)</span>
                  <span class="layer-tag">Catarina (SBJH) · 3 Helipontos Homologados · Congonhas (SBSP 45km)</span>
                  <div style="display: flex; gap: 4px; flex-wrap: wrap; margin-top: 3px;">
                    <span class="badge-audit badge-orange" title="Código Brasileiro de Aeronáutica (Arts. 43-47) - Servidão Federal">✈️ CBA (Lei 7.565/86)</span>
                    <span class="badge-audit badge-purple" title="Instrução do Comando da Aeronáutica - Superfícies Limitadoras e Gabarito">📐 ICA 11-408 & RBAC 155</span>
                    <span class="badge-audit badge-blue" title="Portarias DECEA / SYSAGA: 176/DGCEA, 394/ICA, 230/SAGA, 1465/SAGA, 28/ICA">📜 Portarias DECEA</span>
                    <span class="badge-audit badge-green" title="Helipontos na Estrada do Vinho e Gabriel Piza">🚁 3 Helipontos Homologados</span>
                  </div>
                </div>
              </div>
              <label class="switch" title="Alternar visualização da proteção aeroportuária, helipontos e espaço aéreo">
                <input type="checkbox" id="toggle-zona-protecao-aeroportuaria-catarina" aria-label="Ativar ou desativar proteção aeroportuária e helipontos">
                <span class="slider"></span>
              </label>
            </div>

            <div class="layer-controls">
              <div class="opacity-box full-width">
                <span class="opacity-label">Opacidade</span>
                <input type="range" id="opacity-zona-protecao-aeroportuaria-catarina" class="opacity-range" min="0.1" max="1" step="0.05" value="0.70" aria-label="Ajustar opacidade da camada de proteção aeroportuária">
              </div>
            </div>

            <!-- Legenda Rápida Aeroportuária (Acordeão) -->
            <div class="legend-accordion">
              <button class="legend-toggle" type="button" aria-expanded="false" aria-controls="legend-zona-protecao-aeroportuaria-catarina">
                <span class="legend-toggle-text">📊 Ver Legenda Aeronáutica & Helipontos</span>
                <span class="legend-icon">▼</span>
              </button>
              <div id="legend-zona-protecao-aeroportuaria-catarina" class="zone-legend-grid" aria-hidden="true">
                <span class="zone-chip" title="Pista 13/31 do Aeroporto Executivo Internacional Catarina (2.470 m x 45 m)"><span class="zone-dot" style="background: #0284C7;"></span> Pista 13/31 (SBJH)</span>
                <span class="zone-chip" title="Cone de aproximação, decolagem e transição (ICA 11-408) e Ruído (RBAC 161)"><span class="zone-dot" style="background: #EA580C;"></span> Cone de Proteção / SLO (SBJH)</span>
                <span class="zone-chip" title="Piso de Toque (FATO/TLOF): Vila Don Patto (SWVD), Taxaquara (SIZT) e NÓR Hotel"><span class="zone-dot" style="background: #DC2626;"></span> Helipontos FATO (SWVD, SIZT, NÓR)</span>
                <span class="zone-chip" title="Plano de Zona de Proteção de Helipontos - Rampa de Aproximação 1.000m (8% a 12,5%)"><span class="zone-dot" style="background: #F43F5E;"></span> PZPH Funil Aproximação (1.000m)</span>
                <span class="zone-chip" title="Superfície Horizontal Externa de Congonhas (Portaria 28/ICA - Raio 45 km / TMA-SP - 10.603 ha)"><span class="zone-dot" style="background: #8B5CF6;"></span> Congonhas SHE (SBSP / 10.603 ha)</span>
                <span class="zone-chip" title="Área de Segurança Aeroportuária - Raio de 20 km (Lei 12.725/12 - 21.648 ha em São Roque)"><span class="zone-dot" style="background: #F59E0B;"></span> ASA Raio 20 km (Risco Aviário)</span>
              </div>
            </div>
          </div>"""

norm_text = text.replace("\r\n", "\n")
norm_old = old_card.replace("\r\n", "\n")
norm_new = new_card.replace("\r\n", "\n")

if norm_old in norm_text:
    norm_text = norm_text.replace(norm_old, norm_new)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(norm_text)
    print("SUCCESS: index.html updated with complete aeronautical card!")
else:
    print("ERROR: old_card not found in index.html")
