# Libraries imports
import time
from datetime import datetime, timedelta
from termcolor import colored

# Class imports
from mining import Mining
from inbase import InBase
from sector import Sector
from combat import Combat

# Config/files imports
from bsgo_ai.pyautogui_lib import dnd, get_reward, launch_game
from bsgo_ai.config import (SECTOR_TEXT_POSITION, PS_MINING, PS_INBASE, PS_JUMP, LIST_TARGET_SECTOR,
                            INFO_PRINT_COLOR, WARNING_PRINT_COLOR, START_DELAY_MODE, START_DELAY_HOURS,
                            START_DELAY_DAYS, START_DELAY_DELAYED, START_DELAY_MINUTES)
from bsgo_ai.json_loader import (start_time, mining_sector_session_duration, mining_session_duration, 
                                 first_connection, GUI_CONFIG, start_delay)
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

def detect_if_in_right_sector(target_sector_id):
    sector_list = sector.extract_sector_from_wing()
    print(colored(f'[INFO] Sector: {sector_list}', INFO_PRINT_COLOR))
    is_good_sector = sector.check_sector(sector.ocr_check_sector(sector_list), target_sector_id)
    return is_good_sector

def detect_if_player_in_base():
    sector_list = extract_text(SECTOR_TEXT_POSITION)
    print(f"[DEBUG] sector_list: {sector_list}")
    return len(sector_list) == 0 or (len(sector_list[0]) <= 3 and len(sector_list[1]) <= 3)

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
        PLAYER_STATUS = player_status_detection(target_sector_id)
        print(colored(f"[DEBUG] Player Info Id: {PLAYER_STATUS}", INFO_PRINT_COLOR))
    elif PLAYER_STATUS == PS_JUMP:
        sector_list = []
        current_player_sector = None

        while not sector_list or current_player_sector is None:
            sector_list = sector.extract_sector_from_wing()
            current_player_sector = sector.ocr_check_sector(sector_list)
            
            if not sector_list or current_player_sector is None:
                print(colored("[WARNING] Sector not recognized, retrying...", WARNING_PRINT_COLOR))
                time.sleep(2)

        PLAYER_STATUS = sector.jump_shortest_path(sector_list, target_sector_id)

if __name__ == "__main__":

    if start_delay[START_DELAY_MODE] == START_DELAY_DELAYED:
        days = start_delay.get(START_DELAY_DAYS, 0)
        hours = start_delay.get(START_DELAY_HOURS, 0)
        minutes = start_delay.get(START_DELAY_MINUTES, 0)
        total_seconds = (days * 24 * 3600) + (hours * 3600) + (minutes * 60)

        start_time_gui = datetime.now() + timedelta(seconds=total_seconds)
        formatted_time = start_time_gui.strftime("%Y-%m-%d %H:%M:%S")

        print(colored(f"[INFO] Delayed start activated: mining will begin in {days}d {hours}h {minutes}min.", "grey"))
        print(colored(f"[INFO] Scheduled start time: {formatted_time}", "grey"))

        time.sleep(total_seconds)
    else:
        print(colored("[INFO] Immediate start.", "grey"))

    launch_game()

    if first_connection is True:
        time.sleep(1)
        get_reward()
        time.sleep(1)

    dnd()

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

        if PLAYER_STATUS == PS_MINING and sector_start_time == 0:
            sector_start_time = time.time()
    print(colored("[WARNING] Mining session finished !",WARNING_PRINT_COLOR))
    quit()