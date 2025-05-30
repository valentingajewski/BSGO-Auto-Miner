import time
import pyautogui
from mining import moveToCursorCoords
from config import RESPAWN_BUTTON, PS_INBASE, ENABLE_ALL_GUNS, POST_COMBUSTION, PITCH_DOWN, PITCH_UP, TURN_LEFT

def combat():
    from player_status import PLAYER_STATUS
    pyautogui.press(ENABLE_ALL_GUNS)
    pyautogui.press(POST_COMBUSTION)
    pyautogui.keyDown(TURN_LEFT)
    pyautogui.keyDown(PITCH_UP)
    time.sleep(20)
    pyautogui.keyUp(TURN_LEFT)
    pyautogui.keyUp(PITCH_UP)
    return PLAYER_STATUS

if __name__ == '__main__':
    time.sleep(2)
    combat()
