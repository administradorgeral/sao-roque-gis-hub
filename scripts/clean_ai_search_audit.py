import re

path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\modules\ai-search.js"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Remove anomaliaPerimetral from pinCtx block
target1 = """      if (pinCtx.anomaliaPerimetral) {
        const a = pinCtx.anomaliaPerimetral;
        parts.push(`[ALERTA PERICIAL DE ANOMALIA PERIMETRAL NO PONTO SELECIONADO]
- Zona 2026 Proposta: ${a.nome_2026} (FID ${a.fid})
- Score SAP: ${a.sap_score}/100 (Risco Pericial: ${a.nivel_risco})
- Compacidade Morfológica (Polsby-Popper): ${a.polsby_popper} (referência: < 0.15 indica contorno casuístico de matrículas privadas)
- Salto de Potencial (CA): ${a.ca_2006_estimado} -> ${a.ca_2026_proposto} (${a.salto_ca_ratio}x)
- Transição de Área Rural: ${a.transicao_rural_pct}%
- Na Bacia da APA Itupararanga: ${a.dentro_apa ? "SIM (Manancial)" : "NÃO"}
- Motivos Técnicos: ${a.principais_motivos?.join("; ") || "Anomalia perimetral identificada"}
- Artigos e Precedentes Violados: ${a.artigos_violados?.join("; ") || "CF Art. 37, Lei 10.257/01"}
- Recomendação Pericial Oficial: ${a.recomendacao_tecnica}`);
      }"""

if target1 in text:
    text = text.replace(target1, "")
    print("[1] target1 replaced successfully")
else:
    print("[1] WARNING: target1 not found")

# 2. Update section [6. MATRIZ DE AUDITORIA PERIMETRAL...] in deepContext
target2 = """[6. MATRIZ DE AUDITORIA PERIMETRAL & SPOT ZONING (PMD 2006 VS MINUTA 2026)]
Auditoria pericial algorítmica objetiva com base em 5 Indicadores (Polsby-Popper, APA Mananciais, Salto de CA, Conflito de Usos e Leapfrog):
- FID 1 (ZUE Chácaras Manancial - 4.918,98 ha - APA Manancial): Score SAP 65 (CRÍTICO) | Polsby-Popper 0.067 (perímetro altamente fractal com apêndices contornando matrículas privadas), macrogleba em manancial vulnerável a loteamentos sem rede Sabesp. Camada Exclusiva WebGIS: 'poligono_fid_01_zue_manancial' | Centróide: [-23.61552, -47.11432, 13].
- FID 21 (ZUE Interesse Turístico - 148,77 ha): Score SAP 45 (ATENÇÃO) | Spot Zoning severo (98,0% ex-Zona Rural com salto de CA de 6.12x sem estudo de impacto de vizinhança). Camada Exclusiva WebGIS: 'poligono_fid_21_zue_turistico' | Centróide: [-23.52441, -47.00160, 15].
- FID 30 (Carta VII Canguera / Zona Urbana Industrial - 66,36 ha): Score SAP 40 (MODERADO) | Conflito severo de vizinhança (87,0% ex-zona turística ZUE-DT convertida abruptamente para Industrial Pesada sem amortecimento). Camada Exclusiva WebGIS: 'poligono_fid_30_canguera' | Centróide: [-23.55261, -47.11239, 15].
- FID 15 (ZUE Interesse Turístico - 6.806 ha): Score SAP 65 (CRÍTICO) | Polsby-Popper 0.039 (menor compacidade do município), megazona convoluta avançando sobre topos de morro e cristas.
- FID 4 (ZUR Baixa Densidade - 119 ha): Score SAP 30 (MODERADO) | 50.3% conversão de rural para urbano com salto de CA de 2.29x sem EIV.
- FID 16/17 (ZUE Desenvolvimento & Ocupação Estratégica - 1.234 ha): Score SAP 30 (MODERADO) | Macroglebas leapfrog descoladas da malha contínua urbana ao longo da Castello Branco.
- FID 27 (ZUE Interesse Turístico - 570 ha): Score SAP 35 (MODERADO) | Bacia da APA Itupararanga sem rede coletora.
Camadas exclusivas dedicadas no WebGIS: 'poligono_fid_21_zue_turistico', 'poligono_fid_30_canguera', 'poligono_fid_01_zue_manancial' e a camada agregada 'audit_anomalies_sao_roque'`);"""

