import time
import pyautogui
from detectors import ocr_utils

def handle():
    print("[BASE] Le joueur est dans une base alliée.")
    
    # Vérifier à nouveau par sécurité
    if not ocr_utils.is_in_base():
        print("[BASE] Alerte : on n'est pas dans une base, annulation.")
        return

    print("[BASE] Réparation du vaisseau...")
    pyautogui.click(960, 580)  # clic sur bouton "Repair" (adapter si besoin)
    time.sleep(2)

    print("[BASE] Attente de la fin de réparation (25 sec)...")
    time.sleep(25)

    print("[BASE] Tentative de sortie de la base...")
    pyautogui.click(1800, 960)  # clic sur bouton "Launch" ou équivalent
    time.sleep(2)

    print("[BASE] Sortie effectuée.")
