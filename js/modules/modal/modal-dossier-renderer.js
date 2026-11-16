/**
 * ===============================================================================
 * SÃO ROQUE GIS HUB · RENDERIZADOR DO DOSSIÊ MULTICAMADAS COMPLETO DO PONTO
 * ===============================================================================
 * Renderiza o dossiê pericial multidimensional com todas as camadas interligadas:
 *  - Endereçamento Geométrico e Setor Censitário IBGE 2022
 *  - Zoneamento Homologado Vigente (LC 40/2006) vs. Proposta Minuta 2026
 *  - Pedologia, Geologia e Declividade
 *  - Unidade de Conservação APA de Itupararanga (Mananciais)
 *  - Cartas Oficiais I a XIII do Plano Diretor 2026
 *  - Obras Estruturantes Prioritárias da Carta XIII (SRQ-01 a SRQ-22)
 *  - Vetor Social de Audiências Públicas
 *  - Condicionantes Jurídico-Topológicas Incidentes (33 Camadas)
 *  - Pirâmide de Kelsen Completa
 * ===============================================================================
 */

export class ModalDossierRenderer {
  constructor(escapeHTMLFn) {
    this.escapeHTML = escapeHTMLFn || ((str) => {
      if (str == null) return "";
      return String(str)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
    });
  }

