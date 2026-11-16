from PIL import Image

img = Image.open('data/rbcv_cinturao_verde_regional.png')

# 1. Cotia patch
crop_cotia = img.crop((500, 1050, 750, 1300))
crop_cotia.save('data/inspect_cotia.png')

# 2. Santos / Ilha Porchat patch
crop_santos = img.crop((1100, 1450, 1300, 1650))
crop_santos.save('data/inspect_santos.png')

# 3. Jaraguá patch
crop_jaragua = img.crop((700, 950, 850, 1100))
crop_jaragua.save('data/inspect_jaragua.png')

print("Saved inspection crops: inspect_cotia.png, inspect_santos.png, inspect_jaragua.png")
