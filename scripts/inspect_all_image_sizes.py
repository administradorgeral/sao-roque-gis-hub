import pypdfium2 as pdfium

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\47531_4_2_3_2 MDT.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]

objs = list(page.get_objects())
images = [obj for obj in objs if obj.type == 3]

print(f"Total de imagens: {len(images)}")
for i, img in enumerate(images):
    px = img.get_px_size()
    b = img.get_bounds()
    if px[0] != 6836:
        print(f"Imagem {i}: px_size={px}, bounds={b}")

doc.close()
