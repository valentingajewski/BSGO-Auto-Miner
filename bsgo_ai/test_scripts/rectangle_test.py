import pyautogui
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Capture d'écran complète
screenshot = pyautogui.screenshot()
frame = np.array(screenshot)
frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

# Dessin du rectangle
x, y, w, h = 1140, 117, 280, 30
cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

# Affichage
plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
plt.title("Zone OCR")
plt.axis("off")
plt.show()



