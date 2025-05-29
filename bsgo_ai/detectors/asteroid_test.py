import math
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))
from bsgo_ai.config import SHIP_VMAX, SHIP_PC_ACCELERATION, MINING_GUN1, MINING_GUN2

import math

def pc_time(distance):
    """
    Calcule le temps nécessaire pour parcourir (distance - 1000) mètres
    en partant à l'arrêt, avec accélération jusqu'à v_max puis vitesse constante.

    Paramètres :
    - v_max : vitesse maximale (m/s)
    - acceleration : accélération constante (m/s²)
    - distance : distance totale à parcourir (mètres)

    Retour :
    - temps estimé en secondes (float)
    """

    
    adjusted_distance = max(0, distance - 1000)
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

    


if __name__ == "__main__":
    print(pc_time(1471))