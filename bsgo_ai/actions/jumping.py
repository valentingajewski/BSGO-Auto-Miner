import json
import pyautogui
import time
import random

# Charger les coordonnées de la carte
with open("assets/sectors_map.json", "r") as f:
    sector_coords = json.load(f)

# Simule un saut
def jump_to_sector(name):
    if name not in sector_coords:
        print(f"[JUMP] Secteur inconnu : {name}")
        return False

    x, y = sector_coords[name]
    print(f"[JUMP] Tentative de saut vers {name} en cliquant sur {x},{y}")

    # Ouvre la carte
    pyautogui.press('m')
    time.sleep(2)

    # Clique sur la destination
    pyautogui.click(x, y)
    time.sleep(2)

    # Valider si nécessaire (ex : bouton "JUMP")
    pyautogui.click(x + 100, y + 150)  # zone approximative du bouton "Jump" à adapter

    print(f"[JUMP] Saut lancé vers {name}")
    time.sleep(5)
    return True

# Retourne True si un saut est nécessaire
def should_jump(config):
    # À implémenter : reconnaissance du secteur actuel (par OCR ou autre)
    # Pour l'instant, on suppose qu'on ne doit pas sauter
    return False

def handle(config):
    for sector in config["sectors"]:
        print(f"[JUMP] Navigation vers : {sector}")
        success = jump_to_sector(sector)
        if success:
            time.sleep(15)  # Temps estimé pour le saut
            break
