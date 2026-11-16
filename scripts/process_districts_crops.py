from PIL import Image
import numpy as np
import os

scale = 150 / 72  # 2.0833333333333335 px / pt

# Viewport bounds in PDF points for Cartas 5, 6, 7:
vx0, vx1 = 134.0, 1820.4
vy0, vy1 = 73.9, 1609.3

# In pixel coordinates (image height = 3509 px, corresponding to 1684 pt):
x0 = int(round(vx0 * scale))
x1 = int(round(vx1 * scale))
y0 = int(round((1684.0 - vy1) * scale))
y1 = int(round((1684.0 - vy0) * scale))

print(f"Crop window: x=[{x0}, {x1}], y=[{y0}, {y1}] (width={x1-x0} px, height={y1-y0} px)")

sheets = [
    (5, "maylasky", "carta_05_maylasky_mapa.png"),
    (6, "sao_joao_novo", "carta_06_sao_joao_novo_mapa.png"),
    (7, "canguera", "carta_07_canguera_mapa.png")
]

for num, code, dst_name in sheets:
    src_path = f"C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/minuta_pd2026/desmembrado/02_cartas_tecnicas/renders_png/carta_0{num}_zoneamento_consolidacao_urbana_{code}.png"
    dst_path = f"C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/data/{dst_name}"
    
    img = Image.open(src_path).convert("RGBA")
    cropped = img.crop((x0, y0, x1, y1))
    
    data = np.array(cropped)
    r, g, b, a = data[:, :, 0], data[:, :, 1], data[:, :, 2], data[:, :, 3]
    
    # White background threshold (r > 238, g > 238, b > 238)
    white_mask = (r > 238) & (g > 238) & (b > 238)
    data[white_mask, 3] = 0
    
    # Edge smoothing
    near_white = (r > 230) & (g > 230) & (b > 230) & (~white_mask)
    data[near_white, 3] = 100
    
    out_img = Image.fromarray(data, mode="RGBA")
    out_img.save(dst_path, optimize=True)
    
    size_mb = os.path.getsize(dst_path) / (1024 * 1024)
    print(f"Processado Carta {num} -> {dst_path}: {out_img.width}x{out_img.height} px, {size_mb:.2f} MB (Transparência: {np.sum(white_mask)} pixels transparentes)")