replacement2 = """[6. DIRETRIZES DA REVISÃO DO PLANO DIRETOR 2026 (MINUTA LC 39 E LC 40)]
- Consolidação Urbana das 4 Sedes Distritais (Sede, Maylasky, São João Novo, Canguera).
- Proteção Integral dos Mananciais da APA Itupararanga na Bacia Sul (ZUE Manancial, lote mínimo 5.000m²).
- Fomento ao Enoturismo e Gastronomia Sustentável no Roteiro do Vinho (ZUE-DT / Carta VII).
- Polos Econômicos e Logísticos controlados ao longo dos eixos Rodovia Castello Branco e Raposo Tavares (Carta VIII).
- 22 Obras Estruturantes de Drenagem, Contenção de Encostas e Mobilidade (Carta XIII).`);"""

if target2 in text:
    text = text.replace(target2, replacement2)
    print("[2] target2 replaced successfully")
else:
    print("[2] WARNING: target2 not found")

# 3. Update synthesizeAnswer logic
target3 = """    const isDiagnostic = this.isDiagnosticQuery(qNorm);
    const isAudit = qNorm.includes("spot zoning") || qNorm.includes("perimetro") || qNorm.includes("perímetro") || qNorm.includes("casuismo") || qNorm.includes("casuísmo") || qNorm.includes("anomalia") || qNorm.includes("favorecimento") || qNorm.includes("polsby") || qNorm.includes("fid 21") || qNorm.includes("fid 30") || qNorm.includes("fid 1") || qNorm.includes("fid 01") || qNorm.includes("fid21") || qNorm.includes("fid30") || qNorm.includes("fid1") || qNorm.includes("fid01");

    let camadaSugerida = "carta_01_macrozoneamento_2026";
    let defaultCentro = pinCtx ? [pinCtx.lat, pinCtx.lng, 16] : [-23.5350, -47.1350, 13];

    if (qNorm.includes("fid 21") || qNorm.includes("fid21")) {
      camadaSugerida = "poligono_fid_21_zue_turistico";
      defaultCentro = [-23.52441, -47.00160, 15];
    } else if (qNorm.includes("fid 30") || qNorm.includes("fid30")) {
      camadaSugerida = "poligono_fid_30_canguera";
      defaultCentro = [-23.55261, -47.11239, 15];
    } else if (qNorm.includes("fid 1") || qNorm.includes("fid 01") || qNorm.includes("fid1") || qNorm.includes("fid01")) {
      camadaSugerida = "poligono_fid_01_zue_manancial";
      defaultCentro = [-23.61552, -47.11432, 13];
    } else if (isAudit || pinCtx?.anomaliaPerimetral) {
      camadaSugerida = "audit_anomalies_sao_roque";
    } else if (isDiagnostic) {
      camadaSugerida = "carta_13_obras_prioritarias_2026";
    } else if (pinCtx?.insideAPA) {
      camadaSugerida = "carta_02_zue_2026";
    }

    // 1. TENTATIVA COM O MODELO GEMINI 4 ARGON
    if (this.useGemini && this.apiKey) {
      try {
        const deepContext = this.buildDeepContext(qRaw, pinCtx, kb);
        const argonResponse = await this.callGeminiArgon(qRaw, deepContext);
        if (argonResponse && argonResponse.length > 100) {
          return {
            query: qRaw,
            titulo: isAudit 
              ? "Auditoria Perimetral e Detecção de Spot Zoning (PMD 2006 vs 2026)"
              : (isDiagnostic 
                  ? "Diagnóstico Territorial, Físico e Normativo de São Roque" 
                  : (pinCtx ? `Análise do Ponto Marcado (${pinCtx.distrito} · ${pinCtx.zonaNome})` : `Parecer Territorial: "${qRaw}"`)),
            categoria: "Inteligência Geoespacial & Jurídica (Gemini 4 Argon)",
            isArgon: true,
            markdownText: argonResponse,
            pinContext: pinCtx,
            camadaSugerida: camadaSugerida,
            centroMapa: defaultCentro,
            origem: "Modelo Google Gemini 4 Argon · RAG Territorial Exaustivo"
          };
        }
      } catch (err) {
        console.warn("[AISearchEngine] Gemini 4 Argon falhou, acionando fallback local exaustivo:", err);
      }
    }

    // 2. FALLBACK LOCAL EXAUSTIVO MULTI-EIXO (CASO ESTEJA OFFLINE OU SEM API)
    return this.synthesizeExhaustiveLocalFallback(qRaw, qNorm, pinCtx, kb, isDiagnostic);
  }

  synthesizeExhaustiveLocalFallback(qRaw, qNorm, pinCtx, kb, isDiagnostic) {
    const cartas = kb.cartas_pd2026 || [];
    const obras = kb.obras_prioritarias_srq || [];
    const pedidos = kb.pedidos_participacao_popular || [];
    const zonas = kb.zonas_parametros || {};

    // 2.1 Caso específico: Polígono FID 21 (Carta II - ZUE Interesse Turístico)
    if (qNorm.includes("fid 21") || qNorm.includes("fid21")) {
      return {
        query: qRaw,
        titulo: "Laudo Pericial: Polígono FID 21 (Carta II) — ZUE Interesse Turístico",
        categoria: "Auditoria Perimetral Exclusiva (Camada FID 21)",
        pinContext: pinCtx,
        resumo: `<strong>DIAGNÓSTICO PERICIAL DO POLÍGONO FID 21 (CARTA II):</strong><br><br>
        O polígono <strong>FID 21</strong>, delimitado na <em>Carta II (ZUE)</em> da Minuta do Plano Diretor 2026 com <strong>148,77 hectares (1.487.683 m²)</strong>, apresenta grave incongruência urbanística e fortes indícios de <strong>Spot Zoning</strong>:<br><br>
        • <strong>Conversão Rural Maciça (98,0%):</strong> Praticamente toda a gleba era classificada como Zona Rural (ZRU) na Lei Complementar 40/2006, sem contiguidade imediata com mancha urbana consolidada.<br>
        • <strong>Salto de Potencial Construtivo (CA 6.12x):</strong> O Coeficiente de Aproveitamento salta de 0,2 (teto rural/ambiental) para 1,2 (proposto na ZUE), multiplicando o potencial edificatório sem contrapartida de infraestrutura sanitária ou viária.<br>
        • <strong>Compacidade Polsby-Popper = 0.371:</strong> Apresenta geometria alongada e descolada do tecido urbano principal (urbanização em salto / <em>leapfrog</em>).<br>
        • <strong>Vedações Normativas e Precedentes:</strong> Afronta o Art. 2º da Lei Federal 10.257/2001 (Estatuto da Cidade) e o Precedente Vinculante <strong>ADI TJ-SP nº 2048131</strong>, que veda expressamente a alteração casuística de zoneamento para beneficiar glebas específicas desprovidas de Estudo de Impacto de Vizinhança (EIV).<br><br>
        📋 <em>Recomendação: Submeter a gleba a EIV/RIV rigoroso e condicionar a conversão à cobrança de Outorga Onerosa de Alteração de Uso (OOAU).</em>`,
        zona: zonas["ZUE"] || null,
        zonaKey: "ZUE",
        cartasRelacionadas: ["Carta II: ZUE", "Carta I: Macrozoneamento"],
        pedidosParticipacao: pedidos.slice(0, 2),
        leis: ["Lei Federal 10.257/2001 (Estatuto da Cidade)", "Lei Federal 6.766/1979", "LC 40/2006", "Minuta 2026"],
        artigos: ["Art. 2º e Art. 42-B da Lei 10.257/01", "CF/88 Art. 37", "ADI TJ-SP 2048131"],
        cruzamentos: [],
        camadaSugerida: "poligono_fid_21_zue_turistico",
        centroMapa: [-23.52441, -47.00160, 15],
        origem: "Laudo Pericial Oficial (Polígono Exclusivo FID 21)"
      };
    }

    // 2.2 Caso específico: Polígono FID 30 (Carta VII - Canguera / Zona Urbana Industrial)
    if (qNorm.includes("fid 30") || qNorm.includes("fid30")) {
      return {
        query: qRaw,
        titulo: "Laudo Pericial: Polígono FID 30 (Carta VII) — Zoneamento de Canguera",
        categoria: "Auditoria Perimetral Exclusiva (Camada FID 30)",
        pinContext: pinCtx,
        resumo: `<strong>DIAGNÓSTICO PERICIAL DO POLÍGONO FID 30 (CARTA VII):</strong><br><br>
        O polígono <strong>FID 30</strong>, delimitado na <em>Carta VII (Consolidação Urbana de Canguera)</em> com <strong>66,36 hectares (663.633 m²)</strong>, configura situação de severo conflito de vizinhança e risco ambiental:<br><br>
        • <strong>Transição Abrupta de Uso (87,0% ex-ZUE-DT):</strong> A gleba era predominantemente Zona Urbana Especial de Desenvolvimento Turístico (ZUE-DT) pela LC 40/2006 e foi convertida sumariamente em Zona Urbana Industrial (ZUI).<br>
        • <strong>Conflito Severo de Vizinhança:</strong> A área faz divisa direta com chácaras residenciais e corredores de enoturismo do Roteiro do Vinho, sem previsão de faixa de amortecimento (<em>buffer zone</em>) de no mínimo 100 metros.<br>
        • <strong>Salto de CA (2.73x):</strong> O Coeficiente de Aproveitamento básico passa de 0,55 para 1,50 com Taxa de Ocupação de 60%, atraindo tráfego pesado de carretas para vias rurais sem pavimentação compatível.<br>
        • <strong>Vedações Normativas:</strong> Afronta o Art. 2º, VI da Lei Federal 10.257/2001 (ordenação e controle do uso do solo para evitar proximidade de usos incompatíveis).<br><br>
        📋 <em>Recomendação: Delimitar buffer verde de proteção de 100m e restringir usos industriais para Grau de Incomodidade I (não poluente e sem efluentes químicos).</em>`,
        zona: zonas["ZUI"] || zonas["ZPI"] || null,
        zonaKey: "ZUI",
        cartasRelacionadas: ["Carta VII: Canguera", "Carta VIII: Corredores", "Carta XIII: Obras"],
        pedidosParticipacao: pedidos.filter(p => p.bairro_localidade?.includes("Canguera")),
        leis: ["Lei Federal 10.257/2001", "Lei Estadual 9.866/1997", "LC 40/2006", "Minuta 2026"],
        artigos: ["Art. 2º, VI da Lei 10.257/01", "Normas CETESB P4.261"],
        cruzamentos: [],
        camadaSugerida: "poligono_fid_30_canguera",
        centroMapa: [-23.55261, -47.11239, 15],
        origem: "Laudo Pericial Oficial (Polígono Exclusivo FID 30)"
      };
    }

    // 2.3 Caso específico: Polígono FID 1 (Carta II - ZUE Chácaras Manancial)
    if (qNorm.includes("fid 1") || qNorm.includes("fid 01") || qNorm.includes("fid1") || qNorm.includes("fid01")) {
      return {
        query: qRaw,
        titulo: "Laudo Pericial: Polígono FID 1 (Carta II) — ZUE Chácaras Manancial",
        categoria: "Auditoria Perimetral Exclusiva (Camada FID 1)",
        pinContext: pinCtx,
        resumo: `<strong>DIAGNÓSTICO PERICIAL DO MACROPERÍMETRO FID 1 (CARTA II):</strong><br><br>
        O macroperímetro <strong>FID 1</strong>, delimitado na <em>Carta II (ZUE)</em> com <strong>4.918,98 hectares (49,19 km²)</strong>, representa o maior e mais crítico perímetro periurbano de São Roque:<br><br>
        • <strong>Perímetro Altamente Fractal (Polsby-Popper = 0.067):</strong> O índice de compacidade de apenas 0,067 reflete uma borda extremamente convoluta, com "dedos" e apêndices que avançam sobre glebas pontuais, sugerindo recortes direcionados a propriedades específicas.<br>
        • <strong>Localização em Manancial Crítico (APA Itupararanga):</strong> A totalidade do polígono drena diretamente para a bacia da Represa de Itupararanga, reservatório responsável pelo abastecimento de mais de 1 milhão de pessoas na RMS.<br>
        • <strong>Score SAP 65/100 (Risco Pericial Crítico):</strong> A gleba carece de rede coletora e tratamento de esgoto da Sabesp em mais de 80% de sua extensão, tornando inadmissível o parcelamento em alta densidade sob pena de contaminação por coliformes e fósforo.<br>
        • <strong>Vedações Normativas Expressas:</strong> Leis Estaduais nº 10.100/98 e 9.866/97 e Art. 3º da Lei Federal 6.766/79.<br><br>
        📋 <em>Recomendação: Manutenção irredutível do lote mínimo de 5.000 m², Taxa de Permeabilidade mínima de 55% e exigência obrigatória de fossa séptica biodigestora certificada para qualquer desdobro.</em>`,
        zona: zonas["ZUE"] || null,
        zonaKey: "ZUE",
        cartasRelacionadas: ["Carta II: ZUE", "Carta I: Macrozoneamento", "Carta VII: Canguera"],
        pedidosParticipacao: pedidos.filter(p => p.tema?.includes("Manancial") || p.bairro_localidade?.includes("Canguera")),
        leis: ["Lei Estadual 10.100/1998", "Lei Estadual 9.866/1997", "Lei Federal 6.766/1979", "LC 40/2006"],
        artigos: ["Art. 3º Lei 6.766/79", "Decreto Estadual 53.526/2008", "Quadro VIII Minuta 2026"],
        cruzamentos: [],
        camadaSugerida: "poligono_fid_01_zue_manancial",
        centroMapa: [-23.61552, -47.11432, 13],
        origem: "Laudo Pericial Oficial (Polígono Exclusivo FID 1)"
      };
    }"""

