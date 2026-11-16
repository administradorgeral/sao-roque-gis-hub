import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes
from collections import Counter

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\Hidro .pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]

objs = list(page.get_objects())
path_objs = [obj for obj in objs if obj.type == 2]

# Analisar os caminhos azuis (#0A93FC e #4065EB) e represas (#97DBF2)
blue_linear = []
blue_main = []
water_bodies = []
other = []

for idx, p in enumerate(path_objs):
    r_val = ctypes.c_uint()
    g_val = ctypes.c_uint()
    b_val = ctypes.c_uint()
    a_val = ctypes.c_uint()
    
    s_col, f_col = None, None
    if pdfium_c.FPDFPageObj_GetStrokeColor(p.raw, ctypes.byref(r_val), ctypes.byref(g_val), ctypes.byref(b_val), ctypes.byref(a_val)):
        s_col = (r_val.value, g_val.value, b_val.value)
    if pdfium_c.FPDFPageObj_GetFillColor(p.raw, ctypes.byref(r_val), ctypes.byref(g_val), ctypes.byref(b_val), ctypes.byref(a_val)):
        f_col = (r_val.value, g_val.value, b_val.value)
        
    s_hex = f"#{s_col[0]:02X}{s_col[1]:02X}{s_col[2]:02X}" if s_col else "NONE"
    f_hex = f"#{f_col[0]:02X}{f_col[1]:02X}{f_col[2]:02X}" if f_col else "NONE"
    
    b = p.get_bounds()
    # Ignorar elementos da legenda e barra lateral (X > 1680)
    if b[0] > 1680:
        continue
    # Ignorar a própria moldura externa
    if (b[2] - b[0]) > 1600 and (b[3] - b[1]) > 1550:
        continue
        
    n_segs = pdfium_c.FPDFPath_CountSegments(p.raw)
    
    if s_hex == "#0A93FC":
        blue_linear.append((idx, p, n_segs, b))
    elif s_hex == "#4065EB":
        blue_main.append((idx, p, n_segs, b))
    elif f_hex == "#97DBF2":
        water_bodies.append((idx, p, n_segs, b))
    else:
        other.append((idx, p, n_segs, b, s_hex, f_hex))

print("=== SEGMENTAÇÃO DE OBJETOS DA HIDROGRAFIA NO MAPA ÚTIL ===")
print(f"Cursos d'Água Secundários/Afluentes (#0A93FC): {len(blue_linear)} vetores")
print(f"Rios Principais / Calhas Principais (#4065EB): {len(blue_main)} vetores")
print(f"Represas / Corpos d'Água Poligonais (#97DBF2): {len(water_bodies)} vetores")
print(f"Outros objetos (limites, malha, anotações): {len(other)} vetores")

def inspect_segments(sample_path):
    p_raw = sample_path[1].raw
    n = sample_path[2]
    coords = []
    x = ctypes.c_float()
    y = ctypes.c_float()
    for i in range(n):
        seg = pdfium_c.FPDFPath_GetPathSegment(p_raw, i)
        pdfium_c.FPDFPathSegment_GetPoint(seg, ctypes.byref(x), ctypes.byref(y))
        t = pdfium_c.FPDFPathSegment_GetType(seg)
        c = pdfium_c.FPDFPathSegment_GetClose(seg)
        coords.append((x.value, y.value, t, c))
    return coords

print("\n--- AMOSTRA: CURSO D'ÁGUA SECUNDÁRIO ---")
pts = inspect_segments(blue_linear[0])
print(f"Path {blue_linear[0][0]}: {len(pts)} pontos. Primeiros 5:")
for pt in pts[:5]:
    print(f"  X={pt[0]:.2f}, Y={pt[1]:.2f}, type={pt[2]}, close={pt[3]}")

print("\n--- AMOSTRA: RIO PRINCIPAL ---")
pts_main = inspect_segments(blue_main[0])
print(f"Path {blue_main[0][0]}: {len(pts_main)} pontos. Primeiros 5:")
for pt in pts_main[:5]:
    print(f"  X={pt[0]:.2f}, Y={pt[1]:.2f}, type={pt[2]}, close={pt[3]}")

print("\n--- AMOSTRA: REPRESA / CORPO D'ÁGUA POLIGONAL ---")
pts_wb = inspect_segments(water_bodies[0])
print(f"Path {water_bodies[0][0]}: {len(pts_wb)} pontos. Primeiros 5:")
for pt in pts_wb[:5]:
    print(f"  X={pt[0]:.2f}, Y={pt[1]:.2f}, type={pt[2]}, close={pt[3]}")

doc.close()
