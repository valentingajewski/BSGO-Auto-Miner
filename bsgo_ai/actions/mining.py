import math
import time
import pyautogui
import keyboard
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))
from bsgo_ai.config import SHIP_VMAX, SHIP_PC_ACCELERATION, MINING_GUN1, MINING_GUN2, RESET_CURSOR_POSITION, TARGET_CURSOR_COORDS

def moveToCursorCoords(coords, side):
    pyautogui.moveTo(coords, duration=0.1)
    pyautogui.click(button=side)

def pc_time(distance):
    """
    Calcule le temps nécessaire pour atteindre un astéroïde
    en partant à l'arrêt avec une accélération constante.

    Paramètres :
    - v_max : vitesse maximale (unités/s)
    - acceleration : accélération (unités/s²)
    - distance : distance à parcourir (unités)

    Retour :
    - temps estimé en secondes (float)
    """
    if distance <= 700:
        return 0.0

    adjusted_distance = max(0, distance - 700)
    v_max = SHIP_VMAX
    acceleration = SHIP_PC_ACCELERATION

    if acceleration <= 0 or adjusted_distance <= 0:
        return float('inf')  # Cas non physique ou déjà arrivé

    d_accel = (v_max ** 2) / (2 * acceleration)

    if adjusted_distance > d_accel:
        t1 = v_max / acceleration
        d2 = adjusted_distance - d_accel
        t2 = d2 / v_max
        return t1 + t2
    else:
        return math.sqrt(2 * adjusted_distance / acceleration)

def approach_nearest_asteroid(coords, distance):
    """
    Approche automatiquement l'astéroïde le plus proche.

    - Calcule le temps de parcours avec pc_time.
    - Lance la séquence de touches pour l'approche.

    :param distance: distance à parcourir (int ou float)
    :param coords: tuple (x, y) des coordonnées de l'astéroïde
    :param v_max: vitesse max du vaisseau
    :param acceleration: accélération du vaisseau
    """

    x, y = coords
    duration = pc_time(distance)

    if duration == float('inf'):
        print("Temps de parcours invalide.")
        return

    print(f"Début de l'approche. Durée estimée : {duration:.2f}s")

    # Shift + T
    print(f"[DEBUG] Pressing SHIFT + T")
    pyautogui.keyDown('shift')
    pyautogui.press('t')
    pyautogui.keyUp('shift')

    print(f"[DEBUG] Right Clicking on coordinates: {x,y}")
    moveToCursorCoords((TARGET_CURSOR_COORDS),'right')
    time.sleep(0.2)

    hold_time = max(0, duration)
    if hold_time > 0:
        print(f"Maintien de la touche ESPACE pendant {hold_time:.2f}s")
        pyautogui.press('space')
        time.sleep(hold_time)
        pyautogui.press('space')
    else:
        print("Pas besoin de propulsion : l'astéroïde est très proche.")

    # Appuyer sur Q pendant 2 secondes
    pyautogui.keyDown('q')
    time.sleep(0.5)
    pyautogui.keyUp('q')

    # Appuyer sur pavé numérique 5 et 6
    moveToCursorCoords(MINING_GUN1, 'left')
    time.sleep(0.2)
    moveToCursorCoords(MINING_GUN2, 'left')

    pyautogui.press('.')

    print("Approche terminée.")

    time.sleep(20)

    moveToCursorCoords(MINING_GUN1, 'left')
    time.sleep(0.2)
    moveToCursorCoords(MINING_GUN2, 'left')
