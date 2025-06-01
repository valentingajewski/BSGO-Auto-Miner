import time
from bsgo_ai.pyautogui_lib import combat_procedure, moveToCursorCoords
from bsgo_ai.config import RESPAWN_BUTTON, PS_INBASE, ENABLE_ALL_GUNS, POST_COMBUSTION, PITCH_DOWN, PITCH_UP, TURN_LEFT

class Combat():

    def combat():
        from player_status import PLAYER_STATUS
        combat_procedure()
        return PLAYER_STATUS

    def killed_procedure():
        time.sleep(10)
        moveToCursorCoords(RESPAWN_BUTTON, 'left')
        time.sleep(10)
        return PS_INBASE