from PIL import Image
import numpy as np
import os

scale = 150 / 72  # 2.0833333333333335 px / pt

# Viewport origin for Cartas 5, 6, 7, 11, 12:
# Crop was: x in [134.0, 1820.4], y in [73.9, 1609.3]
# In cropped image coordinates:
# x_pixel = (x_pt - 134.0) * scale
# y_pixel = (1609.3 - y_pt) * scale

boxes_pt = {
    5: (1660, 1815, 1425, 1590),
    6: (1660, 1815, 1425, 1590),
    7: (135, 280, 1425, 1590),
    11: (1610, 1765, 1425, 1590),
    12: (135, 280, 1425, 1590)
}

targets = [
    (5, "carta_05_maylasky_mapa.png"),
    (6, "carta_06_sao_joao_novo_mapa.png"),
    (7, "carta_07_canguera_mapa.png"),
    (11, "carta_11_viario_maylasky_mapa.png"),
    (12, "carta_12_viario_canguera_mapa.png")
]

base_dir = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\data"

print("=== REMOVENDO ROSA DOS VENTOS DAS CARTAS V, VI, VII, XI e XII ===")
for num, fname in targets:
    fpath = os.path.join(base_dir, fname)
    img = Image.open(fpath).convert("RGBA")
    data = np.array(img)
    
    bx0, bx1, by0, by1 = boxes_pt[num]
    
    # Calculate pixel bounds in cropped image
    px0 = max(0, int(round((bx0 - 134.0) * scale)))
    px1 = min(img.width, int(round((bx1 - 134.0) * scale)))
    py0 = max(0, int(round((1609.3 - by1) * scale)))
    py1 = min(img.height, int(round((1609.3 - by0) * scale)))
    
    # Count non-transparent pixels in this region before erasing
    before_erased = np.sum(data[py0:py1, px0:px1, 3] > 0)
    
    # Erase: set alpha channel to 0
    data[py0:py1, px0:px1, 3] = 0
    
    out = Image.fromarray(data, mode="RGBA")
    out.save(fpath, optimize=True)
    
    print(f"Carta {num:02d} ({fname}): Removida Rosa dos Ventos na janela px=[{px0}:{px1}, {py0}:{py1}] ({before_erased} pixels apagados).")

print("=== SUCESSO: TODAS AS 5 CARTAS ATUALIZADAS SEM ROSA DOS VENTOS ===")
