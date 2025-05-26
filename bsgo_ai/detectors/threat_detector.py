import pytesseract
import pyautogui
import cv2
import numpy as np

# Détection d’une menace en cours
def is_under_attack():
    # Capture d’une zone où les alertes sont visibles (adapter selon résolution)
    region = (800, 100, 400, 80)  # x, y, w, h
    screenshot = pyautogui.screenshot(region=region)
    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    text = pytesseract.image_to_string(gray).strip().upper()
    keywords = ["UNDER ATTACK", "ENEMY", "WARNING", "ALERT"]

    if any(keyword in text for keyword in keywords):
        print(f"[THREAT] Alerte détectée : {text}")
        return True

    return False
