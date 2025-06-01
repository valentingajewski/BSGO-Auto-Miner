# Librairies imports
import pathlib as Path
import sys
import signal
import time
import json
import pyautogui

# Class imports
from mining import Mining
from inbase import InBase
from sector import Sector
from combat import Combat

# Config/files imports
from bsgo_ai.config import (COMBAT_LOG_ZONE, SECTOR_TEXT_POSITION, PS_MINING, PS_IN_COMBAT, PS_INBASE, PS_JUMP, PS_KILLED, 
                    LIST_TARGET_SECTOR, WING_PLAYER_LOCATION_ZONE, WING_WINDOW)
from bsgo_ai.json_loader import start_time, mining_sector_session_duration, mining_session_duration, list_target_sectors, GUI_CONFIG
from bsgo_ai.detectors.text_from_image import extract_text

current_sector = 0
sector_start_time = time.time()
target_sector_id = GUI_CONFIG[LIST_TARGET_SECTOR][current_sector]

# Class instances
mining = Mining()
inbase = InBase()
sector = Sector()
combat = Combat()


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
    pyautogui.press(WING_WINDOW)
    time.sleep(1)
    sector_list = extract_text(WING_PLAYER_LOCATION_ZONE)
    print(f'[INFO] Sector: {sector_list}')
    is_good_sector = sector.check_sector(sector.ocr_check_sector(sector_list), target_sector_id)
    pyautogui.press(WING_WINDOW)
    return is_good_sector

def detect_if_player_in_base():
    sector_list = extract_text(SECTOR_TEXT_POSITION)
    print(f'[DEBUG] sector : {sector_list}, length {len(sector_list)}')
    return len(sector_list) == 0 or len(sector_list[0]) <= 3

def player_status_detection(target_sector_id):
    combat_log = detect_if_damage_to_player(extract_text(COMBAT_LOG_ZONE))
    if combat_log >= 2:
        PLAYER_STATUS = PS_IN_COMBAT
    if detect_if_player_is_killed(COMBAT_LOG_ZONE):
        PLAYER_STATUS = PS_KILLED
    if detect_if_player_in_base is True:
        PLAYER_STATUS = PS_INBASE
    if detect_if_in_right_sector(target_sector_id) is False:
        PLAYER_STATUS = PS_JUMP
    else:
        PLAYER_STATUS = PS_MINING
    print(f'[INFO] Player Status: {PLAYER_STATUS}')
    return PLAYER_STATUS

def status(sector_time):
    global PLAYER_STATUS
    global sector_start_time
    global current_sector
    print(PLAYER_STATUS)
    if PLAYER_STATUS == PS_MINING:
        PLAYER_STATUS = mining.mining_status(sector_time)
    elif PLAYER_STATUS == PS_IN_COMBAT:
        PLAYER_STATUS = combat.combat()
    elif PLAYER_STATUS == PS_KILLED:
        PLAYER_STATUS = combat.killed_procedure()
    elif PLAYER_STATUS == PS_INBASE: 
        inbase.repair()
        PLAYER_STATUS = inbase.undock(target_sector_id)
    elif PLAYER_STATUS == PS_JUMP:
        current_sector += 1
        PLAYER_STATUS = sector.jump(GUI_CONFIG[LIST_TARGET_SECTOR][current_sector])
        sector_start_time = time.time()
    else:
        print(PLAYER_STATUS)
    print(PLAYER_STATUS)
    print(f'[INFO] Checking status: {PLAYER_STATUS}')

PLAYER_STATUS = player_status_detection(target_sector_id)
if detect_if_player_in_base() is True:
    PLAYER_STATUS = PS_INBASE
else:
    if detect_if_in_right_sector(GUI_CONFIG[LIST_TARGET_SECTOR][current_sector]) is False:
        sector.jump(GUI_CONFIG[LIST_TARGET_SECTOR][current_sector])

while time.time() - start_time < mining_session_duration :
    if time.time() - sector_start_time > mining_sector_session_duration:
        PLAYER_STATUS = PS_JUMP

    status(mining_sector_session_duration)
    PLAYER_STATUS = player_status_detection(target_sector_id)