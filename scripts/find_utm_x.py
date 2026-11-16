import pypdfium2 as pdfium

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\Hidro .pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]
textpage = page.get_textpage()
n_chars = textpage.count_chars()

print("Buscando números nas margens superior e inferior...")
for i in range(n_chars):
    box = textpage.get_charbox(i)
    # Margem inferior (Y < 35) ou margem superior (Y > 1635)
    if box[1] < 35 or box[1] > 1635:
        # Se X está dentro da área do mapa (X < 1720)
        if box[0] < 1720:
            char = textpage.get_text_range(i, 1)
            # Imprimir caracteres
            if char.strip():
                print(f"Char '{char}': X=[{box[0]:.2f}, {box[2]:.2f}], Y=[{box[1]:.2f}, {box[3]:.2f}]")

doc.close()
