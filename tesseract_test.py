import cv2, pytesseract

img = cv2.imread('image5.jpg')

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

result = pytesseract.image_to_string(img)

print(result)