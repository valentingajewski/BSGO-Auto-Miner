import pyautogui
import time
from bsgo_ai.config import CANCEL_TARGET, TURN_LEFT, ENABLE_ALL_GUNS, POST_COMBUSTION, PITCH_UP

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