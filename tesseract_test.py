try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract


results = pytesseract.image_to_string(Image.open('assets/sun_test.png'))
print(results)