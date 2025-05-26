import pyautogui
import pytesseract
import cv2
import time
import numpy as np

# Chemin vers Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Coordonnées de la zone (x, y, largeur, hauteur)
zone = (455, 84, 40, 20)

# Capture de la zone
x, y, w, h = zone

while True:

    screenshot = pyautogui.screenshot(region=(x, y, w, h))
    frame = np.array(screenshot)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # Redimensionner (agrandir 3x)
    resized = cv2.resize(frame, None, fx=7, fy=7, interpolation=cv2.INTER_CUBIC)

    # Convertir en niveaux de gris
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

    # OCR
    text = pytesseract.image_to_string(gray, config='--psm 6')
    print("Distance to Asteroid", text.strip())

    # Sauvegarde image pour debug
    cv2.imwrite("ocr_zone_debug.png", gray)

    time.sleep(2)
