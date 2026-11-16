import fs from 'fs';

const logradouros = JSON.parse(fs.readFileSync('data/logradouros_sao_roque_web.geojson', 'utf8'));
const setores = JSON.parse(fs.readFileSync('data/setores_censitarios_sao_roque_web.geojson', 'utf8'));
const zoneamento = JSON.parse(fs.readFileSync('data/pmsr_zoneamento_pmd2006.geojson', 'utf8'));
const distritos = JSON.parse(fs.readFileSync('data/distritos_sao_roque_web.geojson', 'utf8'));
const apa = JSON.parse(fs.readFileSync('data/apa_itupararanga_limite_sao_roque_web.geojson', 'utf8'));

console.log('=== CAMADAS CARREGADAS ===');
console.log('Logradouros features:', logradouros.features.length);
console.log('Setores Censitarios IBGE features:', setores.features.length);
console.log('Zoneamento PMD 2006 features:', zoneamento.features.length);
console.log('Distritos features:', distritos.features.length);
console.log('APA features:', apa.features.length);

const testPoints = [
  { name: 'Praça da Matriz (Centro Histórico)', lat: -23.5290, lng: -47.1354 },
  { name: 'Estrada do Vinho km 4 (Canguera)', lat: -23.5820, lng: -47.1450 },
  { name: 'Centro de Maylasky', lat: -23.5415, lng: -47.0545 },
  { name: 'Centro de São João Novo', lat: -23.5350, lng: -47.0050 }
];

function pointInPoly(pt, geom) {
  if (!geom || !geom.coordinates) return false;
  const x = pt[0], y = pt[1];
  const polys = geom.type === 'Polygon' ? [geom.coordinates] : (geom.type === 'MultiPolygon' ? geom.coordinates : []);
  for (const poly of polys) {
    const ring = poly[0];
    let inside = false;
    for (let i = 0, j = ring.length - 1; i < ring.length; j = i++) {
      const xi = ring[i][0], yi = ring[i][1];
      const xj = ring[j][0], yj = ring[j][1];
      const intersect = ((yi > y) !== (yj > y)) && (x < (xj - xi) * (y - yi) / (yj - yi) + xi);
      if (intersect) inside = !inside;
    }
    if (inside) return true;
  }
  return false;
}

function distToSegmentSquared(px, py, vx, vy, wx, wy) {
  const l2 = (vx - wx)**2 + (vy - wy)**2;
  if (l2 === 0) return (px - vx)**2 + (py - vy)**2;
  let t = ((px - vx) * (wx - vx) + (py - vy) * (wy - vy)) / l2;
  t = Math.max(0, Math.min(1, t));
  return (px - (vx + t * (wx - vx)))**2 + (py - (vy + t * (wy - vy)))**2;
}

function findNearestStreetGeo(lng, lat, features) {
  let closest = null;
  let minMeters = Infinity;
  const cosLat = Math.cos(lat * Math.PI / 180);

  for (const f of features) {
    if (!f.geometry) continue;
    const coords = f.geometry.type === 'LineString' ? [f.geometry.coordinates] : (f.geometry.type === 'MultiLineString' ? f.geometry.coordinates : []);
    for (const line of coords) {
      for (let i = 0; i < line.length - 1; i++) {
        const p1 = line[i];
        const p2 = line[i+1];
        
        // Approximate distance taking aspect ratio into account
        // dx in degrees * cosLat, dy in degrees
        const px = lng * cosLat;
        const py = lat;
        const v1x = p1[0] * cosLat;
        const v1y = p1[1];
        const v2x = p2[0] * cosLat;
        const v2y = p2[1];

        const d2 = distToSegmentSquared(px, py, v1x, v1y, v2x, v2y);
        const metersApprox = Math.sqrt(d2) * 111320;
        if (metersApprox < minMeters) {
          minMeters = metersApprox;
          closest = {
            nome: f.properties.nome || f.properties.name || 'Via sem nome',
            tipo: f.properties.tipo_via,
            distancia_m: Math.round(metersApprox),
            bairro: f.properties.bairro,
            ref: f.properties.ref
          };
        }
      }
    }
  }
  return closest;
}

for (const tp of testPoints) {
  const pt = [tp.lng, tp.lat];
  console.log('\n======================================================');
  console.log(`PONTO: ${tp.name} (${tp.lat}, ${tp.lng})`);
  console.log('======================================================');

  // 1. Setor Censitário IBGE
  let foundSetor = null;
  for (const s of setores.features) {
    if (pointInPoly(pt, s.geometry)) {
      foundSetor = s.properties;
      break;
    }
  }
  if (foundSetor) {
    console.log(`[IBGE 2022] Setor: ${foundSetor.cd_setor} | Distrito: ${foundSetor.distrito} | Situacao: ${foundSetor.situacao} | Area: ${foundSetor.area_ha} ha`);
  } else {
    console.log('[IBGE 2022] NÃO ENCONTRADO!');
  }

  // 2. Distrito Oficial
  let foundDist = null;
  for (const d of distritos.features) {
    if (pointInPoly(pt, d.geometry)) {
      foundDist = d.properties;
      break;
    }
  }
  console.log(`[DISTRITO OFICIAL] ${foundDist ? (foundDist.nome || foundDist.distrito) : 'N/A'}`);

  // 3. Zoneamento PMD 2006
  let foundZona = null;
  for (const z of zoneamento.features) {
    if (pointInPoly(pt, z.geometry)) {
      foundZona = z.properties;
      break;
    }
  }
  console.log(`[ZONEAMENTO LC 40/06] ${foundZona ? `${foundZona.sigla || foundZona.zona} - ${foundZona.denominacao || ''}` : 'Zona Rural / Macrozona de Conservacao'}`);

  // 4. APA Itupararanga
  let inApa = false;
  for (const a of apa.features) {
    if (pointInPoly(pt, a.geometry)) {
      inApa = true;
      break;
    }
  }
  console.log(`[APA ITUPARARANGA] ${inApa ? 'SIM (100% Dentro da APA)' : 'NÃO (Fora do Perímetro da APA)'}`);

  // 5. Rua Mais Próxima GEOMÉTRICA
  const streetGeo = findNearestStreetGeo(tp.lng, tp.lat, logradouros.features);
  if (streetGeo) {
    console.log(`[LOGRADOURO GEOMÉTRICO] ${streetGeo.nome} (${streetGeo.tipo || 'via'}) a apenas ${streetGeo.distancia_m} metros!`);
  } else {
    console.log('[LOGRADOURO GEOMÉTRICO] Nenhuma via encontrada');
  }
}
