import keyboard
import time
import pyautogui

MINING_GUN1 = (2431,1231)
MINING_GUN2 = (2431,1281)
coords_test = (1960,470)
SCAN = '&'


def moveToCursorCoords(coords, side):
    pyautogui.moveTo(coords, duration=0.1)
    pyautogui.click(button=side)

def scan_asteroid(coords, key):
    moveToCursorCoords(coords, 'left')
    pyautogui.press(key)


if __name__ == "__main__":
    time.sleep(3)
    scan_asteroid(coords_test, SCAN)




