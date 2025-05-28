import math
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))
from bsgo_ai.config import SHIP_VMAX, SHIP_ACCELERATION, MINING_GUN1, MINING_GUN2

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
    v_max = SHIP_VMAX
    acceleration = SHIP_ACCELERATION

    if acceleration <= 0 or distance <= 0:
        return float('inf')

    d_accel = (v_max ** 2) / (2 * acceleration)

    if distance > d_accel:
        t1 = v_max / acceleration
        d2 = distance - d_accel
        t2 = d2 / v_max
        return t1 + t2
    else:
        return math.sqrt(2 * distance / acceleration)
    


if __name__ == "__main__":
    print(pc_time(1471))