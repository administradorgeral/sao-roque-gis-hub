import pypdfium2 as pdfium
import re

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\Hidro .pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]
textpage = page.get_textpage()
n_chars = textpage.count_chars()

slope_x = 17.636222
intercept_x = 269492.23
slope_y = 17.639066
intercept_y = 7381376.13

# Extrair palavras dentro da área do mapa (X < 1680 e Y > 30 e Y < 1640)
# Agrupar em strings
full_text = textpage.get_text_range()

# Vamos buscar blocos de texto por proximidade espacial
char_data = []
for i in range(n_chars):
    box = textpage.get_charbox(i)
    c = textpage.get_text_range(i, 1)
    if box[0] < 1680 and 30 < box[1] < 1640 and c.strip():
        char_data.append((c, box))

print(f"Total de caracteres úteis dentro do mapa: {len(char_data)}")

# Agrupar caracteres contíguos em palavras/linhas
words = []
curr_str = ""
curr_box = None

for c, b in char_data:
    if not curr_str:
        curr_str = c
        curr_box = list(b)
    else:
        # Se estiver na mesma linha e próximo
        if abs(b[1] - curr_box[1]) < 3.0 and (b[0] - curr_box[2]) < 6.0:
            curr_str += c
            curr_box[2] = b[2]
            curr_box[3] = max(curr_box[3], b[3])
        else:
            words.append((curr_str, curr_box))
            curr_str = c
            curr_box = list(b)

if curr_str:
    words.append((curr_str, curr_box))

print(f"Total de fragmentos de texto agrupados no mapa: {len(words)}")

# Filtrar nomes hidrológicos ou toponímicos
hydro_terms = ["rio", "córrego", "corrego", "rib.", "ribeirão", "ribeirao", "represa", "itupararanga", "guaçu", "guacu", "carambeí", "carambei", "sorocaba", "saboó", "saboo", "taipas", "mailasqui", "canguera", "marmeleiro", "junqueira", "gabriel", "santo", "antonio", "pedro"]

identified_names = []
for w, box in words:
    w_low = w.lower()
    if any(t in w_low for t in hydro_terms) or len(w) > 4:
        # Converter para coordenadas UTM
        utm_x = slope_x * ((box[0]+box[2])/2.0) + intercept_x
        utm_y = slope_y * ((box[1]+box[3])/2.0) + intercept_y
        identified_names.append((w, utm_x, utm_y))

print("\n--- AMOSTRA DE TOPÔNIMOS / NOMES IDENTIFICADOS NO MAPA ---")
for item in sorted(identified_names, key=lambda x: x[0])[:40]:
    print(f"  '{item[0]}': UTM=({item[1]:.1f}, {item[2]:.1f})")

doc.close()
