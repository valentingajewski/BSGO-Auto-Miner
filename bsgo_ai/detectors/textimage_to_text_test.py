import pyautogui
import pytesseract
import cv2
import time
import numpy as np
import easyocr


# Chemin vers Tesseract
#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Coordonnées de la zone (x, y, largeur, hauteur)
zone = (6, 10, 100, 12)

reader = easyocr.Reader(['en'])

while True:

    x, y, w, h = zone
    screenshot = pyautogui.screenshot(region=(x, y, w, h))
    img = np.array(screenshot)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    img = cv2.resize(img, None, fx=7, fy=7, interpolation=cv2.INTER_CUBIC)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("ocr_zone_debug.png", img)

    result = reader.readtext('ocr_zone_debug.png', detail=0)
    result = reader.readtext(img, detail=0)
    print(result)

    time.sleep(1)

