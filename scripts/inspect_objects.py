import pypdfium2 as pdfium

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\40537_4_3_3_1 Declividade.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]

# Procurando objetos gráficos na página
objs = list(page.get_objects())
print(f"Total de objetos na página: {len(objs)}")

rects = []
for obj in objs:
    obj_type = obj.type # PATH, IMAGE, TEXT, etc.
    bounds = obj.get_bounds()
    # bounds: (left, bottom, right, top)
    if bounds[2] - bounds[0] > 500 and bounds[3] - bounds[1] > 500:
        print(f"Objeto Grande Tipo {obj_type}: bounds={bounds}")

doc.close()