replacement3 = """    const isDiagnostic = this.isDiagnosticQuery(qNorm);

    let camadaSugerida = "carta_01_macrozoneamento_2026";
    let defaultCentro = pinCtx ? [pinCtx.lat, pinCtx.lng, 16] : [-23.5350, -47.1350, 13];

    if (qNorm.includes("canguera") || qNorm.includes("vinho")) {
      camadaSugerida = "carta_07_canguera_2026";
      defaultCentro = [-23.5850, -47.1200, 14];
    } else if (qNorm.includes("maylasky") || qNorm.includes("mailasqui")) {
      camadaSugerida = "carta_05_maylasky_2026";
      defaultCentro = [-23.5450, -47.0700, 14];
    } else if (qNorm.includes("sao joao novo") || qNorm.includes("são joão novo")) {
      camadaSugerida = "carta_06_sao_joao_novo_2026";
      defaultCentro = [-23.5800, -47.0100, 14];
    } else if (qNorm.includes("sede") || qNorm.includes("centro")) {
      camadaSugerida = "carta_04_sede_2026";
      defaultCentro = [-23.5350, -47.1350, 15];
    } else if (qNorm.includes("obra") || qNorm.includes("piscinao") || qNorm.includes("aracai") || isDiagnostic) {
      camadaSugerida = "carta_13_obras_prioritarias_2026";
      defaultCentro = [-23.5350, -47.1350, 14];
    } else if (pinCtx?.insideAPA || qNorm.includes("apa") || qNorm.includes("manancial") || qNorm.includes("itupararanga")) {
      camadaSugerida = "carta_02_zue_2026";
      defaultCentro = [-23.5850, -47.1200, 13];
    } else if (qNorm.includes("corredor") || qNorm.includes("raposo") || qNorm.includes("castello")) {
      camadaSugerida = "carta_08_corredores_2026";
      defaultCentro = [-23.5350, -47.1141, 13];
    } else if (qNorm.includes("aeis") || qNorm.includes("interesse social") || qNorm.includes("zeis")) {
      camadaSugerida = "carta_09_aeis_2026";
      defaultCentro = [-23.5350, -47.1141, 13];
    }

    // 1. TENTATIVA COM O MODELO GEMINI 4 ARGON
    if (this.useGemini && this.apiKey) {
      try {
        const deepContext = this.buildDeepContext(qRaw, pinCtx, kb);
        const argonResponse = await this.callGeminiArgon(qRaw, deepContext);
        if (argonResponse && argonResponse.length > 100) {
          return {
            query: qRaw,
            titulo: isDiagnostic 
              ? "Diagnóstico Territorial, Físico e Normativo de São Roque" 
              : (pinCtx ? `Análise do Ponto Marcado (${pinCtx.distrito} · ${pinCtx.zonaNome})` : `Parecer Territorial: "${qRaw}"`),
            categoria: "Inteligência Geoespacial & Jurídica (Gemini 4 Argon)",
            isArgon: true,
            markdownText: argonResponse,
            pinContext: pinCtx,
            camadaSugerida: camadaSugerida,
            centroMapa: defaultCentro,
            origem: "Modelo Google Gemini 4 Argon · RAG Territorial Exaustivo"
          };
        }
      } catch (err) {
        console.warn("[AISearchEngine] Gemini 4 Argon falhou, acionando fallback local exaustivo:", err);
      }
    }

    // 2. FALLBACK LOCAL EXAUSTIVO MULTI-EIXO (CASO ESTEJA OFFLINE OU SEM API)
    return this.synthesizeExhaustiveLocalFallback(qRaw, qNorm, pinCtx, kb, isDiagnostic);
  }

  synthesizeExhaustiveLocalFallback(qRaw, qNorm, pinCtx, kb, isDiagnostic) {
    const cartas = kb.cartas_pd2026 || [];
    const obras = kb.obras_prioritarias_srq || [];
    const pedidos = kb.pedidos_participacao_popular || [];
    const zonas = kb.zonas_parametros || {};"""

