try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
# import


results = pytesseract.image_to_string(Image.open('ss/ss1.png'))
print(results)