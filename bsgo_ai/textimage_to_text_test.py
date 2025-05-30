import pyautogui
import pytesseract
import cv2
import time
import numpy as np
import easyocr


# Chemin vers Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Coordonnées de la zone (x, y, largeur, hauteur)
zone = (35, 1173, 325, 210)

reader = easyocr.Reader(['en'])

def detect_if_damage_to_player(lines):
    #print(f'[DEBUG] combat_log: {lines}')
    """
    Détermine si le joueur est attaqué en comptant les occurrences de messages de dégâts.

    :param lines: liste de chaînes de texte issues de l'OCR (log du jeu)
    :return: True si au moins deux occurrences de dégâts détectées, sinon False
    """
    damage_count = 0
    
    for line in lines:
        line = line.lower()
        if "deals" in line and "damage to you" in line:
            damage_count += 1

    return damage_count >= 2

def extract_text(zone):
    x, y, w, h = zone
    screenshot = pyautogui.screenshot(region=(x, y, w, h))
    img = np.array(screenshot)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    img = cv2.resize(img, None, fx=7, fy=7, interpolation=cv2.INTER_CUBIC)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("extract_text.png", img)
    result = reader.readtext('extract_text.png', detail=0)

    return result
if __name__ == "__main__":
    combat_log = detect_if_damage_to_player(extract_text(zone))
    print(combat_log)

"""
while True:

    

    x, y, w, h = zone
    screenshot = pyautogui.screenshot(region=(x, y, w, h))
    img = np.array(screenshot)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    img = cv2.resize(img, None, fx=7, fy=7, interpolation=cv2.INTER_CUBIC)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(img, config='--psm 6')

    #text = pytesseract.image_to_string(img, config=config)
    #print("Text :", text.strip())
    cv2.imwrite("ocr_zone_debug.png", img)



    result = reader.readtext('ocr_zone_debug.png', detail=0)
    print(result)

    time.sleep(1)
"""


