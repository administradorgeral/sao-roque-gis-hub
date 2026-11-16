with open("scripts/spatial_legal_engine.py", "r", encoding="utf-8") as f:
    text = f.read()

# Replace layer_files dict
old_layer_files = '''        layer_files = {
            "territorio_municipal": "territorio_municipal_sao_roque_web.geojson",
            "zoneamento_pmd2006": "zoneamento_sao_roque_web.geojson",
            "zoneamento_minuta_pmd2006": "zoneamento_minuta_sao_roque_web.geojson",
            "declividade": "declividade_sao_roque_web.geojson",
            "mdt": "mdt_sao_roque_web.geojson",
            "hidrografia": "hidrografia_sao_roque_web.geojson",
            "geomorfologico": "geomorfologico_sao_roque_web.geojson",
            "geologia": "geologia_sao_roque_web.geojson",
            "fragilidade_potencial": "fragilidade_potencial_sao_roque_web.geojson",
            "pedologico": "pedologico_sao_roque_web.geojson",
            "zoneamento_ambiental_pda2019": "zoneamento_ambiental_pda2019_sao_roque_web.geojson",
            "apa_itupararanga": "apa_itupararanga_limite_sao_roque_web.geojson",
            "zona_protecao_aeroportuaria_catarina": "zona_protecao_aeroportuaria_catarina_web.geojson",
            "ahs": "ahs_sao_roque_web.geojson",
            "vegetacao_arborea": "vegetacao_arborea_sao_roque_web.geojson"
        }'''

new_layer_files = '''        layer_files = {
            "territorio_municipal": "territorio_municipal_sao_roque_web.geojson",
            "distritos": "distritos_sao_roque_web.geojson",
            "setores_censitarios": "setores_censitarios_sao_roque_web.geojson",
            "logradouros": "logradouros_sao_roque_web.geojson",
            "zoneamento_pmd2006": "zoneamento_sao_roque_web.geojson",
            "zoneamento_minuta_pmd2006": "zoneamento_minuta_sao_roque_web.geojson",
            "declividade": "declividade_sao_roque_web.geojson",
            "mdt": "mdt_sao_roque_web.geojson",
            "hidrografia": "hidrografia_sao_roque_web.geojson",
            "geomorfologico": "geomorfologico_sao_roque_web.geojson",
            "geologia": "geologia_sao_roque_web.geojson",
            "fragilidade_potencial": "fragilidade_potencial_sao_roque_web.geojson",
            "pedologico": "pedologico_sao_roque_web.geojson",
            "zoneamento_ambiental_pda2019": "zoneamento_ambiental_pda2019_sao_roque_web.geojson",
            "apa_itupararanga": "apa_itupararanga_limite_sao_roque_web.geojson",
            "zona_protecao_aeroportuaria_catarina": "zona_protecao_aeroportuaria_catarina_web.geojson",
            "ahs": "ahs_sao_roque_web.geojson",
            "vegetacao_arborea": "vegetacao_arborea_sao_roque_web.geojson",
            "rbcv_cinturao_verde": "rbcv_cinturao_verde_nucleos_web.geojson"
        }'''

old_query_spatial = '''    def query_spatial_point(self, lat: float, lon: float) -> List[Dict[str, Any]]:
        """Intersecciona um ponto com todas as camadas territoriais."""
        pt = Point(lon, lat)
        intersections = []

        for layer_id, gdf in self.layers.items():
            try:
                # Consulta rápida via spatial index
                possible_matches_index = list(gdf.sindex.intersection((lon, lat, lon, lat)))
                if not possible_matches_index:
                    continue
                
                possible_matches = gdf.iloc[possible_matches_index]
                exact_matches = possible_matches[possible_matches.intersects(pt)]
                
                for _, row in exact_matches.iterrows():
                    props = {k: v for k, v in row.items() if k != "geometry"}
                    intersections.append({
                        "camada_id": layer_id,
                        "propriedades": props
                    })
            except Exception as e:
                print(f"[Erro Espacial] {layer_id}: {e}", file=sys.stderr)

        return intersections'''

new_query_spatial = '''    def query_spatial_point(self, lat: float, lon: float) -> List[Dict[str, Any]]:
        """Intersecciona um ponto com todas as camadas territoriais."""
        pt = Point(lon, lat)
        intersections = []

        for layer_id, gdf in self.layers.items():
            try:
                if layer_id == "logradouros":
                    # Proximidade de vias até 100m (~0.0009 graus)
                    buf = pt.buffer(0.0009)
                    possible_matches_index = list(gdf.sindex.intersection(buf.bounds))
                    if possible_matches_index:
                        possible_matches = gdf.iloc[possible_matches_index]
                        near = possible_matches[possible_matches.intersects(buf)]
                        if not near.empty:
                            dists = near.distance(pt)
                            nearest_idx = dists.idxmin()
                            row = near.loc[nearest_idx]
                            props = {k: v for k, v in row.items() if k != "geometry"}
                            intersections.append({
                                "camada_id": layer_id,
                                "propriedades": props
                            })
                    continue

                # Consulta rápida via spatial index para polígonos
                possible_matches_index = list(gdf.sindex.intersection((lon, lat, lon, lat)))
                if not possible_matches_index:
                    continue
                
                possible_matches = gdf.iloc[possible_matches_index]
                exact_matches = possible_matches[possible_matches.intersects(pt)]
                
                for _, row in exact_matches.iterrows():
                    props = {k: v for k, v in row.items() if k != "geometry"}
                    intersections.append({
                        "camada_id": layer_id,
                        "propriedades": props
                    })
            except Exception as e:
                print(f"[Erro Espacial] {layer_id}: {e}", file=sys.stderr)

        return intersections'''

norm_text = text.replace("\r\n", "\n")
norm_old_lf = old_layer_files.replace("\r\n", "\n")
norm_new_lf = new_layer_files.replace("\r\n", "\n")
norm_old_qs = old_query_spatial.replace("\r\n", "\n")
norm_new_qs = new_query_spatial.replace("\r\n", "\n")

if norm_old_lf in norm_text and norm_old_qs in norm_text:
    res = norm_text.replace(norm_old_lf, norm_new_lf).replace(norm_old_qs, norm_new_qs)
    with open("scripts/spatial_legal_engine.py", "w", encoding="utf-8") as f:
        f.write(res)
    print("SUCCESS: spatial_legal_engine.py updated with all 19 layers!")
else:
    print("ERROR: could not find target code in spatial_legal_engine.py")
