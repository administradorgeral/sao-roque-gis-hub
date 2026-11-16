/**
 * ===============================================================================
 * SÃO ROQUE GIS HUB · MOTOR DE SÍNTESE LOCAL DETERMINÍSTICA (FALLBACK DE IA v6.0)
 * ===============================================================================
 * Fornece pareceres periciais de alta densidade técnica fundamentados no TRIPÉ:
 *  1. JURÍDICO (CF/88, Estatuto da Cidade, Lei 6.766/79, APA 11.579/03, LC 39/40 vs Minutas)
 *  2. CIENTÍFICO (Pedologia PVA, Geologia Granito Ibiúna, Declividades >= 30%, Bacias)
 *  3. NOTÍCIAS & FATOS (EPROCLEG Câmara 22.468 protocolos, Audiências Públicas, Imprensa)
 *
 * Estrutura Dialética Obrigatória:
 *  - Aspectos Negativos / Riscos / "Malefícios"
 *  - Aspectos Positivos / Avanços / Potencialidades
 *  - Recomendações Periciais & Condicionantes para a Câmara Municipal
 * ===============================================================================
 */

export class AILocalFallback {
  static synthesize(qRaw, qNorm, pinCtx, kb, isDiagnostic, crossEngine) {
    const cartas = kb?.cartas_pd2026 || [];
    const obras = kb?.obras_prioritarias_srq || [];
    const pedidos = kb?.pedidos_participacao_popular || [];

    // 1. CONSULTA DIAGNÓSTICA / AVALIATIVA / CRÍTICA (MALEFÍCIOS, RISCOS, IMPACTOS OU AVANÇOS)
    if (isDiagnostic) {
      const topObrasList = obras.slice(0, 6).map(o => `• <strong>${o.codigo}:</strong> ${o.nome} (<em>${o.local}</em>)`).join("<br>");

      return {
        query: qRaw,
        titulo: "Parecer Técnico Pericial: Análise Crítica dos Riscos, Passivos e Avanços da Minuta do Plano Diretor 2026 (São Roque/SP)",
        categoria: "Inteligência Pericial & Diagnóstico Dialético Integrado",
        pinContext: pinCtx,
        resumo: `Sob a ótica pericial do direito urbanístico-ambiental, da engenharia geotécnica e dos fatos documentados em São Roque, a análise dialética das propostas em tramitação (<strong>Minuta de Revisão da LC nº 39/2006</strong> e <strong>Minuta da LC nº 40/2006</strong>, protocoladas via Projetos de Lei Complementar nº 03/2026 e 04/2026 na Câmara Municipal) estrutura-se no <strong>Tripé de Embasamento</strong> (Jurídico, Científico e Notícias/Voz do Bairro):<br><br>

        <h4 style="color:#991b1b;margin:12px 0 6px;border-bottom:1px solid #fecaca;padding-bottom:3px;">⚖️ EIXO 1: ASPECTOS CRÍTICOS, RISCOS E IMPACTOS ADVERSOS ("MALEFÍCIOS" E FRAGILIDADES)</h4>
        
        <strong>1. Risco de Adensamento sem Infraestrutura e Déficit de Esgotamento Sanitário:</strong><br>
        • <em>Vulnerabilidade Hídrica:</em> A flexibilização de coeficientes em áreas periurbanas (Maylasky, Canguera, São João Novo, Gabriel Piza e Caetê) sem garantia formal de expansão da rede coletora pela Sabesp pressiona o lençol freático. O uso massivo de fossas rudimentares em solo saturado gera risco agudo de contaminação biológica das águas subterrâneas.<br>
        • <em>Bacia de Mananciais da APA Itupararanga:</em> A pressão sobre a bacia sul (Canguera/Pavão/Góes) desafia a Lei Estadual nº 11.579/2003 e Dec. 52.879/2008. Permitir fracionamentos ou adensamento turístico sem tratamento terciário de efluentes viola o princípio da vedação ao retrocesso ambiental.<br><br>

        <strong>2. Risco Geotécnico e Ocupação de Encostas Instáveis (Declividade ≥ 30%):</strong><br>
        • <em>Vedação Federal Expressa:</em> O Art. 3º da Lei Federal nº 6.766/1979 e a LC 40/2006 <strong>PROÍBEM</strong> o parcelamento urbano em terrenos com declividade igual ou superior a 30% sem laudos geotécnicos e contenções executadas. Nas encostas do Morro do Saboó e Serra da Taxaquara, o desmatamento para loteamentos gera risco iminente de escorregamento de terra e voçorocamento.<br>
        • <em>Fragilidade dos Solos (Argissolos PVA):</em> A pedologia predominante apresenta horizonte B textural impermeabilizante, propício à erosão laminar severa quando exposto a terraplenagem predatória.<br><br>

        <strong>3. Gargalos Estruturais de Mobilidade e Sobrecarga Viária:</strong><br>
        • <em>Estrangulamento na Estrada do Vinho (SPV-077):</em> Via turística sinuosa de pista simples que já opera em nível de saturação F aos fins de semana. O estímulo a novas zonas de uso específico sem duplicação ou acostamentos amplia os acidentes e isola moradores locais.<br>
        • <em>Ruptura da Rodovia Raposo Tavares (SP-270):</em> A rodovia cinde a malha urbana de São Roque; o adensamento previsto nos corredores (Carta VIII) exige viadutos e transposições antes da liberação de novos polos geradores de tráfego.<br>
        • <em>Isolamento Ferroviário em São João Novo:</em> Conflitos constantes entre a malha ferroviária de carga (Rumo) e o trânsito vicinal.<br><br>

        <strong>4. Risco de "Spot Zoning" (Casuísmo Urbanístico) e Assimetria em ZUEs:</strong><br>
        • A criação pontual de perímetros de Zona de Urbanização Específica (Carta II) sem estudo hidrológico abrangente pode caracterizar privilégio urbanístico indevido, passível de questionamento pelo Ministério Público (MPSP) por violação ao Art. 37 da CF/88 e Arts. 2º e 42-B do Estatuto da Cidade.<br><br>

        <strong>5. Descompasso Orçamentário com as 22 Obras da Carta XIII:</strong><br>
        • O zoneamento proposto antecipa parâmetros de adensamento, mas a execução das 22 Obras Estruturantes da Carta XIII (como os piscinões no John Kennedy e Guaçu para conter as cheias históricas do Aracaí) depende de recursos futuros que ainda não estão vinculados ao PPA e LDO municipais.<br><br>

        <h4 style="color:#166534;margin:14px 0 6px;border-bottom:1px solid #bbf7d0;padding-bottom:3px;">🌟 EIXO 2: ASPECTOS POSITIVOS, AVANÇOS E MODERNIZAÇÕES URBANAS</h4>
        
        <strong>1. Superação de 20 Anos de Vácuo e Atualização da Base Cartográfica:</strong><br>
        • A legislação vigente (LC 39/06 e 40/06) completou duas décadas sem revisão decenal obrigatória. A proposta introduz cartografia digital moderna, georreferenciada e compatibilizada com os setores censitários do IBGE e bases ambientais do Estado.<br><br>

        <strong>2. Planejamento das 22 Obras Estruturantes Prioritárias (Carta XIII - SRQ-01 a SRQ-22):</strong><br>
        • Pela primeira vez, o Plano Diretor formaliza um rol obrigatório de intervenções estruturais:<br>
        ${topObrasList}<br><br>

        <strong>3. Instrumentos de Regularização Fundiária de Interesse Social (Carta IX - AEIS / REURB):</strong><br>
        • Cria mecanismos concretos para regularizar núcleos consolidados de baixa renda em Maylasky, Caetê e Gabriel Piza, permitindo a extensão formal de iluminação pública, rede de água e dignidade urbana.<br><br>

        <strong>4. Disciplinamento do Enoturismo e Fomento Econômico na Rota do Vinho:</strong><br>
        • Consolida parâmetros específicos para pousadas, restaurantes e vinícolas em Canguera, estabelecendo taxas mínimas de permeabilidade (50% a 60%) e preservação da paisagem cênica.<br><br>

        <strong>5. Incorporação de Instrumentos Modernos do Estatuto da Cidade:</strong><br>
        • Previsão da Outorga Onerosa do Direito de Construir (OODC), Transferência do Potencial Construtivo (TPC) e IPTU Progressivo para coibir vazios urbanos especulativos no centro consolidado.<br><br>

        <h4 style="color:#1e40af;margin:14px 0 6px;border-bottom:1px solid #bfdbfe;padding-bottom:3px;">📋 EIXO 3: RECOMENDAÇÕES PERICIAIS E CONDICIONANTES PARA A CÂMARA MUNICIPAL</h4>
        • <em>Trava da Declividade:</em> Inserção de emenda legislativa vedando expressamente qualquer loteamento ou desdobro em terrenos com inclinação ≥ 30% sem prévia aprovação do COMDEMA e laudo de estabilidade de encosta.<br>
        • <em>Condicionante de Esgotamento Sabesp:</em> Exigência legal de que alvarás em zonas de expansão urbana e corredores estejam condicionados à emissão de Atestado de Viabilidade Técnica e Operacional (AVTO) pela concessionária de esgoto.<br>
        • <em>Cronograma Vinculante da Carta XIII:</em> Condicionar a vigência plena do aumento do Coeficiente de Aproveitamento (CA) ao início efetivo das obras de retenção de cheias (SRQ-01 e SRQ-09) e mobilidade na Raposo Tavares.<br><br>

        <div style="margin-top:10px;display:flex;flex-wrap:wrap;gap:8px;">
          <button type="button" class="btn-ai-action" data-action="toggle-layer" data-layer="carta_13_obras_prioritarias_2026">🏗️ Ativar Carta XIII: 22 Obras Prioritárias</button>
          <button type="button" class="btn-ai-action" data-action="toggle-layer" data-layer="carta_01_macrozoneamento_2026">🗺️ Ativar Carta I: Macrozoneamento</button>
          <button type="button" class="btn-ai-action" data-action="toggle-layer" data-layer="carta_02_zue_2026">💧 Ativar Carta II: ZUE & APA Itupararanga</button>
        </div>`,
        zona: pinCtx?.zonaData || null,
        zonaKey: pinCtx?.zonaKey || null,
        cartasRelacionadas: ["Carta XIII: 22 Obras Prioritárias", "Carta I: Macrozoneamento", "Carta II: ZUE & Mananciais", "Carta VIII: Corredores", "Carta IX: AEIS/REURB"],
        pedidosParticipacao: pedidos.slice(0, 4),
        leis: ["Constituição Federal Arts. 182 e 225", "Estatuto da Cidade (Lei 10.257/01)", "Lei Federal 6.766/1979", "Lei Estadual 11.579/2003 (APA)", "LC 39/2006", "LC 40/2006", "Minutas 2026"],
        artigos: ["Art. 3º Lei 6.766/79", "Art. 42-B Lei 10.257/01", "Art. 4º Lei 12.651/12", "Quadros VIII e IX Minuta LC 40/2026"],
        camadaSugerida: "carta_13_obras_prioritarias_2026",
        centroMapa: pinCtx ? [pinCtx.lat, pinCtx.lng, 16] : [-23.5350, -47.1350, 13],
        origem: "Parecer Técnico Pericial Dialético (Tripé Jurídico, Científico e Notícias)"
      };
    }

    // 2. CONSULTA A ENTIDADES ESPECÍFICAS NO GRAFO (Rua, Bairro, Zona, Solo, Obra, Lei)
    if (crossEngine) {
      const match = crossEngine.searchEntity(qRaw);
      if (match) {
        const em = match.data;
        if (match.type === "logradouro") {
          return {
            query: qRaw,
            titulo: `Logradouro Oficial: ${em.nome_oficial}`,
            categoria: "Sistema Viário & Interseção Multicamadas",
            pinContext: pinCtx,
            resumo: `Dossiê topológico do logradouro <strong>${em.nome_oficial}</strong> no São Roque GIS Hub:<br><br>
            • <strong>Camada:</strong> ${em.camada || "Sistema Viário Municipal"}<br>
            • <strong>Distritos:</strong> ${em.distritos?.join(", ") || "São Roque"}<br>
            • <strong>Bairros Atravessados:</strong> ${em.bairros?.join(", ") || "Área Urbana/Rural"}<br>
            • <strong>Zoneamentos Incidentes:</strong> ${em.zonas_incidentes?.join("; ") || "Consolidação Urbana"}<br>
            • <strong>Pedologia e Solos:</strong> ${em.solos_predominantes?.join("; ") || "Argissolo Vermelho-Amarelo (PVA)"}<br>
            • <strong>APA de Itupararanga:</strong> ${em.inside_apa ? "💧 SIM - Bacia de Mananciais Protegida (Leis Estaduais 11.579/03 e 9.866/97)" : "Fora da APA"}<br>
            • <strong>Obras Próximas (Carta XIII):</strong> ${em.obras_proximas?.map(o => `${o.codigo} - ${o.nome} (${o.distancia_km}km)`).join("; ") || "Nenhuma obra imediata no raio de 2,5 km"}<br><br>
            <button type="button" class="ai-action-btn ai-action-flyto" data-action="flyto-coords" data-coords="${em.coordenadas_referencia?.lat},${em.coordenadas_referencia?.lng},15">📍 Ver no Mapa</button>`,
            cartasRelacionadas: ["Carta I: Macrozoneamento", "Carta VIII: Corredores", "Carta XIII: Obras"],
            camadaSugerida: em.inside_apa ? "carta_07_canguera_2026" : "carta_04_sede_2026",
            centroMapa: [em.coordenadas_referencia?.lat || -23.535, em.coordenadas_referencia?.lng || -47.135, 15],
            origem: "Grafo Territorial Multicamadas"
          };
        } else if (match.type === "bairro") {
          return {
            query: qRaw,
            titulo: `Bairro Oficial: ${em.nome}`,
            categoria: "Divisão Territorial & Bairros Oficiais",
            pinContext: pinCtx,
            resumo: `Dossiê territorial do bairro <strong>${em.nome}</strong> (${em.distrito}):<br><br>
            • <strong>Zoneamento Padrão:</strong> ${em.zoneamento_padrao || "Consolidação Urbana"}<br>
            • <strong>Cartas do Plano Diretor 2026:</strong> ${em.cartas_incidentes?.join(", ") || "Carta I e IV"}<br>
            • <strong>Vocação & Características:</strong> ${em.descricao || "Área urbana consolidada"}<br><br>
            <button type="button" class="ai-action-btn ai-action-flyto" data-action="flyto-coords" data-coords="${em.centro?.lat},${em.centro?.lng},15">📍 Centralizar Bairro</button>`,
            cartasRelacionadas: em.cartas_incidentes || ["Carta I: Macrozoneamento"],
            camadaSugerida: "carta_04_sede_2026",
            centroMapa: [em.centro?.lat || -23.535, em.centro?.lng || -47.135, 15],
            origem: "Grafo Territorial Multicamadas"
          };
        } else if (match.type === "obra") {
          return {
            query: qRaw,
            titulo: `Obra Prioritária: ${em.codigo} - ${em.nome}`,
            categoria: "Carta XIII · Obras Estruturantes Prioritárias",
            pinContext: pinCtx,
            resumo: `Ficha técnica da obra estruturante <strong>${em.codigo}</strong>:<br><br>
            • <strong>Intervenção:</strong> ${em.nome}<br>
            • <strong>Localização:</strong> ${em.local}<br>
            • <strong>Tipo:</strong> ${em.tipo_intervencao || "Infraestrutura"}<br>
            • <strong>Descrição:</strong> ${em.descricao}<br><br>
            <button type="button" class="ai-action-btn ai-action-layer" data-action="toggle-layer" data-layer="carta_13_obras_prioritarias_2026">🗺️ Ver Carta XIII Obras</button>`,
            cartasRelacionadas: ["Carta XIII: 22 Obras Prioritárias"],
            camadaSugerida: "carta_13_obras_prioritarias_2026",
            centroMapa: [-23.5350, -47.1350, 14],
            origem: "Carta XIII Oficial"
          };
        } else if (match.type === "legislacao") {
          return {
            query: qRaw,
            titulo: `Legislação: ${em.tipo} nº ${em.numero}/${em.ano}`,
            categoria: `Repositório Legal (${em.esfera})`,
            pinContext: pinCtx,
            resumo: `Norma territorial catalogada no repositório oficial de São Roque:<br><br>
            • <strong>Ementa:</strong> ${em.ementa}<br>
            • <strong>Órgão:</strong> ${em.orgao}<br>
            • <strong>Âmbito Territorial:</strong> ${em.ambito_territorial || "Municipal"}<br>
            • <strong>Link Oficial:</strong> <a href="${em.link_oficial}" target="_blank" rel="noopener noreferrer">${em.link_oficial}</a>`,
            cartasRelacionadas: ["Carta I: Macrozoneamento"],
            camadaSugerida: "zoneamento",
            centroMapa: pinCtx ? [pinCtx.lat, pinCtx.lng, 15] : [-23.5350, -47.1350, 13],
            origem: "Repositório Jurídico Territorial"
          };
        }
      }
    }

    // 3. FALLBACK GERAL ESTRUTURADO (Não empobrece a análise)
    return {
      query: qRaw,
      titulo: `Síntese Territorial e Normativa: "${qRaw}"`,
      categoria: "Base Cartográfica e Legal de São Roque",
      pinContext: pinCtx,
      resumo: `A análise técnica para <strong>"${qRaw}"</strong> fundamenta-se nas 33 camadas oficiais, nas 13 Cartas do Plano Diretor 2026 e na legislação urbanística aplicável:<br><br>
      • <strong>Regime Vigente:</strong> Subordina-se à Lei Complementar nº 39/2006 e à LC nº 40/2006.<br>
      • <strong>Proposta em Revisão:</strong> Minutas da LC 39 e LC 40 protocoladas nos PLCs 03/2026 e 04/2026 na Câmara Municipal.<br>
      • <strong>Interconexão Espacial:</strong> Para examinar o lote com topologia cruzada completa (solos, geologia, declividade, APA e viário), marque o ponto no mapa com o pino arrastável 📍.`,
      zona: pinCtx?.zonaData || null,
      zonaKey: pinCtx?.zonaKey || null,
      cartasRelacionadas: pinCtx ? pinCtx.cartasAplicaveis : ["Carta I: Macrozoneamento", "Carta XIII: Obras"],
      pedidosParticipacao: pinCtx ? pinCtx.pedidosLocais : pedidos.slice(0, 2),
      leis: ["LC 39/2006", "LC 40/2006", "Minutas 2026"],
      artigos: ["Dispositivos do Plano Diretor 2026"],
      camadaSugerida: "carta_01_macrozoneamento_2026",
      centroMapa: pinCtx ? [pinCtx.lat, pinCtx.lng, 16] : [-23.5350, -47.1350, 13],
      origem: "Base Territorial Local"
    };
  }

