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

# Extrair todos os blocos de texto no mapa que contenham "Tratamento", "Captação", "SABESP", "ETA", "ETE", "Bomba", "Reservatório"
keywords = ["tratamento", "capta", "sabesp", "eta", "ete", "bomba", "reservat", "esgoto", "potável", "sanitário"]

infra_points = []

# Vamos encontrar todos os trechos de texto
full_text = textpage.get_text_range()

for i in range(n_chars - 3):
    sub = textpage.get_text_range(i, 20)
    for kw in keywords:
        if kw in sub.lower():
            # Pegar caixa desse trecho
            b_first = textpage.get_charbox(i)
            b_last = textpage.get_charbox(min(n_chars-1, i + len(kw)))
            cx = (b_first[0] + b_last[2]) / 2.0
            cy = (b_first[1] + b_last[3]) / 2.0
            if cx < 1680 and 30 < cy < 1640:
                utm_x = slope_x * cx + intercept_x
                utm_y = slope_y * cy + intercept_y
                # Pegar o texto expandido ao redor
                start = max(0, i - 15)
                end = min(n_chars, i + 35)
                context = textpage.get_text_range(start, end - start).replace("\n", " ").strip()
                infra_points.append({
                    "termo": kw,
                    "texto_completo": context,
                    "utm_x": round(utm_x, 1),
                    "utm_y": round(utm_y, 1)
                })

# Deduplicar por proximidade (< 50 metros)
dedup = []
for p in infra_points:
    is_dup = False
    for d in dedup:
        if abs(p["utm_x"] - d["utm_x"]) < 50 and abs(p["utm_y"] - d["utm_y"]) < 50:
            is_dup = True
            break
    if not is_dup:
        dedup.append(p)

print(f"Instalações e Pontos de Infraestrutura Hídrica/Sanitária da SABESP detectados: {len(dedup)}")
for p in dedup:
    print(f"  [{p['termo'].upper()}] UTM=({p['utm_x']}, {p['utm_y']}): \"{p['texto_completo']}\"")

doc.close()
