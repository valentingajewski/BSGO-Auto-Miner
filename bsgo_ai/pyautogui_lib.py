import pyautogui
import time
from bsgo_ai.config import (CANCEL_TARGET, TURN_LEFT, ENABLE_ALL_GUNS, POST_COMBUSTION, PITCH_UP, 
                            CHAT_POSITION, DND, MINING_GUN1, MINING_GUN2, ALIGN_SHIP_TO_HORIZON)

def turning_rotation(ship_turning_speed):
    return (360 / ship_turning_speed) / 4.0

def turning_ship(ship_turning_speed):
    print("[ACTION] Ship turning...")
    pyautogui.press(CANCEL_TARGET)
    pyautogui.keyDown(TURN_LEFT)
    time.sleep(turning_rotation(ship_turning_speed))
    pyautogui.keyUp(TURN_LEFT)
    
def combat_procedure():
    pyautogui.press(ENABLE_ALL_GUNS)
    pyautogui.press(POST_COMBUSTION)
    pyautogui.keyDown(TURN_LEFT)
    pyautogui.keyDown(PITCH_UP)
    time.sleep(20)
    pyautogui.keyUp(TURN_LEFT)
    pyautogui.keyUp(PITCH_UP)

def moveToCursorCoords(coords, side):
    pyautogui.moveTo(coords, duration=0.1)
    pyautogui.click(button=side)

def starting_procedure():
    moveToCursorCoords(CHAT_POSITION, 'left')
    time.sleep(0.5)
    pyautogui.write(DND)
    time.sleep(2)

def activate_mining_guns():
    moveToCursorCoords(MINING_GUN1, 'left')
    time.sleep(0.2)
    moveToCursorCoords(MINING_GUN2, 'left')

def turn_and_shoot_asteroid():
    pyautogui.keyDown(TURN_LEFT)
    time.sleep(1)
    pyautogui.keyUp(TURN_LEFT)
    activate_mining_guns()
    pyautogui.press(ALIGN_SHIP_TO_HORIZON)
    print("[INFO] Asteroid approach finished")
    time.sleep(20)
    activate_mining_guns()

def pc_approach(hold_time):
    pyautogui.press(POST_COMBUSTION)
    time.sleep(hold_time)
    pyautogui.press(POST_COMBUSTION)