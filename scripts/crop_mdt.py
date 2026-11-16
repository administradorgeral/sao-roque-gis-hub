from PIL import Image

img = Image.open(r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\scripts\rendered_mdt_page.png")
w, h = img.size

# O mapa está na metade esquerda
crop_box = (int(w * 0.15), int(h * 0.25), int(w * 0.55), int(h * 0.65))
cropped = img.crop(crop_box)
crop_out = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\scripts\crop_mdt_pdf.png"
cropped.save(crop_out)
print(f"Crop salvo em: {crop_out} ({cropped.size})")
