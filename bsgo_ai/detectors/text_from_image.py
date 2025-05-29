import pytesseract
import pyautogui
import cv2
import numpy as np


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def extract_text(zone):

    x, y, w, h = zone
    screenshot = pyautogui.screenshot(region=(x, y, w, h))
    frame = np.array(screenshot)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    resized = cv2.resize(frame, None, fx=7, fy=7, interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray, config='--psm 6')

    return text


def extract_distance_to_asteroid(zone):
    x, y, w, h = zone
    screenshot = pyautogui.screenshot(region=(x, y, w, h))
    frame = np.array(screenshot)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # Agrandissement léger (x7 max)
    resized = cv2.resize(frame, None, fx=7, fy=7, interpolation=cv2.INTER_LINEAR)

    # Niveau de gris
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

    # Léger flou pour supprimer bruit
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)

    # Seuillage binaire automatique
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # OCR uniquement chiffres
    config = '--psm 7 -c tessedit_char_whitelist=0123456789'

    text = pytesseract.image_to_string(thresh, config=config)
    return int(text.strip())
