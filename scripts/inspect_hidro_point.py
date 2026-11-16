import pypdfium2 as pdfium
from PIL import Image

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\Hidro .pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]

# Ponto UTM: E=281178, N=7403132
# Calibração afim da Hidro:
# UTM_X = 17.636163 * PDF_X + 269256.56  =>  PDF_X = (UTM_X - 269256.56) / 17.636163
# UTM_Y = 17.638983 * PDF_Y + 7381376.20  =>  PDF_Y = (UTM_Y - 7381376.20) / 17.638983

px = (281178.0 - 269256.56) / 17.636163
py = (7403132.0 - 7381376.20) / 17.638983
print(f"Ponto no PDF: X={px:.2f} pt, Y={py:.2f} pt")

# Renderizar página a escala 2.0
scale = 2.0
pw = page.get_width()
ph = page.get_height()
pil_img = page.render(scale=scale).to_pil()

# No espaço de imagem PIL:
# X_img = px * scale
# Y_img = (ph - py) * scale
cx = int(px * scale)
cy = int((ph - py) * scale)

# Fazer crop de 800x800 pixels ao redor
crop_box = (cx - 400, cy - 400, cx + 400, cy + 400)
crop = pil_img.crop(crop_box)
crop_out = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\scripts\hidro_point_crop.png"
crop.save(crop_out)
print(f"Crop salvo em: {crop_out}")

# Salvar também nos artifacts para inspeção
artifact_out = r"C:\Users\admin\.gemini\antigravity\brain\8a767400-ab0f-40a5-b1b7-b7e6cab406ec\hidro_point_crop.png"
crop.save(artifact_out)
print(f"Crop salvo nos artifacts: {artifact_out}")

doc.close()
