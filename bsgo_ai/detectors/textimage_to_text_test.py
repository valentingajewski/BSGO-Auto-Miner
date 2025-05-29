import pyautogui
import pytesseract
import cv2
import time
import numpy as np
import easyocr


# Chemin vers Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Coordonnées de la zone (x, y, largeur, hauteur)
zone = (455, 84, 40, 15)

reader = easyocr.Reader(['en'])

while True:

    

    x, y, w, h = zone
    screenshot = pyautogui.screenshot(region=(x, y, w, h))
    img = np.array(screenshot)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img = cv2.resize(img, None, fx=5, fy=5, interpolation=cv2.INTER_LINEAR)

    _, img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)
    img = cv2.GaussianBlur(img, (3, 3), 0)

    config = '--psm 7 -c tessedit_char_whitelist=0123456789'

    #text = pytesseract.image_to_string(img, config=config)
    #print("Text :", text.strip())
    cv2.imwrite("ocr_zone_debug.png", img)



    result = reader.readtext('ocr_zone_debug.png', detail=0)
    print(result)

    time.sleep(1)

