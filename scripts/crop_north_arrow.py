from PIL import Image

img = Image.open(r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\minuta_pd2026\desmembrado\02_cartas_tecnicas\renders_png\carta_01_macrozoneamento_municipal.png")
w, h = img.size
scale = 150 / 72

# In points: x in [1600, 1800], y in [1450, 1650]
# In image:
x0 = int(round(1550 * scale))
x1 = int(round(1800 * scale))
y0 = int(round((1684 - 1650) * scale))
y1 = int(round((1684 - 1450) * scale))

crop = img.crop((x0, y0, x1, y1))
crop_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\minuta_pd2026\desmembrado\02_cartas_tecnicas\renders_png\debug_north_arrow.png"
crop.save(crop_path)
print("Saved debug_north_arrow.png:", crop.size)
