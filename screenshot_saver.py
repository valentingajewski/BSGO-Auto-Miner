import time
import os
import pyautogui

# === PARAMÈTRES À CONFIGURER ===
nom_secteur = "serpentos"             # Nom du secteur (ex: Pallas, Canceron, etc.)
intervalle = 5                     # Temps entre chaque screenshot (en secondes)
dossier_sortie = "D:\Dossiers perso\Programmation\BSGO_sector_images"     # Dossier de destination
nombre_max_captures = 100          # Nombre de screenshots avant arrêt (ou utilise Ctrl+C pour l'arrêter)

# === CRÉATION DU DOSSIER SI NÉCESSAIRE ===
if not os.path.exists(dossier_sortie):
    os.makedirs(dossier_sortie)

# === DÉBUT DE LA BOUCLE DE CAPTURE ===
compteur = 1
try:
    print(f"Démarrage de la capture d'écran toutes les {intervalle} secondes dans le secteur '{nom_secteur}'.")
    while compteur <= nombre_max_captures:
        nom_fichier = f"{nom_secteur}_{compteur:03d}.jpg"
        chemin_fichier = os.path.join(dossier_sortie, nom_fichier)
        
        screenshot = pyautogui.screenshot()
        screenshot.save(chemin_fichier)
        
        print(f"[{time.strftime('%H:%M:%S')}] Capture enregistrée : {chemin_fichier}")
        compteur += 1
        time.sleep(intervalle)

    print("Capture terminée.")
except KeyboardInterrupt:
    print("\nCapture arrêtée manuellement par l'utilisateur.")
