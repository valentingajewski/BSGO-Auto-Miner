from bsgo_ai.detectors.asteroid_detector import detect_asteroid
import time, pyautogui

allowed_resources = ["WATER", "TITANIUM", "TYLIUM", "UNKNOWN"]

print("[TEST] Surveillance en cours (Ctrl+C pour arrêter)")
def test():
    try:
        while True:
            result = detect_asteroid()

            if result:
                print(f"\n[✅] Astéroïde détecté !")
                print(f"  - Position : ({result['x']}, {result['y']})")
                print(f"  - Type     : {result['class']}")
                print(f"  - Confiance: {result['confidence']:.2f}")
                pyautogui.moveTo(result['x'], result['y'], duration=0.1)
                pyautogui.click()
            else:
                print(".", end="", flush=True)

            time.sleep(3)

    except KeyboardInterrupt:
        print("\n[🛑] Arrêt manuel.")
