import json, time

from bsgo_ai.config import (MINING_TIME, SECTOR_TIME, LIST_TARGET_SECTOR, TIME_MULTIPLICATOR, SECTORS_JSON_PATH, 
                            GUI_CONFIG_JSON_PATH, FIRST_CONNECTION, START_DELAY, START_DELAY_MODE, START_DELAY_NOW)

# JSON loader
with open(GUI_CONFIG_JSON_PATH, 'r') as f:
    GUI_CONFIG = json.load(f)

with open(SECTORS_JSON_PATH, "r") as f:
    sectors = json.load(f)

# Variable Initialization
start_time = time.time()
mining_session_duration = GUI_CONFIG[MINING_TIME] * TIME_MULTIPLICATOR
mining_sector_session_duration = GUI_CONFIG[SECTOR_TIME] * TIME_MULTIPLICATOR
list_target_sectors = GUI_CONFIG[LIST_TARGET_SECTOR]
first_connection = GUI_CONFIG[FIRST_CONNECTION]
start_delay = GUI_CONFIG.get(START_DELAY, {START_DELAY_MODE: START_DELAY_NOW})