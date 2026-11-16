import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes
import numpy as np

# 1. Obter o limite municipal de referência da Declividade (já aprovado)
# Em Declividade, o limite municipal é o contorno exterior da mancha de classes
# ou um path preto específico.
# Vamos inspecionar os paths de limite em Declividade, MDT e Hidro.

files = {
    "DECLIVIDADE": r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\40537_4_3_3_1 Declividade.pdf",
    "MDT": r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\47531_4_2_3_2 MDT.pdf",
    "HIDRO": r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\Hidro .pdf"
}

r, g, b, a = ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint()

for name, path in files.items():
    doc = pdfium.PdfDocument(path)
    page = doc[0]
    objs = list(page.get_objects())
    path_objs = [o for o in objs if o.type == 2]
    
    # Encontrar a moldura interna do mapa (neatline)
    # A moldura é um retângulo fechado grande com W > 1500 e H > 1500
    neatlines = []
    for p in path_objs:
        box = p.get_bounds()
        w = box[2] - box[0]
        h = box[3] - box[1]
        if w > 1500 and h > 1500:
            neatlines.append((box, w, h))
            
    print(f"\n=== {name} ===")
    print(f"Total paths: {len(path_objs)}")
    print(f"Molduras (Neatlines) encontradas: {len(neatlines)}")
    for nl in neatlines:
        print(f"  Neatline: X0={nl[0][0]:.4f}, Y0={nl[0][1]:.4f}, X1={nl[0][2]:.4f}, Y1={nl[0][3]:.4f} (W={nl[1]:.4f}, H={nl[2]:.4f})")
        
    doc.close()
