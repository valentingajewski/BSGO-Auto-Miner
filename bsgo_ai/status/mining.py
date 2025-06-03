import torch
import math
import pyautogui
import numpy as np
import cv2
import sys
import time
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

from bsgo_ai.pyautogui_lib import turning_ship, moveToCursorCoords, turn_and_shoot_asteroid, pc_approach
from bsgo_ai.detectors.text_from_image import extract_distance_to_asteroid, extract_text
from bsgo_ai.config import (ASTEROID_TO_DETECT, DISTANCE_RECTANGLE_TEXT, SCAN, MINERAL_ANALYSIS_TEXT_ZONE,
                            SHIP_TURNING_SPEED, PS_MINING, SHIP_VMAX, SHIP_PC_ACCELERATION,
                            TARGET_CURSOR_COORDS, CANCEL_TARGET)

YOLOV5_PATH = Path(__file__).resolve().parents[2] / "yolov5"
MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "best.pt"
sys.path.append(str(YOLOV5_PATH))

from models.experimental import attempt_load
from utils.general import non_max_suppression
from utils.torch_utils import select_device

device = select_device('')
model = attempt_load(str(MODEL_PATH), device=device)
model.eval()

class_names = [
    'asteroid',
    'asteroid_no_resource',
    'asteroid_titanium',
    'asteroid_tylium',
    'asteroid_water',
    'planetoid',
    'platform'
]

