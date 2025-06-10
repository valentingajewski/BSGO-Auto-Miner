import os
import time
import random
import subprocess
from termcolor import colored
from config import INFO_PRINT_COLOR

random_wait_time = random.randint(1,10)*60

if __name__ == "__main__":

    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

    print(colored(f"[INFO] Waiting {int(random_wait_time/60)} minutes before launching game", INFO_PRINT_COLOR))
    time.sleep(random_wait_time)
    subprocess.Popen(["python", "D:/Dossiers perso/Programmation/BSGO_AutoMiner/bsgo_ai/status/main.py"])