  render(dossier, legalContext = null) {
    if (!dossier) return null;

    const viaNome = dossier.logradouro?.nome;
    const bairroNome = dossier.bairro?.nome;
    const distNome = dossier.distrito?.nome || "Distrito Sede";
    const ibge = dossier.setor_censitario_ibge;

    let modalTitle = viaNome 
      ? `${viaNome} (${distNome})`
      : (bairroNome ? `${bairroNome} (${distNome})` : `Ponto Territorial: ${dossier.coordenadas?.lat}, ${dossier.coordenadas?.lng}`);

    const container = document.createElement("div");
    container.className = "modal-legal-container";

    // 1. Cabeçalho Geral do Ponto
    const headerBox = document.createElement("div");
    headerBox.className = "dossier-point-header";
    headerBox.innerHTML = `
      <div class="dossier-point-title">
        <span>📍</span>
        <span>${this.escapeHTML(viaNome || bairroNome || "Ponto Territorial Selecionado")}</span>
      </div>
      <div class="dossier-point-subtitle">
        Coordenadas WGS84: ${dossier.coordenadas?.lat}, ${dossier.coordenadas?.lng} · ${this.escapeHTML(distNome)}
        ${ibge ? ` · <span class="dossier-badge dossier-badge-blue" style="font-size:0.68rem;">IBGE Setor ${this.escapeHTML(ibge.cd_setor)} (${this.escapeHTML(ibge.situacao)})</span>` : ""}
      </div>
    `;
    container.appendChild(headerBox);

    // 2. Card: Sistema Viário & Endereçamento Geométrico com Setor IBGE
    const viaCard = document.createElement("div");
    viaCard.className = "dossier-card";
    const distVia = dossier.logradouro?.distancia_m != null ? `${dossier.logradouro.distancia_m} metros` : "Sobre o eixo";
    viaCard.innerHTML = `
      <div class="dossier-card-header">
        <span>🛣️</span>
        <span>${this.escapeHTML(dossier.logradouro?.camada || "Sistema Viário Oficial & Setor Censitário IBGE")}</span>
      </div>
      <div class="dossier-grid-2">
        <div class="dossier-item"><strong>Logradouro Mais Próximo:</strong><br>${this.escapeHTML(viaNome || "Via Local não codificada")}</div>
        <div class="dossier-item"><strong>Distância ao Eixo:</strong><br><span class="dossier-badge dossier-badge-blue">${this.escapeHTML(distVia)}</span></div>
        <div class="dossier-item"><strong>Bairro / Setor Censitário:</strong><br>${this.escapeHTML(bairroNome || "Área Urbana/Rural")}</div>
        <div class="dossier-item"><strong>Divisão Distrital:</strong><br><span class="dossier-badge dossier-badge-purple">${this.escapeHTML(distNome)}</span></div>
      </div>
      ${ibge ? `
        <div class="modal-subcard" style="margin-top: 6px; font-size: 0.72rem;">
          <strong>Setor Censitário IBGE 2022:</strong> Código <code>${this.escapeHTML(ibge.cd_setor)}</code> · Situação: <strong>${this.escapeHTML(ibge.situacao)}</strong> · Área: ${ibge.area_ha ? ibge.area_ha.toFixed(2) + ' ha' : '—'}
        </div>
      ` : ""}
    `;
    container.appendChild(viaCard);

    // 3. Card: Regime Jurídico Vigente (LC 40/2006 & LC 39/2006)
    const zInfo = dossier.zoneamento_2006;
    const params = zInfo?.parametros || legalContext?.parametros;
    const zoneCard = document.createElement("div");
    zoneCard.className = "dossier-card";
    zoneCard.style.borderLeft = "4px solid #1e3a8a";
    zoneCard.innerHTML = `
      <div class="dossier-card-header" style="justify-content: space-between;">
        <div style="display: flex; align-items: center; gap: 6px;">
          <span>🏛️</span>
          <span>Regime Vigente: Zoneamento Homologado (LC 40/2006 & LC 39/2006)</span>
        </div>
        <span class="dossier-badge dossier-badge-blue">Direito Positivo em Vigor</span>
      </div>
      <div style="margin-bottom: 8px;">
        <strong style="color: #1e3a8a; font-size: 0.88rem;">${this.escapeHTML(zInfo?.legenda_oficial || "Zona de Uso do Solo Vigente")}</strong>
        <div style="font-size: 0.71rem; color: #64748b; margin-top: 2px;">
          Base Legal: Leis Complementares Municipais nº 39/2006 e nº 40/2006 (Atualmente eficazes para alvarás e certidões).
        </div>
      </div>
      ${params ? `
        <div class="urban-params-grid" style="margin-bottom: 8px;">
          <div class="urban-param-card">
            <span class="urban-param-label">Taxa Ocupação Vigente</span>
            <span class="urban-param-val">${this.escapeHTML(params.taxa_ocupacao || "—")}</span>
          </div>
          <div class="urban-param-card">
            <span class="urban-param-label">Coef. Aproveitamento Vigente</span>
            <span class="urban-param-val">${this.escapeHTML(params.coeficiente_aproveitamento || "—")}</span>
          </div>
          <div class="urban-param-card">
            <span class="urban-param-label">Gabarito Máximo Vigente</span>
            <span class="urban-param-val">${this.escapeHTML(params.gabarito_altura || "—")}</span>
          </div>
          <div class="urban-param-card">
            <span class="urban-param-label">Lote Mínimo Vigente</span>
            <span class="urban-param-val">${this.escapeHTML(params.lote_minimo || "—")}</span>
          </div>
        </div>
        ${params.recuos ? `<div class="modal-subcard" style="margin-bottom: 4px;"><strong>Recuos Mínimos:</strong> <span>${this.escapeHTML(params.recuos)}</span></div>` : ""}
        ${params.usos_admitidos && params.usos_admitidos !== "—" ? `<div class="modal-subcard" style="margin-bottom: 4px;"><strong>Usos Admitidos:</strong> <span>${this.escapeHTML(params.usos_admitidos)}</span></div>` : ""}
        ${params.restricoes && params.restricoes !== "—" ? `<div class="modal-subcard subcard-warning"><strong>Restrições & Vetos Vigentes:</strong> <span>${this.escapeHTML(params.restricoes)}</span></div>` : ""}
      ` : `<div class="dossier-item" style="color: #64748b;">Parâmetros gerais de uso e ocupação conforme LC 40/2006 homologada.</div>`}
    `;
    container.appendChild(zoneCard);

    // 4. Card: Pedologia (Solos) & Geologia do Subsolo
    const solo = dossier.pedologia_solos;
    const geol = dossier.geologia_geotecnia;
    const geoCard = document.createElement("div");
    geoCard.className = "dossier-card";
    geoCard.innerHTML = `
      <div class="dossier-card-header">
        <span>🌱⛰️</span>
        <span>Pedologia & Subsolo Geotécnico</span>
      </div>
      <div class="dossier-grid-2">
        <div class="dossier-item">
          <strong>${this.escapeHTML(solo?.camada || "Pedologia (Solos)")}:</strong><br>
          <span class="dossier-badge dossier-badge-green">${this.escapeHTML(solo?.legenda_oficial || "Classe Predominante")}</span>
          <div style="font-size: 0.7rem; color: #475569; margin-top: 3px;">
            Textura: ${this.escapeHTML(solo?.textura || "Média a Argilosa")}<br>
            Permeabilidade: ${this.escapeHTML(solo?.permeabilidade || "Moderada")}
          </div>
        </div>
        <div class="dossier-item">
          <strong>${this.escapeHTML(geol?.camada || "Geologia de Engenharia")}:</strong><br>
          <span class="dossier-badge dossier-badge-amber">${this.escapeHTML(geol?.legenda_oficial || "Formação Regional")}</span>
          <div style="font-size: 0.7rem; color: #475569; margin-top: 3px;">
            Litologia: ${this.escapeHTML(geol?.litologia || "Rochas Cristalinas")}<br>
            Geotecnia: ${this.escapeHTML(geol?.comportamento_geotecnico || "Estável fora de encostas íngremes")}
          </div>
        </div>
      </div>
      ${solo?.implicacao_obras ? `
        <div class="modal-subcard" style="margin-top: 8px; font-size: 0.71rem;">
          <strong>Aptidão Construtiva & Drenagem:</strong> ${this.escapeHTML(solo.implicacao_obras)}
        </div>
      ` : ""}
    `;
    container.appendChild(geoCard);

    // 5. Card: Mananciais e APA de Itupararanga (se aplicável)
    if (dossier.unidade_conservacao_apa) {
      const apa = dossier.unidade_conservacao_apa;
      const apaCard = document.createElement("div");
      apaCard.className = "dossier-card";
      apaCard.style.borderLeft = "4px solid #0284c7";
      apaCard.innerHTML = `
        <div class="dossier-card-header" style="color: #0369a1;">
          <span>💧</span>
          <span>${this.escapeHTML(apa.camada || "Área de Proteção Ambiental de Itupararanga")}</span>
        </div>
        <div style="font-size: 0.75rem; color: #0c4a6e; line-height: 1.4;">
          <strong>${this.escapeHTML(apa.legenda_oficial || "APA da Represa de Itupararanga")}</strong>
          <div style="margin-top: 4px;">${this.escapeHTML(apa.restricoes || "Lote mínimo 1.000m² a 5.000m²; saneamento ecológico autônomo obrigatório.")}</div>
          <div style="font-size: 0.7rem; color: #0284c7; margin-top: 4px;">
            Legislação Incidente: Leis Estaduais nº 10.100/1998 e nº 9.866/1997 (Proteção de Mananciais).
          </div>
        </div>
      `;
      container.appendChild(apaCard);
    }

    // 6. Card: Regime Proposto (Minutas de Revisão LC 39/40 & 13 Cartas do Plano Diretor 2026)
    if (dossier.plano_diretor_2026?.cartas_incidentes?.length) {
      const cartasCard = document.createElement("div");
      cartasCard.className = "dossier-card";
      cartasCard.style.borderLeft = "4px solid #d97706";
      cartasCard.innerHTML = `
        <div class="dossier-card-header" style="justify-content: space-between;">
          <div style="display: flex; align-items: center; gap: 6px;">
            <span>📜</span>
            <span>Regime Proposto: Minutas de Revisão (LC 39 e 40) & Cartas 2026</span>
          </div>
          <span class="dossier-badge dossier-badge-amber">Proposta em Tramitação</span>
        </div>
        <div style="font-size: 0.72rem; color: #475569; margin-bottom: 6px; line-height: 1.35;">
          Documentos da Proposta: <strong>Minutas Prévias de Revisão das LCs 39 e 40</strong>, Estudo Técnico PMD 2006 e <strong>Cartas Oficiais I a XIII</strong>:
        </div>
        <div class="dossier-cartas-list">
          ${dossier.plano_diretor_2026.cartas_incidentes.map(c => `<div class="dossier-carta-pill">${this.escapeHTML(c)}</div>`).join("")}
        </div>
      `;
      container.appendChild(cartasCard);
    }

    // 7. Card: Obras Estruturantes Prioritárias da Carta XIII
    if (dossier.obras_estruturantes_proximas?.length) {
      const obrasCard = document.createElement("div");
      obrasCard.className = "dossier-card";
      obrasCard.innerHTML = `
        <div class="dossier-card-header">
          <span>🏗️</span>
          <span>Obras Estruturantes Prioritárias Próximas (Carta XIII)</span>
        </div>
        <div class="dossier-obras-list">
          ${dossier.obras_estruturantes_proximas.map(o => `
            <div class="dossier-obra-card">
              <strong style="color: #b45309;">${this.escapeHTML(o.codigo)}: ${this.escapeHTML(o.nome)}</strong>
              <div style="color: #64748b; font-size: 0.7rem; margin-top: 2px;">Local: ${this.escapeHTML(o.local)}</div>
              <div style="color: #334155; margin-top: 3px;">${this.escapeHTML(o.descricao)}</div>
            </div>
          `).join("")}
        </div>
      `;
      container.appendChild(obrasCard);
    }

    // 8. Seção 5: Voz do Bairro (Câmara Municipal EPROCLEG & Moradores)
    const voz = dossier.voz_do_bairro;
    if (voz && voz.regiao_identificada) {
      const reg = voz.regiao_identificada;
      const est = voz.estatisticas_regiao || {};
      const temasRank = voz.ranking_temas || [];
      const geocodedNear = voz.proposicoes_proximas_gps || [];
      const hearingDirect = voz.pedidos_moradores_audiencias || [];

      const vozCard = document.createElement("div");
      vozCard.className = "dossier-card";
      vozCard.style.borderLeft = "4px solid #0284c7";
      vozCard.innerHTML = `
        <div class="dossier-card-header" style="justify-content: space-between; flex-wrap: wrap; gap: 6px;">
          <div style="display: flex; align-items: center; gap: 6px;">
            <span>🏛️🗣️</span>
            <span><strong>Seção 5: Voz do Bairro</strong> (Câmara Municipal & Moradores)</span>
          </div>
          <span class="dossier-badge dossier-badge-blue" style="font-size: 0.68rem;">EPROCLEG · 2017–2026</span>
        </div>

        <div style="background: rgba(2,132,199,0.06); padding: 8px 10px; border-radius: 6px; margin-bottom: 8px;">
          <div style="font-size: 0.8rem; font-weight: 700; color: #0369a1;">
            Região Parlamentar: ${this.escapeHTML(reg.nome_regiao)}
          </div>
          <div style="font-size: 0.72rem; color: #475569; margin-top: 2px;">
            <strong>${est.total_proposicoes || 0} proposições reais</strong> registradas para esta localidade:
            <span style="color: #0284c7;">• Indicações: ${est.indicacoes || 0}</span> | 
            <span style="color: #7c3aed;">• Requerimentos: ${est.requerimentos || 0}</span> | 
            <span style="color: #059669;">• Projetos de Lei: ${est.projetos_de_lei || 0}</span>
          </div>
        </div>

        <!-- 1. Ranking de Assuntos Mais Recorrentes (Barras Visuais) -->
        <div style="margin-bottom: 10px;">
          <div style="font-size: 0.74rem; font-weight: 700; color: #1e293b; margin-bottom: 4px;">
            📊 Assuntos Mais Recorrentes dos Últimos Anos (Ranking Regional):
          </div>
          <div style="display: flex; flex-direction: column; gap: 4px;">
            ${temasRank.slice(0, 5).map((t, idx) => {
              const barWidth = Math.max(8, Math.min(100, Math.round(t.percentual * 1.8)));
              return `
                <div style="font-size: 0.7rem;">
                  <div style="display: flex; justify-content: space-between; margin-bottom: 2px;">
                    <span style="color: #334155;"><strong>${idx + 1}º ${this.escapeHTML(t.tema_nome)}</strong></span>
                    <span style="color: #64748b;"><strong>${t.quantidade}</strong> protocolos (${t.percentual}%)</span>
                  </div>
                  <div style="background: #e2e8f0; height: 6px; border-radius: 3px; overflow: hidden;">
                    <div style="width: ${barWidth}%; height: 100%; background: #0284c7; border-radius: 3px;"></div>
                  </div>
                </div>
              `;
            }).join("")}
          </div>
        </div>

        <!-- 2. Protocolos Georreferenciados no Entorno Imediato (< 1.800m) -->
        ${geocodedNear.length ? `
          <div style="margin-top: 10px; margin-bottom: 8px;">
            <div style="font-size: 0.74rem; font-weight: 700; color: #1e293b; margin-bottom: 4px;">
              📍 Protocolos da Câmara no Entorno Imediato (${geocodedNear.length} no raio de 1.800m):
            </div>
            <div class="modal-laws-list" style="max-height: 220px; overflow-y: auto;">
              ${geocodedNear.slice(0, 6).map(p => `
                <div class="modal-law-item" style="border-left: 3px solid #0284c7; padding: 6px 8px;">
                  <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 6px;">
                    <div>
                      <span class="dossier-badge dossier-badge-blue" style="font-size: 0.65rem; padding: 1px 5px;">📍 ${p.distancia_m} m</span>
                      <strong style="color: #1e293b; font-size: 0.76rem; margin-left: 4px;">${this.escapeHTML(p.titulo)}</strong>
                      <div style="font-size: 0.68rem; color: #64748b; margin-top: 1px;">
                        Autor: <strong>${this.escapeHTML(p.autor)}</strong> · Protocolado em: <strong>${this.escapeHTML(p.data_formatada || p.ano)}${p.hora_formatada ? ` às ${p.hora_formatada}` : ''}</strong>
                      </div>
                    </div>
                    <a href="${this.escapeHTML(p.url_eprocleg)}" target="_blank" rel="noopener noreferrer" class="btn-law-modal-link" style="font-size: 0.65rem; padding: 2px 6px;" title="Ver protocolo oficial no portal da Câmara">
                      EPROCLEG ↗
                    </a>
                  </div>
                  <details style="margin-top: 4px; font-size: 0.71rem; color: #334155; line-height: 1.35;">
                    <summary style="cursor: pointer; color: #0284c7; font-weight: 600;">Ver texto na íntegra</summary>
                    <div style="background: #f8fafc; padding: 6px; border-radius: 4px; margin-top: 4px; border: 1px solid #e2e8f0; font-style: italic;">
                      "${this.escapeHTML(p.descricao_completa || p.descricao_resumida)}"
                    </div>
                  </details>
                </div>
              `).join("")}
            </div>
          </div>
        ` : ""}

        <!-- 3. Sugestões dos Moradores nas Audiências Públicas do Plano Diretor -->
        ${hearingDirect.length ? `
          <div style="margin-top: 10px;">
            <div style="font-size: 0.74rem; font-weight: 700; color: #1e293b; margin-bottom: 4px;">
              🗣️ Sugestões dos Moradores nas Audiências Públicas (Plano Diretor 2026):
            </div>
            ${hearingDirect.map(h => {
              const st = (h.status_prefeitura || "").toUpperCase();
              const badgeClass = st.includes("NÃO") || st.includes("NAO") 
                ? "dossier-badge-amber" 
                : (st.includes("PARCIAL") || st.includes("ENCAMINH") ? "dossier-badge-blue" : "dossier-badge-green");
              return `
                <div class="dossier-demanda-card" style="margin-bottom: 6px;">
                  <div style="display: flex; justify-content: space-between; align-items: center; gap: 4px; margin-bottom: 3px;">
                    <strong style="color: #0f172a; font-size: 0.73rem;">${this.escapeHTML(h.numeros_sugestao || "Sugestão Popular")} · ${this.escapeHTML(h.local_alvo)}</strong>
                    <span class="dossier-badge ${badgeClass}" style="font-size: 0.65rem;">${this.escapeHTML(h.status_prefeitura)}</span>
                  </div>
                  <div style="font-size: 0.7rem; color: #334155; line-height: 1.35;">
                    <strong>Pedido dos Moradores:</strong> ${this.escapeHTML(h.pedido_dos_moradores)}
                  </div>
                  <div style="font-size: 0.68rem; color: #065f46; background: #ecfdf5; padding: 4px 6px; border-radius: 4px; margin-top: 4px; border: 1px solid #a7f3d0;">
                    <strong>Resposta Oficial da Prefeitura na Minuta 2026:</strong> ${this.escapeHTML(h.resposta_oficial_minuta_2026)}
                  </div>
                </div>
              `;
            }).join("")}
          </div>
        ` : ""}
      `;
      container.appendChild(vozCard);
    } else if (dossier.demandas_populares?.length) {
      const partCard = document.createElement("div");
      partCard.className = "dossier-card";
      partCard.innerHTML = `
        <div class="dossier-card-header">
          <span>🗣️</span>
          <span>Vetor de Participação Popular (Audiências Públicas 2024–2026)</span>
        </div>
        ${dossier.demandas_populares.slice(0, 3).map(dem => `
          <div class="dossier-demanda-card">
            <strong style="color: #047857;">${this.escapeHTML(dem.tema || "Demanda Comunitária")}</strong>
            <div style="color: #475569; margin-top: 2px;">${this.escapeHTML(dem.pedido_principal)}</div>
            <div style="color: #065f46; font-size: 0.7rem; margin-top: 3px; font-style: italic;">
              Parecer Técnico: ${this.escapeHTML(dem.posicao_tecnica_prefeitura)}
            </div>
          </div>
        `).join("")}
      `;
      container.appendChild(partCard);
    }

    // 9. Card: Regras Jurídicas & Condicionantes Incidentes
    if (dossier.regras_juridicas_incidentes?.length) {
      const regrasCard = document.createElement("div");
      regrasCard.className = "dossier-card";
      regrasCard.style.borderLeft = "4px solid #ef4444";
      regrasCard.innerHTML = `
        <div class="dossier-card-header">
          <span>⚖️</span>
          <span>Regras Jurídicas & Restrições Incidentes (${dossier.regras_juridicas_incidentes.length})</span>
        </div>
        <div style="font-size: 0.72rem; color: #475569; margin-bottom: 6px;">
          Dispositivos e condicionantes normativos vinculados às camadas incidentes neste local:
        </div>
        <div class="modal-laws-list" style="max-height: 220px; overflow-y: auto;">
          ${dossier.regras_juridicas_incidentes.slice(0, 10).map(r => `
            <div class="modal-law-item" style="border-left: 3px solid ${r.grau_restricao === 'Impeditiva' ? '#ef4444' : (r.grau_restricao === 'Condicionante' ? '#f59e0b' : '#3b82f6')};">
              <div style="display: flex; justify-content: space-between; align-items: center; gap: 4px;">
                <strong style="color: #1e293b; font-size: 0.74rem;">${this.escapeHTML(r.norma)} · ${this.escapeHTML(r.artigo)}</strong>
                <span class="dossier-badge ${r.grau_restricao === 'Impeditiva' ? 'dossier-badge-amber' : 'dossier-badge-blue'}" style="font-size: 0.65rem;">
                  ${this.escapeHTML(r.grau_restricao || "Diretriz")}
                </span>
              </div>
              <div style="font-size: 0.71rem; color: #334155; margin-top: 3px; line-height: 1.35;">
                ${this.escapeHTML(r.regra)}
              </div>
              ${r.ponto_atencao ? `
                <div style="font-size: 0.68rem; color: #b91c1c; margin-top: 2px; font-weight: 600;">
                  ⚠️ ${this.escapeHTML(r.ponto_atencao)}
                </div>
              ` : ""}
            </div>
          `).join("")}
        </div>
      `;
      container.appendChild(regrasCard);
    }

    // 10. Card: Pirâmide de Kelsen Completa
    const applicableLaws = legalContext?.leis_aplicaveis || [];
    if (applicableLaws.length > 0) {
      const federais = applicableLaws.filter((l) => l.esfera_cat === "federal" || l.tipo?.includes("Federal") || String(l.esfera_label || "").includes("Federal"));
      const estaduais = applicableLaws.filter((l) => l.esfera_cat === "estadual" || l.tipo?.includes("Estadual") || String(l.esfera_label || "").includes("Estadual"));
      const municipais = applicableLaws.filter((l) => l.esfera_cat === "municipal" || l.tipo?.includes("Municipal") || l.tipo?.includes("Complementar") || String(l.esfera_label || "").includes("Municipal"));

      const groups = [
        { title: "🔺 1. Esfera Federal (Teto Normativo e Parcelamento do Solo)", list: federais, color: "#1d4ed8" },
        { title: "🔺 2. Esfera Estadual (Condicionantes Regionais e Mananciais)", list: estaduais, color: "#059669" },
        { title: "🔺 3. Esfera Municipal (Zoneamento Local e Uso do Solo)", list: municipais, color: "#7c3aed" }
      ];

      const lawsCard = document.createElement("div");
      lawsCard.className = "dossier-card";
      lawsCard.innerHTML = `
        <div class="dossier-card-header">
          <span>⚖️</span>
          <span>Precedência Normativa Aplicável a este Ponto (${applicableLaws.length} Leis)</span>
        </div>
        <div class="pyramid-banner" style="margin-bottom: 8px;">
          <strong>🔺 Pirâmide de Kelsen:</strong> Prevalência automática das normas superiores com observância ao interesse local e à máxima proteção ambiental.
        </div>
      `;

      const lawsList = document.createElement("div");
      lawsList.className = "modal-laws-list";

      groups.forEach((grp) => {
        if (grp.list.length === 0) return;

        const grpHeader = document.createElement("div");
        grpHeader.style.fontSize = "0.74rem";
        grpHeader.style.fontWeight = "700";
        grpHeader.style.color = grp.color;
        grpHeader.style.marginTop = "8px";
        grpHeader.style.marginBottom = "3px";
        grpHeader.textContent = grp.title;
        lawsList.appendChild(grpHeader);

        grp.list.slice(0, 5).forEach((law) => {
          const lawItem = document.createElement("div");
          lawItem.className = "modal-law-item";
          lawItem.style.borderLeftColor = grp.color;
          lawItem.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 8px;">
              <div>
                <strong style="color: #1e293b; font-size: 0.82rem;">${this.escapeHTML(law.tipo)} nº ${this.escapeHTML(law.numero)}/${this.escapeHTML(String(law.ano))}</strong>
                <div style="font-size: 0.72rem; color: #64748b; margin-top: 2px;">
                  ${this.escapeHTML(law.tag_ambito || law.ambito_territorial || "Âmbito Territorial")}
                </div>
              </div>
              <a href="${this.escapeHTML(law.link_oficial)}" target="_blank" rel="noopener noreferrer" class="btn-law-modal-link" title="Abrir link oficial da norma">
                Oficial ↗
              </a>
            </div>
            <p style="font-size: 0.73rem; color: #334155; margin-top: 5px; line-height: 1.35;">
              ${this.escapeHTML(law.ementa || "")}
            </p>
          `;
          lawsList.appendChild(lawItem);
        });
      });

      lawsCard.appendChild(lawsList);
      container.appendChild(lawsCard);
    }

    return {
      title: modalTitle,
      container
    };
  }
}
