import pypdfium2 as pdfium
import numpy as np
import cv2
import time
from PIL import Image

print("Testando montagem e vetorização do MDT com OpenCV...")
t0 = time.time()

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\47531_4_2_3_2 MDT.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]

objs = list(page.get_objects())
images = [obj for obj in objs if obj.type == 3][:92]

print(f"[{time.time()-t0:.1f}s] Carregadas {len(images)} tiras do PDF.")

# As tiras estão empilhadas do topo (y max) para a base (y min)
# Imagem 0: y in [1601.2, 1619.7] pt (topo)
# Imagem 91: y in [36.0, 54.5] pt (base)
strip_bitmaps = []
for i in range(len(images)):
    bm = images[i].get_bitmap()
    arr = bm.to_numpy() # shape (H, W, 4) BGRA ou (H, W, 3) BGR
    # Em PDFium, to_numpy retorna BGRA
    strip_bitmaps.append(arr)

# Concatenar verticalmente
full_img = np.vstack(strip_bitmaps)
print(f"[{time.time()-t0:.1f}s] Imagem composta montada com sucesso! Shape: {full_img.shape} (H={full_img.shape[0]}, W={full_img.shape[1]})")

# Cores alvo em BGR (OpenCV usa BGR por padrão)
# Classe 1: #006100 -> BGR (0, 97, 0)
# Classe 2: #7AAB00 -> BGR (0, 171, 122)
# Classe 3: #FFFF00 -> BGR (0, 255, 255)
# Classe 4: #FF9900 -> BGR (0, 153, 255)
# Classe 5: #FF2200 -> BGR (0, 34, 255)

classes_bgr = {
    "CL_1_630_760": {"name": "630 a 760 m", "bgr": (0, 97, 0), "hex": "#006100"},
    "CL_2_760_830": {"name": "760 a 830 m", "bgr": (0, 171, 122), "hex": "#7AAB00"},
    "CL_3_830_900": {"name": "830 a 900 m", "bgr": (0, 255, 255), "hex": "#FFFF00"},
    "CL_4_900_970": {"name": "900 a 970 m", "bgr": (0, 153, 255), "hex": "#FF9900"},
    "CL_5_970_1125": {"name": "970 a 1.125 m", "bgr": (0, 34, 255), "hex": "#FF2200"},
}

# Testar contornos de uma classe
bgr_img = full_img[:, :, :3]
mask_c5 = cv2.inRange(bgr_img, np.array([0, 25, 240]), np.array([10, 45, 255]))
contours, _ = cv2.findContours(mask_c5, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
print(f"[{time.time()-t0:.1f}s] Classe 5 (970-1.125m): {len(contours)} contornos encontrados no OpenCV!")

doc.close()
