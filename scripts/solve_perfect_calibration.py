import pypdfium2 as pdfium
import numpy as np

def calibrate_pdf(pdf_name, path):
    doc = pdfium.PdfDocument(path)
    page = doc[0]
    t = page.get_textpage()
    n = t.count_chars()
    chars = []
    for i in range(n):
        ch = t.get_text_range(i, 1)
        if ch in '\r\n\t': continue
        b = t.get_charbox(i)
        chars.append({'ch': ch, 'l': b[0], 'b': b[1], 'r': b[2], 't': b[3]})

    # Buscar UTM X targets
    x_pairs = []
    for val in [270000, 272000, 275000, 276000, 280000, 284000, 285000, 288000, 290000, 292000, 295000, 296000]:
        target = str(val)
        for i in range(len(chars) - len(target) + 1):
            cand = ''.join([chars[i+j]['ch'] for j in range(len(target))])
            if cand == target:
                cb = [chars[i+j] for j in range(len(target))]
                # Centro do texto do número base (sem zeros decimais se houver)
                cx = (min(c['l'] for c in cb) + max(c['r'] for c in cb)) / 2.0
                cy = (min(c['b'] for c in cb) + max(c['t'] for c in cb)) / 2.0
                # Apenas rótulos nas margens inferior (y < 40) ou superior (y > 1620)
                if (cy < 40 or cy > 1620) and cx < 1700:
                    x_pairs.append((cx, val, cy))
                    
    # Buscar UTM Y targets
    y_pairs = []
    for val in [7385000, 7390000, 7395000, 7400000, 7405000, 7410000]:
        target = str(val)
        for i in range(len(chars) - len(target) + 1):
            cand = ''.join([chars[i+j]['ch'] for j in range(len(target))])
            if cand == target:
                cb = [chars[i+j] for j in range(len(target))]
                cx = (min(c['l'] for c in cb) + max(c['r'] for c in cb)) / 2.0
                cy = (min(c['b'] for c in cb) + max(c['t'] for c in cb)) / 2.0
                # Apenas rótulos nas margens esquerda (cx < 40) ou direita (1670 < cx < 1720)
                if (cx < 40 or 1670 < cx < 1720) and 30 < cy < 1640:
                    y_pairs.append((cy, val, cx))

    doc.close()
    
    # Agrupar e fazer a média por valor UTM
    from collections import defaultdict
    x_by_val = defaultdict(list)
    for cx, val, cy in x_pairs:
        x_by_val[val].append(cx)
        
    y_by_val = defaultdict(list)
    for cy, val, cx in y_pairs:
        y_by_val[val].append(cy)
        
    x_pts = []
    x_utms = []
    for val in sorted(x_by_val.keys()):
        x_pts.append(np.mean(x_by_val[val]))
        x_utms.append(val)
        
    y_pts = []
    y_utms = []
    for val in sorted(y_by_val.keys()):
        y_pts.append(np.mean(y_by_val[val]))
        y_utms.append(val)
        
    x_pts = np.array(x_pts)
    x_utms = np.array(x_utms)
    y_pts = np.array(y_pts)
    y_utms = np.array(y_utms)
    
    sx, ix = np.polyfit(x_pts, x_utms, 1)
    sy, iy = np.polyfit(y_pts, y_utms, 1)
    
    print(f"\n=== CALIBRAÇÃO RIGOROSA: {pdf_name} ===")
    print(f"X Grid: {len(x_pts)} pontos de controle: {list(zip(np.round(x_pts, 1), x_utms))}")
    print(f"  UTM_X = {sx:.6f} * PDF_X + {ix:.2f}")
    print(f"  Erro max X: {np.max(np.abs(x_utms - (sx * x_pts + ix))):.4f} metros")
    
    print(f"Y Grid: {len(y_pts)} pontos de controle: {list(zip(np.round(y_pts, 1), y_utms))}")
    print(f"  UTM_Y = {sy:.6f} * PDF_Y + {iy:.2f}")
    print(f"  Erro max Y: {np.max(np.abs(y_utms - (sy * y_pts + iy))):.4f} metros")
    
    return {
        "pdf": pdf_name,
        "slope_x": sx, "intercept_x": ix,
        "slope_y": sy, "intercept_y": iy
    }

c_dec = calibrate_pdf("DECLIVIDADE", r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\40537_4_3_3_1 Declividade.pdf")
c_mdt = calibrate_pdf("MDT", r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\47531_4_2_3_2 MDT.pdf")
c_hidro = calibrate_pdf("HIDROGRAFIA", r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\Hidro .pdf")
