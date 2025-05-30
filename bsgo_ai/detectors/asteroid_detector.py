import torch
import pyautogui
import numpy as np
import cv2
import sys
import time
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

from bsgo_ai.config import (ASTEROID_TO_DETECT, DISTANCE_RECTANGLE_TEXT, SCAN, MINERAL_ANALYSIS_TEXT_ZONE, SESSION_TIME,
                            SHIP_TURNING_SPEED, PS_MINING)
from bsgo_ai.mining import approach_water_asteroid, moveToCursorCoords, approach_nearest_asteroid
from bsgo_ai.detectors.text_from_image import extract_distance_to_asteroid, extract_mineral_analysis


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

def detect_asteroid():
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
                pyautogui.moveTo(center_x, center_y, duration=0.1)
                pyautogui.click()
                distance_asteroid = extract_distance_to_asteroid(DISTANCE_RECTANGLE_TEXT)

                print(f"Asteroid detected : {label} at ({center_x}, {center_y}), distance : {distance_asteroid}, trust : {conf:.2f}")

                return (center_x, center_y, distance_asteroid)

    print("No asteroid detected")
    return None

def detect_nearest_asteroid(list_asteroid_temp):
    nearest_coords = None
    nearest_distance = float('inf')

    for i, item in enumerate(list_asteroid_temp):
        if not isinstance(item, (tuple, list)):
            print(f"[ERREUR] Élement non-structuré : {item} (type: {type(item)})")
            continue
        if len(item) != 3:
            print(f"[ERREUR] Élement de longueur inattendue à l'index {i} : {item}")
            continue

        x, y, distance = item

        if distance is not None and distance < nearest_distance:
            nearest_distance = distance
            nearest_coords = (x, y)

    print(f"[INFO] Nearest asteroid : {nearest_coords}, distance : {nearest_distance}")

    return nearest_coords, nearest_distance

def scan_asteroid(coords, scan_key):
    moveToCursorCoords(coords, 'left')
    pyautogui.press(scan_key)
    time.sleep(5.5)
    return extract_mineral_analysis(MINERAL_ANALYSIS_TEXT_ZONE)

def turning_rotation(ship_turning_speed):
    return (360 / ship_turning_speed) / 4.0

def mining_status(start_time=None, max_duration=None):
    from player_status import player_status_detection
    full_rotation = 0
    max_quarters = 4
    ship_turning_speed = SHIP_TURNING_SPEED
    PLAYER_STATUS = PS_MINING

    if start_time is None:
        start_time = time.time()
    if max_duration is None:
        max_duration = SESSION_TIME*60

    while (full_rotation < max_quarters and time.time() - start_time < max_duration) and PLAYER_STATUS == PS_MINING:
        attempts = 0
        while attempts < ASTEROID_TO_DETECT and PLAYER_STATUS == PS_MINING:
            result = detect_asteroid()
            if result is None:
                attempts += 1
                continue

            x, y, distance = result

            if distance is None or distance > 3000:
                print(f"[INFO] Asteroid too far: {distance}")
                attempts += 1
                continue

            coords = (x, y)
            print(f"[INFO] Scanning asteroid. Distance : {distance}")
            mineral_result = scan_asteroid(coords, SCAN)

            if "WATER" in mineral_result.upper():
                print("[INFO] Asteroid water detected. Approaching...")
                approach_water_asteroid(coords, distance)
                return mining_status(start_time, max_duration)
            else:
                print("[INFO] No useful resources, to the next one...")
                attempts += 1

        else:
            print("[ACTION] Ship turning...")
            pyautogui.press('c')
            pyautogui.keyDown('q')
            time.sleep(turning_rotation(ship_turning_speed))
            pyautogui.keyUp('q')
            full_rotation += 1
            time.sleep(5)

    print("Recherche terminée : Aucun astéroïde WATER trouvé après un tour complet ou durée dépassée.")
    print("Détection finale : approche de l'astéroïde le plus proche...")
    asteroid_list = []
    for _ in range(ASTEROID_TO_DETECT):
        result = detect_asteroid()
        if result is not None:
            asteroid_list.append(result)
    if asteroid_list:
        coords, distance = detect_nearest_asteroid(asteroid_list)
        approach_nearest_asteroid(coords, distance)
        PLAYER_STATUS = player_status_detection()
    return PLAYER_STATUS
