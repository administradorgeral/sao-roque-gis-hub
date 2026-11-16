import pypdfium2 as pdfium

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\40537_4_3_3_1 Declividade.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]
objs = list(page.get_objects())
images = [obj for obj in objs if obj.type == 3]

print("Atributos de PdfImage:", [a for a in dir(images[0]) if not a.startswith('_')])
bm = images[0].get_bitmap()
pil_img = bm.to_pil()
pil_img.save(r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\scripts\sample_img_0.png")
print("Salvo com sucesso!", pil_img.size, pil_img.mode)

doc.close()
