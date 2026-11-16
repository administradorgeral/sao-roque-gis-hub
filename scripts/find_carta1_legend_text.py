import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\minuta_pd2026\desmembrado\02_cartas_tecnicas\carta_01_macrozoneamento_municipal.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]

tp = page.get_textpage()
left, bottom, right, top = ctypes.c_float(), ctypes.c_float(), ctypes.c_float(), ctypes.c_float()

# Scan all text objects and their positions
text_items = []
for idx, obj in enumerate(page.get_objects()):
    if obj.type == pdfium.raw.FPDF_PAGEOBJ_TEXT:
        pdfium_c.FPDFPageObj_GetBounds(obj.raw, ctypes.byref(left), ctypes.byref(bottom), ctypes.byref(right), ctypes.byref(top))
        
        # In pypdfium2, extract text from text object if possible, or use textpage char boxes
        text_items.append((left.value, bottom.value, right.value, top.value))

print(f"Total text objects: {len(text_items)}")

# Let's inspect text near the right side or bottom (where title blocks / legends usually are)
# Page size is 2384 x 1684. Title block is usually at bottom-right (x > 1800, y < 500)
# Or legend is at left (x < 600, y > 1000) or right.
n_chars = tp.count_chars()
chars_pos = []
for c_i in range(n_chars):
    box = tp.get_charbox(c_i)
    char = tp.get_text_range(c_i, 1)
    chars_pos.append((char, box))

# Group characters into words/lines with coordinates
words = []
cur_word = ""
cur_box = None
for char, box in chars_pos:
    if char in ["\n", "\r", " "]:
        if cur_word:
            words.append((cur_word, cur_box))
            cur_word = ""
            cur_box = None
    else:
        cur_word += char
        if cur_box is None:
            cur_box = list(box)
        else:
            cur_box[0] = min(cur_box[0], box[0])
            cur_box[1] = min(cur_box[1], box[1])
            cur_box[2] = max(cur_box[2], box[2])
            cur_box[3] = max(cur_box[3], box[3])
if cur_word:
    words.append((cur_word, cur_box))

print(f"Total words: {len(words)}")

# Look for legend words
for w, box in words:
    if any(k in w.upper() for k in ["LEGENDA", "MACROZONA", "ESPECÍFICA", "RURAL", "CONSOLIDAÇÃO", "CONSOLIDAÇÃO", "MANANCIAL", "MUNICIPAL"]):
        print(f"Word '{w}' at x=[{box[0]:.1f}, {box[2]:.1f}], y=[{box[1]:.1f}, {box[3]:.1f}]")
