import pypdfium2 as pdfium

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\47531_4_2_3_2 MDT.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]

objs = list(page.get_objects())
images = [obj for obj in objs if obj.type == 3][:87]

print(f"Total de tiras do mapa principal: {len(images)}")
print(f"Imagem 0: bounds={images[0].get_bounds()}, size={images[0].get_px_size()}")
print(f"Imagem 86: bounds={images[86].get_bounds()}, size={images[86].get_px_size()}")

total_h_px = sum(img.get_px_size()[1] for img in images)
print(f"Altura total acumulada em pixels: {total_h_px}")
print(f"Largura de cada tira em pixels: {images[0].get_px_size()[0]}")

doc.close()
