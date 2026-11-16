import numpy as np
from PIL import Image

user_img = Image.open('C:/Users/admin/.gemini/antigravity/brain/8a767400-ab0f-40a5-b1b7-b7e6cab406ec/.user_uploaded/media_1794723676929_518256f4.jpg')
w, h = user_img.size
print(f"User screenshot size: {w} x {h}")

# The user screenshot shows Cotia, Raposo Tavares, and the white strip.
# Let's crop the Cotia / Raposo Tavares central section:
# Around x: 400 to 900, y: 150 to 450
crop = user_img.crop((400, 150, 900, 450))
crop.save('data/user_crop_cotia.png')
print("Saved data/user_crop_cotia.png")
