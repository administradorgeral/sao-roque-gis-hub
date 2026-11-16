from PIL import Image
import numpy as np

img = Image.open(r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\minuta_pd2026\desmembrado\02_cartas_tecnicas\renders_png\carta_01_macrozoneamento_municipal.png")
w, h = img.size
print(f"Dimensões do PNG: {w} x {h}")

# The image is 4967 x 3509.
# Let's crop candidate legend locations:
# 1. Top left (x: 100 to 1200, y: 100 to 1200)
# 2. Bottom left (x: 100 to 1200, y: 2300 to 3400)
# 3. Top right (x: 3500 to 4800, y: 100 to 1200)
# 4. Middle right (x: 3500 to 4800, y: 1200 to 2400)

crops = {
    "top_left": (100, 100, 1500, 1200),
    "bottom_left": (100, 2300, 1500, 3400),
    "top_right": (3500, 100, 4850, 1200),
    "mid_right": (3500, 1200, 4850, 2400)
}

for name, box in crops.items():
    c = img.crop(box)
    # Check if there is high variance / text / table in the crop
    c_arr = np.array(c.convert('L'))
    # Non-white pixels (pixels < 245)
    non_white = np.mean(c_arr < 245)
    print(f"Crop {name}: {non_white*100:.1f}% non-white pixels")
    if non_white > 0.05:
        crop_path = fr"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\minuta_pd2026\desmembrado\02_cartas_tecnicas\renders_png\debug_{name}.png"
        c.save(crop_path)
        print(f"  Salvo para inspeção: debug_{name}.png")