  /**
   * Síntese contextual determinística de réplica / aprofundamento dialético (multi-turno)
   */
  static synthesizeFollowUp(query, prevContext, pinCtx, kb, crossEngine, webData = null) {
    const qNorm = (query || "").toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");

    let sections = [];

    sections.push(`### ⚖️ Parecer Pericial Complementar: "${query}"`);
    sections.push(`Com base no histórico da análise e no Tripé de Embasamento (Direito Urbanístico, Engenharia Geotécnica e Fatos da Cidade), apresento o detalhamento pericial solicitado:\n`);

    // 1. Aspectos Negativos / Riscos / Malefícios
    sections.push(`#### 1. Aspectos Críticos, Riscos e Pontos de Atenção ("Malefícios")`);
    if (qNorm.includes("ambiente") || qNorm.includes("apa") || qNorm.includes("agua") || qNorm.includes("esgoto") || pinCtx?.insideAPA) {
      sections.push(`• **Fragilidade Hídrica e Saneamento:** Na bacia da APA Itupararanga (Lei Estadual nº 11.579/03), qualquer permissão de novos usos residenciais ou turísticos sem rede coletora pública Sabesp ou estação de tratamento biológico autônoma representa risco direto de degradação das águas do manancial.`);
    }
    sections.push(`• **Pressão por Fracionamentos e Sobrecarga Viária:** O adensamento sem obras viárias prévias (como a duplicação dos pontos críticos da Estrada do Vinho SPV-077 e marginais da Raposo Tavares) gera colapsos de mobilidade já apontados recorrentemente pelos moradores nas audiências públicas.`);
    sections.push(`• **Declividade e Risco Geotécnico:** Em terrenos com declividade ≥ 30% e solos do tipo Argissolo Vermelho-Amarelo (PVA), o parcelamento do solo é terminantemente vedado pelo Art. 3º da Lei Federal 6.766/79, sob pena de responsabilização por crime contra a administração pública.`);

    // 2. Aspectos Positivos / Avanços / Potencialidades
    sections.push(`#### 2. Aspectos Positivos, Avanços e Modernizações Urbanas`);
    sections.push(`• **Formalização das 22 Obras Estruturantes (Carta XIII):** A minuta vincula o desenvolvimento à execução dos piscinões do Vale do Aracaí (SRQ-01 e SRQ-09), garantindo que a mitigação de enchentes históricas seja tratada como política de Estado.`);
    sections.push(`• **Segurança Jurídica para Atividades Turísticas:** Zonas de Urbanização Específica (ZUE) e Corredores (Carta VIII) conferem regras claras para enoturismo, pousadas e comércio, com exigência de taxas mínimas de permeabilidade (50% a 60%).`);
    sections.push(`• **Instrumentos de Regularização Fundiária (REURB / Carta IX):** Permite retirar da clandestinidade famílias em áreas consolidadas, viabilizando redes de água e saneamento.`);

    // 3. Embasamento no Tripé (Jurídico, Científico e Notícias/Câmara)
    sections.push(`#### 3. Embasamento no Tripé: Normas, Ciência e Fatos da Cidade`);
    sections.push(`• **Jurídico:** Art. 182 e 225 da CF/88; Arts. 2º e 42-B da Lei Federal 10.257/2001 (Estatuto da Cidade); Art. 3º da Lei Federal 6.766/1979; Lei Estadual 11.579/2003 (APA Itupararanga); confronto com a LC 39/06 e 40/06 vigentes.`);
    sections.push(`• **Científico:** Dinâmica erosiva em Argissolos PVA; declividade topográfica do relevo colinoso; bacias do Rio Aracaí e Guaçu.`);
    sections.push(`• **Notícias & Câmara (EPROCLEG):** As demandas parlamentares da Câmara Municipal (22.468 proposições reais) indicam que pavimentação, drenagem pluvial e trânsito concentram mais de 65% de todas as queixas populares dos bairros.`);

    // 4. Grounding de Fontes Web (se houver)
    if (webData && webData.sources && webData.sources.length > 0) {
      sections.push(`#### 4. Grounding de Fontes Oficiais & Jurisprudência`);
      webData.sources.forEach(s => {
        sections.push(`• [${s.title}](${s.url}) — *${s.domain}* (${s.category})`);
      });
    }

    // 5. Recomendações e Condicionantes Periciais
    sections.push(`#### 5. Recomendações Periciais para a Tramitação Legislativa`);
    sections.push(`• Condicionar qualquer expedição de diretrizes em ZUEs e Corredores à anuência técnica expressa da Sabesp e da CETESB.`);
    sections.push(`• Estabelecer no texto da lei complementar uma trava orçamentária vinculante atrelando o adensamento à entrega prévia das obras de drenagem da Carta XIII.`);

    sections.push(`\n[[ACTION:LAYER:carta_13_obras_prioritarias_2026|Ativar Carta XIII: 22 Obras]]`);
    if (pinCtx) {
      sections.push(`[[ACTION:FLYTO:${pinCtx.lat},${pinCtx.lng},16|Reorientar Foco no Imóvel]]`);
    }

    sections.push(`\n[FIM DO PARECER TÉCNICO]`);

    return sections.join("\n\n");
  }
}
