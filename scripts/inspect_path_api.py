import pypdfium2 as pdfium

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\40537_4_3_3_1 Declividade.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]

objs = list(page.get_objects())
path_objs = [obj for obj in objs if obj.type == 2]

p = path_objs[0]
print("Atributos de PdfPath:", [a for a in dir(p) if not a.startswith('_')])

# Testar métodos
for attr in ['get_stroke_color', 'get_fill_color', 'get_matrix', 'get_draw_mode']:
    if hasattr(p, attr):
        try:
            val = getattr(p, attr)()
            print(f"{attr}(): {val}")
        except Exception as e:
            print(f"{attr}() erro: {e}")

doc.close()
