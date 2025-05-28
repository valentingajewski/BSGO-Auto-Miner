import keyboard
import time
import pyautogui

MINING_GUN1 = (2431,1231)
MINING_GUN2 = (2431,1281)

def moveToCursorCoords(coords):
    pyautogui.moveTo(coords, duration=0.1)
    pyautogui.click(button='left')


if __name__ == "__main__":
    time.sleep(3)
    moveToCursorCoords(MINING_GUN1)
    time.sleep(0.2)
    moveToCursorCoords(MINING_GUN2)




