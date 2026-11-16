from PIL import Image

scale = 150 / 72  # px / pt

# Let's crop the actual colored areas in Carta 5, 6, 7 to see what they look like
# Carta 5
img5 = Image.open(r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\minuta_pd2026\desmembrado\02_cartas_tecnicas\renders_png\carta_05_zoneamento_consolidacao_urbana_maylasky.png")
# Map content is in [134, 1820] pt, [74, 1609] pt
# Let's crop the whole map viewport of Carta 5, 6, 7:
for num, name in [(5, 'maylasky'), (6, 'sao_joao_novo'), (7, 'canguera')]:
    src = f"C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/minuta_pd2026/desmembrado/02_cartas_tecnicas/renders_png/carta_0{num}_zoneamento_consolidacao_urbana_{name}.png"
    img = Image.open(src)
    # The drawing frame is between x=134 pt and x=1820 pt, y=74 pt and y=1609 pt
    # In pixel coordinates:
    x0 = int(round(134.0 * scale))
    x1 = int(round(1820.4 * scale))
    y0 = int(round((1684.0 - 1609.3) * scale))
    y1 = int(round((1684.0 - 73.9) * scale))
    crop = img.crop((x0, y0, x1, y1))
    crop_thumb = crop.resize((crop.width // 3, crop.height // 3))
    crop_thumb.save(f"C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/scripts/viewport_carta_0{num}.png")
    print(f"Carta {num} ({name}): viewport px = ({x0}, {y0}, {x1}, {y1}) -> size {crop.size}")