if target3 in text:
    text = text.replace(target3, replacement3)
    print("[3] target3 replaced successfully")
else:
    print("[3] WARNING: target3 not found")

# 4. Remove anomaliaPerimetral card from pinCardHtml in renderAnswer
target4 = """            ${p.anomaliaPerimetral ? `
            <div class="ai-pin-context-item" style="grid-column: 1 / -1; background: #fef2f2; border: 1px solid #fecaca; padding: 8px 12px; border-radius: 6px; margin-top: 4px;">
              <div style="color: #991b1b; font-weight: 700; font-size: 0.8rem; margin-bottom: 2px;">
                ⚠️ ALERTA PERICIAL: Anomalia Perimetral & Spot Zoning (${p.anomaliaPerimetral.nivel_risco})
              </div>
              <div style="color: #b91c1c; font-size: 0.76rem; line-height: 1.4;">
                <strong>Score SAP: ${p.anomaliaPerimetral.sap_score}/100</strong> · Polsby-Popper: ${p.anomaliaPerimetral.polsby_popper} · Salto de CA: ${p.anomaliaPerimetral.salto_ca_ratio}x · ${p.anomaliaPerimetral.principais_motivos?.[0] || ""}
              </div>
            </div>` : ""}"""

if target4 in text:
    text = text.replace(target4, "")
    print("[4] target4 replaced successfully")
else:
    print("[4] WARNING: target4 not found")

with open(path, "w", encoding="utf-8") as f:
    f.write(text)

print("=== ATUALIZAÇÃO DO AI-SEARCH.JS CONCLUÍDA COM SUCESSO ===")
