import pypdfium2 as pdfium
from PIL import Image

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\40537_4_3_3_1 Declividade.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]

objs = list(page.get_objects())
images = [obj for obj in objs if obj.type == 3]

print(f"Total de imagens: {len(images)}")
# Vamos extrair e salvar duas imagens para ver o que contêm
img_0 = images[0].get_image()
pil_img_0 = img_0.to_pil()
pil_img_0.save(r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\scripts\sample_img_0.png")

img_mid = images[len(images)//2].get_image()
pil_img_mid = img_mid.to_pil()
pil_img_mid.save(r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\scripts\sample_img_mid.png")

print(f"Imagem 0: size={pil_img_0.size}, mode={pil_img_0.mode}, colors={len(pil_img_0.getcolors(maxcolors=10000) or [])}")
print(f"Imagem Mid: size={pil_img_mid.size}, mode={pil_img_mid.mode}, colors={len(pil_img_mid.getcolors(maxcolors=10000) or [])}")

doc.close()
