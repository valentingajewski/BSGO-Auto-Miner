import torch
import pyautogui
import numpy as np
import cv2
import sys
import time
from pathlib import Path
from text_from_image import extract_distance_to_asteroid


ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

from bsgo_ai.config import ASTEROID_TO_DETECT, DISTANCE_RECTANGLE_TEXT

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
    list_asteroid_temp = []
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
        count = 0
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

                list_asteroid_temp.append((center_x, center_y, distance_asteroid))
                print(f"Astéroïde détecté : {label} à ({center_x}, {center_y}), distance : {distance_asteroid}, confiance : {conf:.2f}")

                count += 1
                time.sleep(1)

                if count >= ASTEROID_TO_DETECT:
                    break

    if not list_asteroid_temp:
        print("Aucun astéroïde détecté.")
    else:
        print(f"Total astéroïdes détectés : {len(list_asteroid_temp)}")

    return list_asteroid_temp

if __name__ == "__main__":
    detect_asteroid()
