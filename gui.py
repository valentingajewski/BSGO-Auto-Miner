import tkinter as tk
from threading import Thread
from bsgo_ai.detectors.asteroid_detector import detect_asteroid

def start_detection():
    # Lancer la détection dans un thread pour ne pas bloquer l'interface
    Thread(target=detect_asteroid, daemon=True).start()

# Création de la fenêtre principale
root = tk.Tk()
root.title("BSGO AutoMiner")
root.geometry("300x150")
root.resizable(False, False)

# Titre
label = tk.Label(root, text="AutoMiner - Détection d'astéroïdes", font=("Arial", 12))
label.pack(pady=20)

# Bouton Start
start_button = tk.Button(root, text="Start", command=start_detection, font=("Arial", 11), bg="green", fg="white")
start_button.pack(pady=10)

# Boucle principale
def run():
    root.mainloop()

if __name__ == "__main__":
    run()
