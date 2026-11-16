import pypdfium2 as pdfium
import json
from collections import Counter

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\Hidro .pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]

print("=== INFORMAÇÕES DO DOCUMENTO ===")
metadata = doc.get_metadata_dict()
for k, v in metadata.items():
    print(f"  {k}: {v}")

pw = float(page.get_width())
ph = float(page.get_height())
print(f"\nDimensões da Página: {pw:.2f} x {ph:.2f} pt ({pw*25.4/72:.1f} x {ph*25.4/72:.1f} mm)")

objs = list(page.get_objects())
print(f"Total de objetos na página: {len(objs)}")

types = Counter([o.type for o in objs])
type_names = {1: "PATH (Vetor)", 2: "TEXT", 3: "IMAGE", 4: "SHADING", 5: "FORM"}
for t, cnt in types.items():
    print(f"  {type_names.get(t, f'Desconhecido({t})')}: {cnt}")

# Extrair todo o texto para entender a legenda e carimbo técnico
textpage = page.get_textpage()
n_chars = textpage.count_chars()
full_text = textpage.get_text_range()
print(f"\nTotal de caracteres de texto: {n_chars}")

# Buscar linhas de texto com posições
print("\n--- PALAVRAS-CHAVE E METADADOS DO CARIMBO/LEGENDA ---")
keywords = [
    "HIDRO", "BACIA", "SUB-BACIA", "RIO", "CÓRREGO", "CORREGO", "REPRESA",
    "NASCENTE", "IGC", "SIRGAS", "UTM", "ESCALA", "CREA", "ART", "ANEXO",
    "SÃO ROQUE", "GUAÇU", "CARAMBEÍ", "ITUPARARANGA", "SOROCABA"
]

lines = [line.strip() for line in full_text.split("\n") if line.strip()]
print(f"Total de linhas de texto extraídas: {len(lines)}")
for line in lines:
    if any(k in line.upper() for k in keywords):
        print(f"  [METADADO] {line}")

# Analisar cores e tipos de vetores (PATHs)
paths = [o for o in objs if o.type == 1]
stroke_colors = Counter()
fill_colors = Counter()
stroke_widths = Counter()

for p in paths:
    # get_stroke_color() e get_fill_color()
    try:
        sc = p.get_stroke_color()
        if sc:
            hex_sc = f"#{int(sc[0]):02X}{int(sc[1]):02X}{int(sc[2]):02X}"
            stroke_colors[hex_sc] += 1
    except Exception:
        pass
    try:
        fc = p.get_fill_color()
        if fc:
            hex_fc = f"#{int(fc[0]):02X}{int(fc[1]):02X}{int(fc[2]):02X}"
            fill_colors[hex_fc] += 1
    except Exception:
        pass

print("\n--- CORES DE LINHA (STROKE) NOS VETORES ---")
for c, cnt in stroke_colors.most_common(15):
    print(f"  {c}: {cnt} vetores")

print("\n--- CORES DE PREENCHIMENTO (FILL) NOS VETORES ---")
for c, cnt in fill_colors.most_common(15):
    print(f"  {c}: {cnt} vetores")

# Analisar coordenadas de grid ou neatline
print("\n--- BUSCANDO COORDENADAS UTM NAS MARGENS ---")
import re
utm_matches = []
for line in lines:
    # procurar números com 6 ou 7 dígitos típicos de UTM (ex: 280000, 7390000)
    nums = re.findall(r'\b(2[7-9]\d{4}|73[8-9]\d{4}|74[0-1]\d{4})\b', line)
    if nums:
        utm_matches.extend(nums)

print(f"Coordenadas UTM encontradas no texto: {sorted(list(set(utm_matches)))}")

doc.close()
