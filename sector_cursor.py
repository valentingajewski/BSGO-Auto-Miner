import json
import threading
import tkinter as tk
from tkinter import simpledialog, messagebox
from pynput import mouse, keyboard
import os

# Nom du fichier de sauvegarde
DATA_FILE = 'secteurs.json'

# Fonction pour charger les données existantes (s'il y en a)
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

class SectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sector Logger")
        self.root.attributes("-topmost", True)  # Toujours au premier plan
        self.running = False

        self.start_button = tk.Button(root, text="Start", command=self.start_listening)
        self.start_button.pack(padx=20, pady=10)

        self.coord_label = tk.Label(root, text="")
        self.coord_label.pack(padx=20, pady=10)

        self.listener_thread = None
        self.data = load_data()

    def start_listening(self):
        if not self.running:
            self.running = True
            self.listener_thread = threading.Thread(target=self.run_keyboard_listener, daemon=True)
            self.listener_thread.start()
            self.start_button.config(state=tk.DISABLED)

    def run_keyboard_listener(self):
        with keyboard.Listener(on_press=self.on_key_press) as listener:
            listener.join()

    def on_key_press(self, key):
        if self.running:
            try:
                if key.char == 'j':
                    x, y = self.root.winfo_pointerx(), self.root.winfo_pointery()
                    self.root.after(0, lambda: self.update_and_prompt(x, y))
            except AttributeError:
                pass

    def update_and_prompt(self, x, y):
        self.coord_label.config(text=f"Coordonnées : ({x}, {y})")
        self.prompt_for_sector(x, y)

    def prompt_for_sector(self, x, y):
        # Créer une fenêtre temporaire au premier plan pour le prompt
        popup = tk.Toplevel(self.root)
        popup.attributes("-topmost", True)
        popup.grab_set()  # Forcer l'interaction avec la fenêtre
        name = simpledialog.askstring("Nom du Secteur", f"Entrez le nom du secteur pour les coordonnées ({x}, {y}) :", parent=popup)
        popup.grab_release()
        popup.destroy()

        if name:
            self.data.append({"name": name, "x": x, "y": y})
            save_data(self.data)

# Lancer l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = SectorApp(root)
    root.mainloop()
