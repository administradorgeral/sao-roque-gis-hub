from PIL import Image
import os

png_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\minuta_pd2026\desmembrado\02_cartas_tecnicas\renders_png\carta_02_zoneamentos_macrozona_urbanizacao_especifica.png"
img = Image.open(png_path)
w, h = img.size
print(f"Dimensões totais da prancha: {w} x {h}")

scale = 150 / 72  # 2.0833 px / pt

x0 = int(round(300 * scale))
x1 = int(round(1950 * scale))
y0 = int(round((1684 - 1620) * scale))
y1 = int(round((1684 - 120) * scale))

map_crop = img.crop((x0, y0, x1, y1))
out_crop = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\data\carta_02_zue_mapa.png"
map_crop.save(out_crop, optimize=True)
size_mb = os.path.getsize(out_crop) / (1024 * 1024)
print(f"Salvo mapa recortado: {out_crop} ({map_crop.width} x {map_crop.height} px, {size_mb:.2f} MB)")
