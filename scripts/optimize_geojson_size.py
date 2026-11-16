import json
import os
import time

def optimize_geojson():
    path = os.path.join(os.path.dirname(__file__), '..', 'data', 'declividade_sao_roque.geojson')
    path = os.path.abspath(path)
    
    orig_size = os.path.getsize(path) / (1024 * 1024)
    print(f"Original size: {orig_size:.2f} MB")
    
    t0 = time.time()
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    features = data.get('features', [])
    print(f"Loaded in {time.time() - t0:.2f}s. Features count: {len(features)}")
    
    def round_coords(geom_coords):
        if isinstance(geom_coords, (int, float)):
            return round(geom_coords, 6)
        return [round_coords(c) for c in geom_coords]
    
    for feat in features:
        geom = feat.get('geometry')
        if geom and 'coordinates' in geom:
            geom['coordinates'] = round_coords(geom['coordinates'])
            
    temp_path = path + '.tmp'
    t1 = time.time()
    with open(temp_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, separators=(',', ':'))
        
    new_size = os.path.getsize(temp_path) / (1024 * 1024)
    print(f"Serialized in {time.time() - t1:.2f}s.")
    print(f"Optimized size: {new_size:.2f} MB ({100 - (new_size / orig_size * 100):.1f}% reduction)")
    
    # Validation: reload to guarantee JSON is valid
    with open(temp_path, 'r', encoding='utf-8') as f:
        val_data = json.load(f)
        assert len(val_data.get('features', [])) == len(features), "Feature count mismatch!"
        assert 'codigo_classe' in val_data['features'][0]['properties'], "Missing property!"
        
    print("Validation passed: exact feature count and attributes preserved.")
    os.replace(temp_path, path)
    print("Successfully replaced data/declividade_sao_roque.geojson!")

if __name__ == '__main__':
    optimize_geojson()
