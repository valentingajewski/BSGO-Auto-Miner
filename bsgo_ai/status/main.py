# Libraries imports
import time
from termcolor import colored

# Class imports
from mining import Mining
from inbase import InBase
from sector import Sector
from combat import Combat

# Config/files imports
from bsgo_ai.pyautogui_lib import starting_procedure
from bsgo_ai.config import (SECTOR_TEXT_POSITION, PS_MINING, PS_INBASE, PS_JUMP, LIST_TARGET_SECTOR)
from bsgo_ai.json_loader import start_time, mining_sector_session_duration, mining_session_duration, GUI_CONFIG
from bsgo_ai.detectors.text_from_image import extract_text

# Class instances
mining = Mining()
inbase = InBase()
sector = Sector()
combat = Combat()

current_sector = 0
sector_start_time = time.time()
target_sector_id = GUI_CONFIG[LIST_TARGET_SECTOR][current_sector]
#sector_list = sector.extract_sector_from_text()

def detect_if_damage_to_player(lines):
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

def detect_if_in_right_sector(target_sector_id):
    sector_list = sector.extract_sector_from_wing()
    print(f'[INFO] Sector: {sector_list}')
    is_good_sector = sector.check_sector(sector.ocr_check_sector(sector_list), target_sector_id)
    return is_good_sector

def detect_if_player_in_base():
    sector_list = extract_text(SECTOR_TEXT_POSITION)
    return len(sector_list) == 0 or len(sector_list[0]) <= 3

def player_status_detection(target_sector_id):
    if detect_if_player_in_base() is True:
        return PS_INBASE
    if detect_if_in_right_sector(target_sector_id) is False:
        return PS_JUMP
        #sector.jump_shortest_path(sector_list, target_sector_id)
    else:
        return PS_MINING

def status(sector_time):
    global PLAYER_STATUS
    global sector_start_time
    global current_sector
    global target_sector_id
    if PLAYER_STATUS == PS_MINING:
        PLAYER_STATUS = mining.mining_status(sector_time, target_sector_id=target_sector_id)
    elif PLAYER_STATUS == PS_INBASE: 
        inbase.repair()
        inbase.undock()
    elif PLAYER_STATUS == PS_JUMP:
        sector_list = sector.extract_sector_from_wing()
        PLAYER_STATUS = sector.jump_shortest_path(sector_list, target_sector_id)
        print(PLAYER_STATUS)

#starting_procedure()
PLAYER_STATUS = player_status_detection(target_sector_id)

while time.time() - start_time < mining_session_duration:
    if PLAYER_STATUS == PS_MINING and time.time() - sector_start_time > mining_sector_session_duration:
        current_sector += 1
        try:
            target_sector_id = GUI_CONFIG[LIST_TARGET_SECTOR][current_sector]
        except IndexError:
            current_sector = 0
            target_sector_id = GUI_CONFIG[LIST_TARGET_SECTOR][current_sector]
        PLAYER_STATUS = PS_JUMP
        sector_start_time = 0

    status(mining_sector_session_duration)
    PLAYER_STATUS = player_status_detection(target_sector_id)

    # Réinitialise sector_start_time si on vient d'arriver dans un bon secteur
    if PLAYER_STATUS == PS_MINING and sector_start_time == 0:
        sector_start_time = time.time()
print("[WARNING] Mining session finished !")