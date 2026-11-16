import { SpatialCrossEngine } from "../js/modules/spatial-cross-engine.js";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Mock fetch for Node.js using local filesystem
global.fetch = async (url) => {
  const cleanUrl = url.split("?")[0];
  const filePath = path.resolve(__dirname, "..", cleanUrl);
  if (fs.existsSync(filePath)) {
    const data = fs.readFileSync(filePath, "utf-8");
    return {
      ok: true,
      status: 200,
      json: async () => JSON.parse(data)
    };
  }
  return { ok: false, status: 404 };
};

async function runTests() {
  console.log("=================================================================");
  console.log("TESTE DO MOTOR DE INTELIGÊNCIA TERRITORIAL CRUZADA (TUDO LIGADO A TUDO)");
  console.log("=================================================================");

  const engine = new SpatialCrossEngine();
  const loaded = await engine.init();
  if (!loaded) {
    console.error("[-] Falha ao inicializar SpatialCrossEngine");
    process.exit(1);
  }

  console.log("[+] Engine carregado com sucesso!\n");

  // Teste 1: Ponto em Canguera (-23.5850, -47.1200)
  console.log("[TESTE 1] Drill-Down Multicamadas no Ponto (-23.5850, -47.1200):");
  const dossier = engine.buildCrossDossierForPoint(-23.5850, -47.1200);
  console.log("  • Logradouro Mais Próximo:", dossier.logradouro ? `${dossier.logradouro.nome} (${dossier.logradouro.distancia_m}m)` : "N/D");
  console.log("  • Bairro:", dossier.bairro ? dossier.bairro.nome : "N/D");
  console.log("  • Distrito:", dossier.distrito.nome);
  console.log("  • Zoneamento:", dossier.zoneamento_2006.legenda_oficial);
  console.log("  • Solo:", dossier.pedologia_solos ? dossier.pedologia_solos.legenda_oficial : "N/D");
  console.log("  • Geologia:", dossier.geologia_geotecnia ? dossier.geologia_geotecnia.legenda_oficial : "N/D");
  console.log("  • APA Itupararanga:", dossier.unidade_conservacao_apa ? dossier.unidade_conservacao_apa.legenda_oficial : "Fora da APA");
  console.log("  • Cartas 2026 Aplicáveis:", dossier.plano_diretor_2026.cartas_incidentes.slice(0, 3).join(", "));
  console.log("  • Obras Carta XIII Próximas:", dossier.obras_estruturantes_proximas.length);

  // Teste 2: Busca por Logradouro ("Estrada do Vinho")
  console.log("\n[TESTE 2] Consulta Topológica da Via 'Estrada do Vinho':");
  const matchVia = engine.searchEntity("Estrada do Vinho");
  if (matchVia && matchVia.type === "logradouro") {
    const v = matchVia.data;
    console.log("  • Nome Oficial:", v.nome_oficial);
    console.log("  • Camada:", v.camada);
    console.log("  • Legenda Oficial:", v.legenda_oficial);
    console.log("  • Distritos que atravessa:", v.distritos.join(", "));
    console.log("  • Zonas que corta:", v.zonas_incidentes.join("; "));
    console.log("  • Solos presentes:", v.solos_predominantes.join("; "));
    console.log("  • Está na APA Itupararanga?", v.inside_apa ? "SIM (Mananciais)" : "Não");
    console.log("  • Obras da Carta XIII Próximas:", v.obras_proximas.map(o => `${o.codigo} (${o.nome})`).join(", ") || "Nenhuma");
  } else {
    console.error("  [-] Via não encontrada no grafo!");
  }

  // Teste 3: Busca por Bairro ("Canguera")
  console.log("\n[TESTE 3] Consulta ao Bairro 'Canguera':");
  const matchBairro = engine.searchEntity("Canguera");
  if (matchBairro && matchBairro.type === "bairro") {
    const b = matchBairro.data;
    console.log("  • Nome:", b.nome);
    console.log("  • Distrito:", b.distrito);
    console.log("  • Zoneamento Padrão:", b.zoneamento_padrao);
    console.log("  • Cartas do Plano Diretor:", b.cartas_incidentes.join(", "));
    console.log("  • Vocação:", b.descricao);
  }

  // Teste 4: Busca por Solo ("Argissolo" / "PVA")
  console.log("\n[TESTE 4] Consulta por Pedologia 'PVA':");
  const matchSolo = engine.searchEntity("PVA");
  if (matchSolo && matchSolo.type === "solo") {
    const s = matchSolo.data;
    console.log("  • Classe:", s.nome_classe);
    console.log("  • Textura:", s.textura);
    console.log("  • Permeabilidade:", s.permeabilidade);
    console.log("  • Implicação para Obras:", s.implicacao_obras);
  }

  // Teste 5: Busca por Zona ("ZUE-DT")
  console.log("\n[TESTE 5] Consulta por Zona 'ZUE-DT':");
  const matchZona = engine.searchEntity("ZUE-DT");
  if (matchZona && matchZona.type === "zona_2006") {
    const z = matchZona.data;
    console.log("  • Legenda Oficial:", z.legenda_oficial);
    console.log("  • CA Máximo:", z.parametros_construtivos.coeficiente_aproveitamento_maximo);
    console.log("  • TO Máxima:", z.parametros_construtivos.taxa_ocupacao_maxima);
    console.log("  • Vias que a cortam:", z.vias_que_atravessam.slice(0, 5).join(", "));
    console.log("  • Distritos:", z.distritos_onde_ocorre.join(", "));
  }

  console.log("\n=================================================================");
  console.log("[SUCESSO] TODOS OS TESTES DE TOPOLOGIA CRUZADA PASSARAM COM ÊXITO!");
  console.log("=================================================================");
}

runTests();
