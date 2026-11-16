"""
create_exclusive_layers.py
Gera arquivos GeoJSON exclusivos para os polígonos destacados pelo usuário:
1. Polígono FID 21 (Carta II) ZUE - Interesse Turístico
2. Polígono FID 30 - Carta VII — Zoneamento de Canguera / Industrial
3. Polígono FID 1  (Carta II) ZUE - Chácaras Manancial
"""

import json
import os

def create_layers():
    minuta_path = "data/pmsr_zoneamento_minuta_pmd2006.geojson"
    audit_path = "data/audit_anomalies_sao_roque.geojson"

    with open(minuta_path, "r", encoding="utf-8") as f:
        minuta_data = json.load(f)

    with open(audit_path, "r", encoding="utf-8") as f:
        audit_data = json.load(f)

    audit_map = {f['properties']['fid']: f['properties'] for f in audit_data['features']}

    configs = [
        {
            "fid": 21,
            "filename": "data/poligono_fid_21_zue_turistico.geojson",
            "titulo": "Polígono FID 21: ZUE - Interesse Turístico (Carta II)",
            "carta": "Carta II: Macrozona de Urbanização Específica (Revisão 2026)",
            "cor": "#f59e0b",
            "cor_borda": "#d97706",
            "tipo_destaque": "Spot Zoning Severo (Salto de CA 6.12x)"
        },
        {
            "fid": 30,
            "filename": "data/poligono_fid_30_canguera.geojson",
            "titulo": "Polígono FID 30: Carta VII — Zoneamento de Canguera / Zona Urbana Industrial",
            "carta": "Carta VII: Consolidação Urbana - Canguera / Corredor Sul (Revisão 2026)",
            "cor": "#8b5cf6",
            "cor_borda": "#6d28d9",
            "tipo_destaque": "Conflito de Vizinhança Turística vs Industrial"
        },
        {
            "fid": 1,
            "filename": "data/poligono_fid_01_zue_manancial.geojson",
            "titulo": "Polígono FID 1: ZUE - Chácaras Manancial (Carta II)",
            "carta": "Carta II: Macrozona de Urbanização Específica (Revisão 2026)",
            "cor": "#0284c7",
            "cor_borda": "#0369a1",
            "tipo_destaque": "Mananciais da APA Itupararanga (Morfologia Convoluta PP=0.067)"
        }
    ]

    for cfg in configs:
        fid = cfg["fid"]
        minuta_feat = [f for f in minuta_data["features"] if f["properties"].get("fid") == fid][0]
        audit_prop = audit_map.get(fid, {})

        # Mesclar propriedades mantendo rigor pericial
        props = dict(minuta_feat["properties"])
        props["titulo_camada"] = cfg["titulo"]
        props["carta_origem"] = cfg["carta"]
        props["tipo_destaque"] = cfg["tipo_destaque"]
        props["cor_hex"] = cfg["cor"]
        props["cor_borda"] = cfg["cor_borda"]
        props["camada_exclusiva"] = True

        if audit_prop:
            props["sap_score"] = audit_prop.get("sap_score")
            props["nivel_risco"] = audit_prop.get("nivel_risco")
            props["polsby_popper"] = audit_prop.get("polsby_popper")
            props["salto_ca_ratio"] = audit_prop.get("salto_ca_ratio")
            props["ca_2006_estimado"] = audit_prop.get("ca_2006_estimado")
            props["ca_2026_proposto"] = audit_prop.get("ca_2026_proposto")
            props["transicao_rural_pct"] = audit_prop.get("transicao_rural_pct")
            props["dentro_apa"] = audit_prop.get("dentro_apa")
            props["principais_motivos"] = audit_prop.get("principais_motivos")
            props["artigos_violados"] = audit_prop.get("artigos_violados")
            props["recomendacao_tecnica"] = audit_prop.get("recomendacao_tecnica")
            props["centroide"] = audit_prop.get("centroide")

        feature_collection = {
            "type": "FeatureCollection",
            "metadata": {
                "titulo": cfg["titulo"],
                "fid": fid,
                "carta": cfg["carta"],
                "orgao": "São Roque GIS Hub · Camada Exclusiva de Detalhamento Pericial",
                "area_ha": props.get("area_ha")
            },
            "features": [
                {
                    "type": "Feature",
                    "geometry": minuta_feat["geometry"],
                    "properties": props
                }
            ]
        }

        with open(cfg["filename"], "w", encoding="utf-8") as out_f:
            json.dump(feature_collection, out_f, ensure_ascii=False, indent=2)

        print(f"Camada exclusiva gerada: {cfg['filename']} (FID {fid} - {props.get('nome')})")

if __name__ == "__main__":
    create_layers()