class Mining():

    def detect_asteroid(self):
        screenshot = pyautogui.screenshot()
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        img = cv2.resize(frame, (640, 640))
        img = img / 255.0
        img = img.transpose(2, 0, 1)
        img = np.ascontiguousarray(img)
        img_tensor = torch.from_numpy(img).float().unsqueeze(0).to(device)

        with torch.no_grad():
            pred = model(img_tensor)[0]
            detections = non_max_suppression(pred, conf_thres=0.5, iou_thres=0.45)[0]

        if detections is not None and len(detections):
            screen_w, screen_h = pyautogui.size()
            scale_x = screen_w / 640
            scale_y = screen_h / 640

            for *box, conf, cls in detections:
                class_id = int(cls.item())
                label = class_names[class_id]

                if label == 'asteroid':
                    x1, y1, x2, y2 = map(int, box)
                    center_x = int((x1 + x2) / 2 * scale_x)
                    center_y = int((y1 + y2) / 2 * scale_y)
                    moveToCursorCoords((center_x, center_y), 'left')

                    try:
                        distance_asteroid = extract_distance_to_asteroid(DISTANCE_RECTANGLE_TEXT)
                    except Exception as e:
                        print(f"[WARNING] Failed to extract distance. Defaulting to 3000. Reason: {e}")
                        distance_asteroid = 3001

                    print(f"Asteroid detected : {label} at ({center_x}, {center_y}), distance : {distance_asteroid}, trust : {conf:.2f}")

                    return (center_x, center_y, distance_asteroid)

        print("No asteroid detected")
        return None

    def detect_nearest_asteroid(self, list_asteroid_temp):
        nearest_coords = None
        nearest_distance = float('inf')

        for i, item in enumerate(list_asteroid_temp):
            if not isinstance(item, (tuple, list)):
                continue
            if len(item) != 3:
                continue

            x, y, distance = item

            if distance is not None and distance < nearest_distance:
                nearest_distance = distance
                nearest_coords = (x, y)

        print(f"[INFO] Nearest asteroid : {nearest_coords}, distance : {nearest_distance}")

        return nearest_coords, nearest_distance

    def scan_asteroid(self, coords, scan_key):
        moveToCursorCoords(coords, 'left')
        pyautogui.press(scan_key)
        time.sleep(5.5)
        return extract_text(MINERAL_ANALYSIS_TEXT_ZONE)
    
    def pc_time(self, distance):
        if distance <= 700:
            return 0.0

        adjusted_distance = max(0, distance - 700)
        v_max = SHIP_VMAX
        acceleration = SHIP_PC_ACCELERATION

        if acceleration <= 0 or adjusted_distance <= 0:
            return float('inf')  # Cas non physique ou déjà arrivé

        d_accel = (v_max ** 2) / (2 * acceleration)

        if adjusted_distance > d_accel:
            t1 = v_max / acceleration
            d2 = adjusted_distance - d_accel
            t2 = d2 / v_max
            return t1 + t2
        else:
            return math.sqrt(2 * adjusted_distance / acceleration)

    def approach_water_asteroid(self, coords, distance):
        x, y = coords
        duration = self.pc_time(distance)
        if duration == float('inf'):
            print("Temps de parcours invalide.")
            return
        print(f"[ACTION] Approaching asteroid, estimated arrival in: {duration:.2f}s")
        print(f"[INFO] Right clicking on coordinates: {x,y}")
        moveToCursorCoords((TARGET_CURSOR_COORDS),'right')
        time.sleep(0.2)
        hold_time = max(0, duration)
        if hold_time > 0:
            pc_approach(hold_time)
        else:
            time.sleep(3)
            print("[INFO] Asteroid is close. No thrust needeed")

        turn_and_shoot_asteroid()


    def approach_nearest_asteroid(self, coords, distance):
        time.sleep(3)

        x, y = coords
        duration = self.pc_time(distance)

        if duration == float('inf'):
            print("Temps de parcours invalide.")
            return

        print(f"[ACTION] Approaching asteroid, estimated arrival in: {duration:.2f}s")

        print(f"[DEBUG] Right clicking on coordinates: {x,y}")
        moveToCursorCoords((TARGET_CURSOR_COORDS),'right')
        time.sleep(0.2)
        pyautogui.press(CANCEL_TARGET)

        hold_time = max(0, duration)
        if hold_time > 0:
            pc_approach(hold_time)
        else:
            print("[INFO] Asteroid is close. No thrust needeed")

    def mining_status(self, sector_time, target_sector_id, start_time=None, full_rotation=0):
        ship_turning_speed = SHIP_TURNING_SPEED
        PLAYER_STATUS = PS_MINING

        if start_time is None:
            start_time = time.time()

        if (full_rotation >= 4 or time.time() - start_time > sector_time) or PLAYER_STATUS != PS_MINING:
            print(f"[INFO] No valuable asteroids detected after {full_rotation} full rotations.")

            asteroid_list = [res for _ in range(ASTEROID_TO_DETECT) if (res := self.detect_asteroid()) is not None]

            if asteroid_list:
                coords, distance = self.detect_nearest_asteroid(asteroid_list)
                self.approach_nearest_asteroid(coords, distance)
                time.sleep(3)
                x, y = coords
                duration = self.pc_time(distance)
                if duration == float('inf'):
                    print("Invalid travel time.")
                    return

                print(f"[ACTION] Final approach in {duration:.2f} seconds")
                moveToCursorCoords(TARGET_CURSOR_COORDS, 'right')
                time.sleep(0.2)
                pyautogui.press(CANCEL_TARGET)
            return

        # Process detection attempts without while loop
        def process_attempts(attempts=0):
            if attempts >= ASTEROID_TO_DETECT:
                print("[ACTION] Rotating ship by 1/4 turn...")
                turning_ship(ship_turning_speed)
                time.sleep(5)
                return self.mining_status(sector_time, target_sector_id, start_time, full_rotation + 1)


            result = self.detect_asteroid()
            if result is None:
                return process_attempts(attempts + 1)

            x, y, distance = result
            if distance is None or distance > 3000:
                print(f"[INFO] Asteroid too far: {distance}")
                return process_attempts(attempts + 1)

            coords = (x, y)
            print(f"[INFO] Scanning asteroid at {coords}, distance: {distance}")
            mineral_result = self.scan_asteroid(coords, SCAN)
            print(f"[DEBUG] mineral_result: {mineral_result}")

            for element in mineral_result:
                if "WATER" in element.upper():
                    print("[INFO] WATER resource detected, initiating approach...")
                    self.approach_water_asteroid(coords, distance)
                    return self.mining_status(sector_time, target_sector_id, start_time, full_rotation)
                else:
                    print("[INFO] Unwanted resource, moving to next attempt...")
                    return process_attempts(attempts + 1)

        process_attempts()

