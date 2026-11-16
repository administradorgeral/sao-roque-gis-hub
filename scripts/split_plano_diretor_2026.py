import os
import pypdfium2 as pdfium
from PIL import Image

print("=== INICIANDO DESMEMBRAMENTO DO PLANO DIRETOR (COMBINED.PDF) ===")

src_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\minuta_pd2026\Plano Diretor - Combined.pdf"
base_out = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\minuta_pd2026\desmembrado"
cartas_dir = os.path.join(base_out, "02_cartas_tecnicas")
renders_dir = os.path.join(cartas_dir, "renders_png")

os.makedirs(base_out, exist_ok=True)
os.makedirs(cartas_dir, exist_ok=True)
os.makedirs(renders_dir, exist_ok=True)

doc = pdfium.PdfDocument(src_path)
total_pages = len(doc)
print(f"Documento carregado: {total_pages} páginas.")

# 1. Desmembrar as 4 Seções Textuais Principais
text_sections = [
    ("01_participacao_popular_sugestoes.pdf", 0, 74, "Bloco 1: Participação Popular e Notas Técnicas"),
    ("03_minuta_lc39_plano_diretor_estrategico.pdf", 87, 152, "Bloco 3: Minuta LC 39/2006 (Plano Diretor Estratégico)"),
    ("04_minuta_lc40_zoneamento_uso_ocupacao.pdf", 152, 214, "Bloco 4: Minuta LC 40/2006 (Zoneamento, Uso e Ocupação)"),
    ("05_projetos_lei_camara_municipal.pdf", 214, 318, "Bloco 5: Mensagens e Projetos de Lei Formatados")
]

for filename, start_idx, end_idx, desc in text_sections:
    out_path = os.path.join(base_out, filename)
    sub_doc = pdfium.PdfDocument.new()
    page_indices = list(range(start_idx, end_idx))
    sub_doc.import_pages(doc, page_indices)
    sub_doc.save(out_path)
    size_mb = os.path.getsize(out_path) / (1024 * 1024)
    print(f"✓ Salvo: {filename} ({len(page_indices)} págs, {size_mb:.2f} MB) - {desc}")

# 2. Desmembrar e Renderizar as 13 Cartas Técnicas (páginas 75 a 87 / índices 74 a 86)
cartas_metadata = [
    (74, "carta_01_macrozoneamento_municipal", "Carta I - Macrozoneamento Municipal"),
    (75, "carta_02_zoneamentos_macrozona_urbanizacao_especifica", "Carta II - Zoneamentos da Macrozona de Urbanização Específica"),
    (76, "carta_03_zoneamentos_macrozona_consolidacao_urbana", "Carta III - Zoneamentos da Macrozona de Consolidação Urbana"),
    (77, "carta_04_zoneamento_consolidacao_urbana_sede", "Carta IV - Zoneamento de Consolidação Urbana (Sede)"),
    (78, "carta_05_zoneamento_consolidacao_urbana_maylasky", "Carta V - Zoneamento de Consolidação Urbana (Maylasky)"),
    (79, "carta_06_zoneamento_consolidacao_urbana_sao_joao_novo", "Carta VI - Zoneamento de Consolidação Urbana (São João Novo)"),
    (80, "carta_07_zoneamento_consolidacao_urbana_canguera", "Carta VII - Zoneamento de Consolidação Urbana (Canguera)"),
    (81, "carta_08_corredores_comercio_servicos_turismo", "Carta VIII - Corredores de Comércio, Serviços e Turismo"),
    (82, "carta_09_areas_especial_interesse_aeis_aeit_aeiu", "Carta IX - Áreas de Especial Interesse (AEIS, AEIT, AEIU)"),
    (83, "carta_10_sistema_viario_drenagem_sede", "Carta X - Sistema Viário e Drenagem (Sede Municipal)"),
    (84, "carta_11_sistema_viario_drenagem_maylasky", "Carta XI - Sistema Viário e Drenagem (Maylasky)"),
    (85, "carta_12_sistema_viario_drenagem_canguera", "Carta XII - Sistema Viário e Drenagem (Canguera)"),
    (86, "carta_13_intervencoes_obras_prioritarias_srq01_srq22", "Carta XIII - Intervenções e Obras Prioritárias (SRQ-01 a SRQ-22)")
]

print("\n--- Processando as 13 Cartas Técnicas Individuais ---")
scale_render = 150 / 72  # 150 DPI para renderização equilibrada e nítida

for p_idx, file_base, title in cartas_metadata:
    # 2.1 Salvar PDF individual da Carta
    carta_pdf = os.path.join(cartas_dir, f"{file_base}.pdf")
    c_doc = pdfium.PdfDocument.new()
    c_doc.import_pages(doc, [p_idx])
    c_doc.save(carta_pdf)
    size_kb = os.path.getsize(carta_pdf) / 1024
    
    # 2.2 Renderizar PNG de alta resolução
    page = doc[p_idx]
    bitmap = page.render(scale=scale_render)
    pil_img = bitmap.to_pil()
    png_path = os.path.join(renders_dir, f"{file_base}.png")
    pil_img.save(png_path, optimize=True)
    img_size = os.path.getsize(png_path) / (1024 * 1024)
    
    print(f"✓ {title}:")
    print(f"    PDF: {file_base}.pdf ({size_kb:.1f} KB)")
    print(f"    PNG: {file_base}.png ({pil_img.width}x{pil_img.height} px, {img_size:.2f} MB)")

print("\n=== DESMEMBRAMENTO CONCLUÍDO COM SUCESSO! ===")
