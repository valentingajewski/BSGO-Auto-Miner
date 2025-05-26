import pyautogui

def scan_asteroid(asteroid_list_temp):
    for asteroid in asteroid_list_temp:
        # Click on nearest asteroid
        pyautogui.moveTo(asteroid['x'], asteroid['y'])
        pyautogui.click()

        from bsgo_ai.detectors.ocr_utils import extract_text
        distance_text = extract_text((1700, 200, 120, 50))
        try:
            distance = int(''.join(filter(str.isdigit, distance_text)))
        except ValueError:
            continue

        if distance <= 2000:
            from bsgo_ai.actions.keyboard_control import scanning
            scanning()
            # TODO: Lire le résultat du scan avec OCR ici
            scanned_resource = "WATER"  # À remplacer par analyse OCR réelle
            if scanned_resource == "WATER":  # ou selon le scan_choice
                print("Astéroïde détecté, démarrage du minage")
                # TODO: implémenter shoot_asteroid()
                asteroid_list_temp.clear()
                break
            else:
                asteroid_list_temp.remove(asteroid)

def mining(status, scan_choice):
    asteroid_list_temp = []
    from bsgo_ai.detectors.asteroid_detector import detect_asteroid

    for _ in range(5):
        asteroid = detect_asteroid()
        if asteroid:
            from bsgo_ai.detectors.ocr_utils import extract_text
            distance_text = extract_text((1700, 200, 120, 50))
            try:
                distance = int(''.join(filter(str.isdigit, distance_text)))
            except ValueError:
                distance = 99999

            asteroid['distance'] = distance
            asteroid_list_temp.append(asteroid)

    # Supprimer doublons
    asteroid_list_temp = [dict(t) for t in {tuple(d.items()) for d in asteroid_list_temp}]

    while status == "Mining":
        scan_asteroid(asteroid_list_temp)