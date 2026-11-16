from PIL import Image
import numpy as np
import os

scale = 150 / 72  # 2.0833333333333335 px / pt

# 1. Macro sheets (8, 9, 13):
# Envelope: x in [329.58, 1512.58], y in [142.18, 1573.34]
# Image height = 3509 px (1684 pt)
macro_x0 = int(round(329.58 * scale))
macro_x1 = int(round(1512.58 * scale))
macro_y0 = int(round((1684 - 1573.34) * scale))
macro_y1 = int(round((1684 - 142.18) * scale))

# 2. Sede sheet (10):
# Envelope: x in [833.36, 1821.80], y in [244.92, 1609.54]
sede_x0 = int(round(833.36 * scale))
sede_x1 = int(round(1821.80 * scale))
sede_y0 = int(round((1684 - 1609.54) * scale))
sede_y1 = int(round((1684 - 244.92) * scale))

# 3. Maylasky & Canguera sheets (11, 12):
# Envelope: x in [134.0, 1820.4], y in [73.9, 1609.3]
dist_x0 = int(round(134.0 * scale))
dist_x1 = int(round(1820.4 * scale))
dist_y0 = int(round((1684.0 - 1609.3) * scale))
dist_y1 = int(round((1684.0 - 73.9) * scale))

jobs = [
    (8, "carta_08_corredores_comercio_servicos_turismo.png", "carta_08_corredores_mapa.png", (macro_x0, macro_y0, macro_x1, macro_y1)),
    (9, "carta_09_areas_especial_interesse_aeis_aeit_aeiu.png", "carta_09_aeis_mapa.png", (macro_x0, macro_y0, macro_x1, macro_y1)),
    (10, "carta_10_sistema_viario_drenagem_sede.png", "carta_10_viario_sede_mapa.png", (sede_x0, sede_y0, sede_x1, sede_y1)),
    (11, "carta_11_sistema_viario_drenagem_maylasky.png", "carta_11_viario_maylasky_mapa.png", (dist_x0, dist_y0, dist_x1, dist_y1)),
    (12, "carta_12_sistema_viario_drenagem_canguera.png", "carta_12_viario_canguera_mapa.png", (dist_x0, dist_y0, dist_x1, dist_y1)),
    (13, "carta_13_intervencoes_obras_prioritarias_srq01_srq22.png", "carta_13_obras_prioritarias_mapa.png", (macro_x0, macro_y0, macro_x1, macro_y1))
]

base_in = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\minuta_pd2026\desmembrado\02_cartas_tecnicas\renders_png"
base_out = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\data"

print("Iniciando processamento em lote das Cartas 08 a 13...")
for num, in_file, out_file, crop_box in jobs:
    src_path = os.path.join(base_in, in_file)
    dst_path = os.path.join(base_out, out_file)
    
    img = Image.open(src_path).convert("RGBA")
    cropped = img.crop(crop_box)
    
    data = np.array(cropped)
    r, g, b, a = data[:, :, 0], data[:, :, 1], data[:, :, 2], data[:, :, 3]
    
    white_mask = (r > 238) & (g > 238) & (b > 238)
    data[white_mask, 3] = 0
    
    near_white = (r > 230) & (g > 230) & (b > 230) & (~white_mask)
    data[near_white, 3] = 100
    
    out_img = Image.fromarray(data, mode="RGBA")
    out_img.save(dst_path, optimize=True)
    
    mb = os.path.getsize(dst_path) / (1024 * 1024)
    print(f"Carta {num:02d} -> {out_file}: {out_img.width}x{out_img.height} px, {mb:.2f} MB (Transparência: {np.sum(white_mask)} pixels)")
print("Processamento concluído com sucesso!")
