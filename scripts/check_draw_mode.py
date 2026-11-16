import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\Hidro .pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]

objs = list(page.get_objects())
path_objs = [obj for obj in objs if obj.type == 2]

fill_mode = ctypes.c_int()
b_stroke = ctypes.c_int()

print("Inspecionando DrawMode de Path 2746 e 2747:")
for p_idx in [2746, 2747, 0, 1, 2766]:
    p = path_objs[p_idx]
    res = pdfium_c.FPDFPath_GetDrawMode(p.raw, ctypes.byref(fill_mode), ctypes.byref(b_stroke))
    print(f"Path {p_idx:4d}: res={res}, fill_mode={fill_mode.value}, b_stroke={b_stroke.value}")

# Contar quantos paths REALMENTE têm fill_mode != 0 (preenchidos) vs fill_mode == 0 (apenas linha/stroke)
fill_counts = {}
stroke_counts = {}
for idx, p in enumerate(path_objs):
    pdfium_c.FPDFPath_GetDrawMode(p.raw, ctypes.byref(fill_mode), ctypes.byref(b_stroke))
    fm = fill_mode.value
    bs = b_stroke.value
    fill_counts[fm] = fill_counts.get(fm, 0) + 1
    stroke_counts[bs] = stroke_counts.get(bs, 0) + 1

print("\n--- DISTRIBUIÇÃO DE FILL MODE EM TODOS OS 5071 PATHS ---")
print("Fill Mode (0 = SEM PREENCHIMENTO / STROKE ONLY, 1 = ALTERNATE, 2 = WINDING):")
for fm, cnt in sorted(fill_counts.items()):
    print(f"  fill_mode = {fm}: {cnt} paths")

print("\nStroke (0 = sem traço, 1 = com traço):")
for bs, cnt in sorted(stroke_counts.items()):
    print(f"  b_stroke  = {bs}: {cnt} paths")

doc.close()
