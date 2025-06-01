import time
import json
import pyautogui
from player_status import status
from mining import moveToCursorCoords
from config import DND, CHAT_POSITION, COMBAT_LOG_POSITION_BUTTON

with open("config.json", "r") as f:
    config = json.load(f)

start_time = time.time()

mining_time = config["mining_time"]
sector_time = config["sector_time"]
selected_sector_ids = config["sectors"]

def starting_procedure():
    moveToCursorCoords(CHAT_POSITION, 'left')
    pyautogui.write(DND)
    time.sleep(2)
    moveToCursorCoords(COMBAT_LOG_POSITION_BUTTON)

if __name__ == "__main__":

    starting_procedure()

    while time.time() - start_time < mining_time *60:
        print(f'[INFO] Mining session started at: {start_time}')
        status(sector_time, selected_sector_ids)
    else:
        print("[INFO] Mining session finished")