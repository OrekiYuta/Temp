import pytesseract
from PIL import Image

img = Image.open('a.png')
print(img)
b = pytesseract.image_to_string(img)

print(b)