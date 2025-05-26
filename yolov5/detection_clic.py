import torch
import pyautogui
import numpy as np
import cv2
import time

from models.experimental import attempt_load
from utils.general import non_max_suppression

# Charger le modèle YOLOv5 entraîné
model_path = 'yolov5/runs/train/asteroid_detector/weights/best.pt'
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = attempt_load(model_path, device=device)
model.eval()

# Liste des classes (dans l'ordre d'entraînement)
class_names = [
    'asteroid',
    'asteroid_no_resource',
    'asteroid_titanium',
    'asteroid_tylium',
    'asteroid_water',
    'planetoid'
]

print("Modèle chargé. Début de la détection…")

while True:
    # 1. Capture d'écran
    screenshot = pyautogui.screenshot()
    frame = np.array(screenshot)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # 2. Prétraitement image pour YOLO
    img = cv2.resize(frame, (640, 640))  # Redimensionne pour le modèle
    img_tensor = torch.from_numpy(img).to(device).permute(2, 0, 1).float() / 255.0
    if img_tensor.ndimension() == 3:
        img_tensor = img_tensor.unsqueeze(0)

    # 3. Inference
    with torch.no_grad():
        pred = model(img_tensor)[0]
        detections = non_max_suppression(pred, conf_thres=0.5, iou_thres=0.45)[0]

    found = False
    if detections is not None and len(detections):
        for *box, conf, cls in detections:
            class_id = int(cls.item())
            label = class_names[class_id]

            if "asteroid" in label:
                x1, y1, x2, y2 = map(int, box)
                # Adapter les coordonnées à la résolution de ton écran
                screen_w, screen_h = pyautogui.size()
                scale_x = screen_w / 640
                scale_y = screen_h / 640
                center_x = int((x1 + x2) / 2 * scale_x)
                center_y = int((y1 + y2) / 2 * scale_y)

                print(f"Astéroïde détecté : {label} à ({center_x}, {center_y}), confiance : {conf:.2f}")
                pyautogui.moveTo(center_x, center_y, duration=0.1)
                pyautogui.click()
                found = True
                break

    if not found:
        print("Aucun astéroïde détecté.")

    time.sleep(1.5)
