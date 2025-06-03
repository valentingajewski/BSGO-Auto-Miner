import time
from bsgo_ai.config import (REPAIR_BUTTON, REPAIR_MENU_BUTTON, REPAIR_VALIDATION_BUTTON, UNDOCK_BUTTON, CLOSE_BUTTON,
                    DRADIS_SELECT_TARGET_BUTTON, DRADIS_CLOSE_BUTTON, DRADIS_MENU_BUTTON, DRADIS_TARGET_BUTTON)
from bsgo_ai.pyautogui_lib import moveToCursorCoords


class InBase():

    def repair(self):
        time.sleep(10)
        print("[ACTION] Repairing the ship")
        moveToCursorCoords(REPAIR_MENU_BUTTON, 'left')
        time.sleep(1)
        moveToCursorCoords(REPAIR_BUTTON, 'left')
        time.sleep(1)
        moveToCursorCoords(REPAIR_VALIDATION_BUTTON, 'left')
        time.sleep(1)
        moveToCursorCoords(CLOSE_BUTTON, 'left')
        time.sleep(25)

    def undock(self):
        print("[ACTION] Undocking")
        moveToCursorCoords(UNDOCK_BUTTON, 'left')
        time.sleep(10)

    def dradis(self):
        time.sleep(5)
        moveToCursorCoords(DRADIS_MENU_BUTTON, 'left')
        time.sleep(0.5)
        moveToCursorCoords(DRADIS_TARGET_BUTTON, 'left')
        time.sleep(0.5)
        moveToCursorCoords(DRADIS_SELECT_TARGET_BUTTON, 'left')
        time.sleep(5)
        moveToCursorCoords(DRADIS_CLOSE_BUTTON, 'left')
        time.sleep(0.5)
