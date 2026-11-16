import pypdfium2 as pdfium

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\47531_4_2_3_2 MDT.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]

objs = list(page.get_objects())
images = [obj for obj in objs if obj.type == 3][:87]

y_tops = [img.get_bounds()[3] for img in images]
print("Primeiros 15 Y_top:")
for i, y in enumerate(y_tops[:15]):
    print(f"  Img {i:2d}: Y_top = {y:.2f}")

is_sorted = all(y_tops[i] >= y_tops[i+1] for i in range(len(y_tops)-1))
print(f"\nAs imagens estão estritamente ordenadas por Y decrescente (topo para base)? {is_sorted}")

if not is_sorted:
    for i in range(len(y_tops)-1):
        if y_tops[i] < y_tops[i+1]:
            print(f"ERRO DE ORDEM: Img {i} (Y={y_tops[i]:.2f}) está ABAIXO de Img {i+1} (Y={y_tops[i+1]:.2f})!")

doc.close()
