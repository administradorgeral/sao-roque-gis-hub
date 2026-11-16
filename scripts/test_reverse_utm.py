import numpy as np

# Testar alinhamento de um ponto de teste UTM conhecido, por exemplo UTM X=280000, Y=7395000:
# Em Declividade:
# PDF_X = (280000 - 269709.68) / 17.636225 = 583.476 pt
# PDF_Y = (7395000 - 7381599.70) / 17.637638 = 759.756 pt

# Em MDT:
# PDF_X = (280000 - 270233.84) / 17.640225 = 553.630 pt
# PDF_Y = (7395000 - 7381324.25) / 17.641051 = 775.223 pt

# Em Hidro:
# PDF_X = (280000 - 269256.56) / 17.636163 = 609.171 pt
# PDF_Y = (7395000 - 7381376.20) / 17.638983 = 772.368 pt

# Agora, o caminho inverso: dado o ponto em cada PDF, a conversão para UTM resulta no mesmo lugar?
print("=== TESTE DE CONVERSÃO REVERSA PARA UTM (280000, 7395000) ===")
utm_dec_x = 17.636225 * 583.476 + 269709.68
utm_dec_y = 17.637638 * 759.756 + 7381599.70
print(f"Declividade -> UTM: ({utm_dec_x:.2f}, {utm_dec_y:.2f})")

utm_mdt_x = 17.640225 * 553.630 + 270233.84
utm_mdt_y = 17.641051 * 775.223 + 7381324.25
print(f"MDT         -> UTM: ({utm_mdt_x:.2f}, {utm_mdt_y:.2f})")

utm_hid_x = 17.636163 * 609.171 + 269256.56
utm_hid_y = 17.638983 * 772.368 + 7381376.20
print(f"Hidrografia -> UTM: ({utm_hid_x:.2f}, {utm_hid_y:.2f})")
