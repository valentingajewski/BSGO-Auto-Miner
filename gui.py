import tkinter as tk
from tkinter import messagebox
import json
import threading
import time
import subprocess
import psutil
import os
import sys
import pyautogui
from bsgo_ai.actions.mining import mining, scan_asteroid

# Charger les secteurs
with open("assets/sectors_map.json", "r") as f:
    sectors_data = json.load(f)
sector_names = list(sectors_data.keys())

# Fenêtre
root = tk.Tk()
root.title("BSGO AutoMining")

# Variables
session_duration_var = tk.StringVar(value="30")
jump_range_var = tk.StringVar(value="3")
resources_vars = {r: tk.BooleanVar() for r in ["WATER", "TITANIUM", "TYLIUM"]}
timer_label_var = tk.StringVar(value="00:00")
stop_timer = False
sectors_listbox = None

def save_config():
    selected_resources = [r for r, v in resources_vars.items() if v.get()]
    selected_sectors = [sectors_listbox.get(i) for i in sectors_listbox.curselection()]
    try:
        config = {
            "session_duration": int(session_duration_var.get()) * 60,
            "resources": selected_resources,
            "sectors": selected_sectors,
            "jump_range": int(jump_range_var.get())
        }
    except ValueError:
        messagebox.showerror("Erreur", "Valeurs invalides.")
        return

    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)

    messagebox.showinfo("OK", "Configuration enregistrée ✅")

def countdown(duration):
    global stop_timer
    start = time.time()
    while not stop_timer:
        elapsed = int(time.time() - start)
        remaining = max(0, duration - elapsed)
        mins, secs = divmod(remaining, 60)
        timer_label_var.set(f"{mins:02d}:{secs:02d}")
        if remaining == 0:
            break
        time.sleep(1)

def launch_bot():
    subprocess.Popen(["python", "main.py"], creationflags=subprocess.CREATE_NEW_CONSOLE)

def start_automining():
    save_config()
    with open("config.json", "r") as f:
        config = json.load(f)

    global stop_timer
    stop_timer = False
    threading.Thread(target=launch_bot, daemon=True).start()
    threading.Thread(target=countdown, args=(config["session_duration"],), daemon=True).start()

def stop_automining():
    global stop_timer
    stop_timer = True
    killed = 0
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if (
                "python" in proc.info['name'].lower() and
                "main.py" in " ".join(proc.info['cmdline']).lower()
            ):
                proc.terminate()
                killed += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    if killed:
        messagebox.showinfo("Arrêté", f"Processus AutoMining arrêté ({killed})")
    else:
        messagebox.showwarning("Aucun processus trouvé", "Aucun processus main.py trouvé.")

# Widgets
tk.Label(root, text="Durée de la session (minutes):").pack()
tk.Entry(root, textvariable=session_duration_var).pack()

tk.Label(root, text="Ressources à miner:").pack()
for res, var in resources_vars.items():
    tk.Checkbutton(root, text=res.capitalize(), variable=var).pack(anchor="w")

tk.Label(root, text="Portée PRL:").pack()
tk.Entry(root, textvariable=jump_range_var).pack()

tk.Label(root, text="Secteurs ciblés:").pack()
sectors_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, height=6)
for sector in sector_names:
    sectors_listbox.insert(tk.END, sector)
sectors_listbox.pack()

tk.Label(root, text="Temps restant:").pack()
tk.Label(root, textvariable=timer_label_var, fg="red", font=("Arial", 14)).pack()

tk.Button(root, text="Enregistrer", command=save_config).pack(pady=5)
tk.Button(root, text="▶️ Start AutoMining", command=start_automining).pack(pady=5)
tk.Button(root, text="🛑 Stop AutoMining", command=stop_automining).pack(pady=5)
tk.Button(root, text="Quitter", command=root.destroy).pack(pady=5)

root.mainloop()

# Nouvelle logique de minage


