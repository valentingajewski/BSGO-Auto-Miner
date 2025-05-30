import pathlib as Path
import sys
import signal

from detectors.asteroid_detector import mining_status
from detectors.text_from_image import extract_text
from combat import combat, killed_procedure
from base_procedure import repair, undock
from config import COMBAT_LOG_ZONE, SECTOR_TEXT_POSITION, PS_MINING, PS_IN_COMBAT, PS_INBASE, PS_JUMP, PS_KILLED
from jump import jump

PLAYER_STATUS = PS_MINING

is_terminated = False

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    is_terminated = True

signal.signal(signal.SIGINT, signal_handler)

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
        if "killed" in line:
            return True


def player_status_detection():
    combat_log = detect_if_damage_to_player(extract_text(COMBAT_LOG_ZONE))
    sector = extract_text(SECTOR_TEXT_POSITION)
    if combat_log >= 2:
        PLAYER_STATUS = PS_IN_COMBAT
    if detect_if_player_is_killed(COMBAT_LOG_ZONE):
        PLAYER_STATUS = PS_KILLED
    if sector is False:
        PLAYER_STATUS = PS_INBASE
    else:
        PLAYER_STATUS = PS_MINING

    return PLAYER_STATUS

def status():
    print(f'[DEBUG] {is_terminated}')
    while not is_terminated:
        print('[DEBUG] While loop')
        if PLAYER_STATUS == PS_MINING:
            print('[DEBUG] MINING')
            mining_status()
        if PLAYER_STATUS == PS_IN_COMBAT:
            print('[DEBUG] IN COMBAT')
            combat()
        if PLAYER_STATUS == PS_KILLED:
            print('[DEBUG] KILLED')
            killed_procedure()
        if PLAYER_STATUS == PS_INBASE:
            print('[DEBUG] IN BASE')
            repair()
            undock()
        if PLAYER_STATUS == PS_JUMP:
            print('[DEBUG] JUMP')
            jump()
        
        print(f'[DEBUG] check status: {PLAYER_STATUS}')
        player_status_detection()

if __name__ == "__main__":
    status()
