import torch
import pyautogui
import numpy as np
import cv2
import sys
import time
from pathlib import Path
from text_from_image import extract_distance_to_asteroid, extract_text

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

from bsgo_ai.config import ASTEROID_TO_DETECT, DISTANCE_RECTANGLE_TEXT, SCAN, MINERAL_ANALYSIS_TEXT_ZONE
from bsgo_ai.actions.mining import approach_nearest_asteroid, moveToCursorCoords

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
    'planetoid'
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

            if "asteroid" in label:
                x1, y1, x2, y2 = map(int, box)
                center_x = int((x1 + x2) / 2 * scale_x)
                center_y = int((y1 + y2) / 2 * scale_y)
                pyautogui.moveTo(center_x, center_y, duration=0.1)
                pyautogui.click()
                distance_asteroid = extract_distance_to_asteroid(DISTANCE_RECTANGLE_TEXT)

                print(f"Astéroïde détecté : {label} à ({center_x}, {center_y}), distance : {distance_asteroid}, confiance : {conf:.2f}")

                return (center_x, center_y, distance_asteroid)

    print("Aucun astéroïde détecté.")
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

    print(f"Nearest asteroid : {nearest_coords}, distance : {nearest_distance}")

    return nearest_coords, nearest_distance

def scan_asteroid(coords, scan_key):
    moveToCursorCoords(coords, 'left')
    pyautogui.press(scan_key)
    time.sleep(5.5)
    return extract_text(MINERAL_ANALYSIS_TEXT_ZONE)

if __name__ == "__main__":
    attempts = 0
    max_attempts = ASTEROID_TO_DETECT

    while attempts < max_attempts:
        result = detect_asteroid()

        if result is None:
            attempts += 1
            continue

        x, y, distance = result

        if distance is None or distance > 3000:
            print(f"Astéroïde ignoré (distance trop grande) : {distance}")
            attempts += 1
            continue

        coords = (x, y)
        print(f"Scan de l'astéroïde à {coords}, distance : {distance}")
        mineral_result = scan_asteroid(coords, SCAN)
        time.sleep(1)

        if "WATER" in mineral_result.upper():
            print("Ressource WATER détectée, approche en cours...")
            approach_nearest_asteroid(coords, distance)
            break
        else:
            print("Ressource non intéressante, tentative suivante...")
            attempts += 1

    if attempts >= max_attempts:
        print("Scan des astéroïdes terminé. Aucun WATER trouvé.")