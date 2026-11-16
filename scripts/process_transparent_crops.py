from PIL import Image
import numpy as np
import os

scale = 150 / 72  # 2.0833333333333335 px / pt

# Exact bounding box of São Roque zones in PDF points:
# x in [329.58, 1512.58] pt
# y in [142.18, 1573.34] pt

# In image coordinates:
# x0 = 329.58 * scale
# x1 = 1512.58 * scale
# y0 = (1684 - 1573.34) * scale  (Top of image is high Y in PDF)
# y1 = (1684 - 142.18) * scale   (Bottom of image is low Y in PDF)

x0 = int(round(329.58 * scale))
x1 = int(round(1512.58 * scale))
y0 = int(round((1684 - 1573.34) * scale))
y1 = int(round((1684 - 142.18) * scale))

print(f"Crop window: x=[{x0}, {x1}], y=[{y0}, {y1}] (width={x1-x0} px, height={y1-y0} px)")

cartas = [
    ("carta_01_macrozoneamento_municipal.png", "carta_01_macrozoneamento_mapa.png"),
    ("carta_02_zoneamentos_macrozona_urbanizacao_especifica.png", "carta_02_zue_mapa.png"),
    ("carta_03_zoneamentos_macrozona_consolidacao_urbana.png", "carta_03_consolidacao_urbana_mapa.png")
]

src_dir = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\minuta_pd2026\desmembrado\02_cartas_tecnicas\renders_png"
dst_dir = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\data"

for src_name, dst_name in cartas:
    src_path = os.path.join(src_dir, src_name)
    dst_path = os.path.join(dst_dir, dst_name)
    
    img = Image.open(src_path).convert("RGBA")
    cropped = img.crop((x0, y0, x1, y1))
    
    # Process transparency: make white/off-white background transparent
    data = np.array(cropped)
    r, g, b, a = data[:, :, 0], data[:, :, 1], data[:, :, 2], data[:, :, 3]
    
    # Background white threshold (r > 240, g > 240, b > 240)
    white_mask = (r > 238) & (g > 238) & (b > 238)
    data[white_mask, 3] = 0
    
    # Also smooth slight edge fringing:
    near_white = (r > 230) & (g > 230) & (b > 230) & (~white_mask)
    data[near_white, 3] = 100
    
    out_img = Image.fromarray(data, mode="RGBA")
    out_img.save(dst_path, optimize=True)
    
    size_mb = os.path.getsize(dst_path) / (1024 * 1024)
    print(f"Processado {dst_name}: {out_img.width}x{out_img.height} px, {size_mb:.2f} MB (Transparência aplicada: {np.sum(white_mask)} pixels transparentes)")
