import pytesseract
import pyautogui
import cv2
import numpy as np


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def extract_text(zone):

    # zone = (455, 84, 40, 20)
    x, y, w, h = zone
    screenshot = pyautogui.screenshot(region=(x, y, w, h))
    frame = np.array(screenshot)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    resized = cv2.resize(frame, None, fx=7, fy=7, interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray, config='--psm 6')

    return text


