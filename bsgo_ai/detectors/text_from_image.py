import pytesseract
import pyautogui
import cv2
import numpy as np
import easyocr


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
reader = easyocr.Reader(['en'], gpu=True)

def replace_confusables(text):
    confusables = {
        'i': '1', 'I': '1',
        'o': '0', 'O': '0',
        'l': '1', 'L': '1',
        's': '5', 'S': '5',
        'b': '6', 'B': '8',
        'g': '9', 'G': '9',
        'z': '2', 'Z': '2',
        'e': '3', 'E': '3',
        't': '7', 'T': '7',
        ',': '',  'm': '1'
    }
    return ''.join(confusables.get(c, c) for c in text)

"""
def extract_mineral_analysis(zone):

    x, y, w, h = zone
    screenshot = pyautogui.screenshot(region=(x, y, w, h))
    frame = np.array(screenshot)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    resized = cv2.resize(frame, None, fx=7, fy=7, interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray, config='--psm 6')

    return text
"""
def extract_text(zone):
    x, y, w, h = zone
    screenshot = pyautogui.screenshot(region=(x, y, w, h))
    img = np.array(screenshot)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    img = cv2.resize(img, None, fx=7, fy=7, interpolation=cv2.INTER_CUBIC)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    result = reader.readtext(img, detail=0)
    return result

def detect_if_player_is_killed(zone):
    lines = extract_text(zone)
    for line in lines:
        if "You have been destroyed" in line:
            return True


def extract_distance_to_asteroid(zone):
    x, y, w, h = zone
    screenshot = pyautogui.screenshot(region=(x, y, w, h))
    img = np.array(screenshot)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img = cv2.resize(img, None, fx=5, fy=5, interpolation=cv2.INTER_LINEAR)

    _, img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)
    img = cv2.GaussianBlur(img, (3, 3), 0)


    #text = pytesseract.image_to_string(img, config=config)
    #print("Text :", text.strip())
    #cv2.imwrite("ocr_zone_debug.png", img)

    result = reader.readtext(img, detail=0)
    return int(replace_confusables(result[0].lower().strip()))
