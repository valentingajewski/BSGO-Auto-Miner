
import time
import time

import sys
from pathlib import Path

# Ajoute le chemin racine du projet pour que "bsgo_ai" soit trouvable
ROOT_PATH = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_PATH))

from bsgo_ai.detectors.asteroid_detector import detect_asteroid
from bsgo_ai.detectors.ocr_utils import extract_text
from bsgo_ai.actions.keyboard_control import scanning

zone_distance = (455, 84, 40, 20)

while True:
    found = detect_asteroid()
    if found:
        time.sleep(1)
        text = extract_text(zone_distance)
        print(f"[OCR] Texte brut lu : '{text}'")

        try:
            distance_str = ''.join(filter(str.isdigit, text))
            distance = int(distance_str)
            print(f"[OCR] Distance extraite : {distance}")

            if distance < 3000:
                print("[ACTION] Distance < 3000 → SCAN !")
                scanning()
                break  # on sort de la boucle pour le test
            else:
                print("[ACTION] Trop loin → on continue")
        except ValueError:
            print("[OCR] Impossible de lire une distance.")
    else:
        print("[INFO] Aucun astéroïde détecté.")

    time.sleep(1)
