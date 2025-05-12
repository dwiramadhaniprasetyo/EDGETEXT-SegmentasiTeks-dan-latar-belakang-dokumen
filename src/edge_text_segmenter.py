import cv2
import numpy as np
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
def segment_text(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError("Gambar tidak ditemukan.")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Thresholding adaptif
    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        blockSize=15,
        C=11
    )

    # Operasi morfologi untuk memperjelas teks
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    return image, morph

def extract_text_from_image(image_array):
    pil_img = Image.fromarray(image_array)
    return pytesseract.image_to_string(pil_img, lang='eng')
