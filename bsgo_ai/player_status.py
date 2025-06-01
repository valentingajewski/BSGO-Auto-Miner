import pathlib as Path
import sys
import signal

from detectors.asteroid_detector import mining_status
from detectors.text_from_image import extract_text
from combat import combat, killed_procedure
from base_procedure import repair, undock
from config import COMBAT_LOG_ZONE, SECTOR_TEXT_POSITION, PS_MINING, PS_IN_COMBAT, PS_INBASE, PS_JUMP, PS_KILLED
from jump import jump, ocr_check_sector, check_sector

def detect_if_damage_to_player(lines):
    """
    Détermine si le joueur est attaqué en comptant les occurrences de messages de dégâts.

    :param lines: liste de chaînes de texte issues de l'OCR (log du jeu)
    :return: True si au moins deux occurrences de dégâts détectées, sinon False
    """
    damage_count = 0
    
    for line in lines:
        line = line.lower()
        if "deals" in line and "damage to you" in line:
            damage_count += 1

    return damage_count >= 2

def detect_if_player_is_killed(zone):
    lines = extract_text(zone)
    for line in lines:
        if "You have been destroyed" in line:
            return True

def player_status_detection(target_sector_id):
    combat_log = detect_if_damage_to_player(extract_text(COMBAT_LOG_ZONE))
    sector = extract_text(SECTOR_TEXT_POSITION)
    is_good_sector = check_sector(ocr_check_sector(sector), target_sector_id)

    print(f'[INFO] Sector: {sector}')
    if combat_log >= 2:
        PLAYER_STATUS = PS_IN_COMBAT
    if detect_if_player_is_killed(COMBAT_LOG_ZONE):
        PLAYER_STATUS = PS_KILLED
    if len(sector) == 0 or len(sector[0]) <= 5:
        PLAYER_STATUS = PS_INBASE
    if is_good_sector is False:
        PLAYER_STATUS = PS_JUMP
    else:
        PLAYER_STATUS = PS_MINING

    print(f'[INFO] Player Status: {PLAYER_STATUS}')
    return PLAYER_STATUS

def status(sector_time, selected_sector_ids, target_sector_id):
    global PLAYER_STATUS
    while True:
        if PLAYER_STATUS == PS_MINING:
            PLAYER_STATUS = mining_status(sector_time, selected_sector_ids, target_sector_id)
        elif PLAYER_STATUS == PS_IN_COMBAT:
            PLAYER_STATUS = combat(target_sector_id)
        elif PLAYER_STATUS == PS_KILLED:
            PLAYER_STATUS = killed_procedure(target_sector_id)
        elif PLAYER_STATUS == PS_INBASE:
            repair()
            PLAYER_STATUS = undock(target_sector_id)
        elif PLAYER_STATUS == PS_JUMP:
            PLAYER_STATUS = jump(target_sector_id)
        else:
            print(PLAYER_STATUS)
        
        print(f'[INFO] Checking status: {PLAYER_STATUS}')
        player_status_detection(target_sector_id)


PLAYER_STATUS = player_status_detection(target_sector_id)

"""
if __name__ == "__main__":
    status()
"""