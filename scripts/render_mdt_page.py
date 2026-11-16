import pypdfium2 as pdfium
from PIL import Image

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\47531_4_2_3_2 MDT.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]

# Renderizar a página em resolução 150 DPI
bm = page.render(scale=150/72)
img = bm.to_pil()
out_png = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\scripts\rendered_mdt_page.png"
img.save(out_png)
print(f"Página renderizada salva em: {out_png} ({img.size})")

doc.close()
