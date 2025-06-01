import tkinter as tk
from tkinter import ttk, messagebox
import json
import subprocess

# Charger les secteurs depuis le JSON
with open('bsgo_ai/sectors_links/secteurs.json', 'r') as f:
    SECTORS_JSON = json.load(f)

# Interface principale
root = tk.Tk()
root.title("BSGO Auto Miner")
root.geometry("500x600")
root.configure(bg='black')

style = ttk.Style()
style.theme_use('default')
style.configure('TButton', font=('Courier', 10, 'bold'), foreground='white', background='black', borderwidth=2)
style.map('TButton', background=[('active', '#333')])
style.configure('TCombobox', fieldbackground='black', background='black', foreground='white')

# Champs utilisateur
tk.Label(root, text="Mining Duration (s):", fg="white", bg="black", font=("Courier", 10)).pack(pady=5)
mining_time_entry = tk.Entry(root)
mining_time_entry.pack(pady=5)

tk.Label(root, text="Sector Duration (s):", fg="white", bg="black", font=("Courier", 10)).pack(pady=5)
sector_time_entry = tk.Entry(root)
sector_time_entry.pack(pady=5)

tk.Label(root, text="Mining Sectors:", fg="white", bg="black", font=("Courier", 10)).pack(pady=5)
sector_listbox = tk.Listbox(root, selectmode="multiple", bg="black", fg="white", font=("Courier", 10), height=10)
for s in SECTORS_JSON:
    sector_listbox.insert(tk.END, s["name"])
sector_listbox.pack(pady=10)

# Fonctions
def get_selected_sector_ids():
    selected_indices = sector_listbox.curselection()
    return [SECTORS_JSON[i]["id"] for i in selected_indices]

def save_config_file():
    try:
        mining_time = int(mining_time_entry.get())
        sector_time = int(sector_time_entry.get())
        selected_ids = get_selected_sector_ids()

        if not selected_ids:
            raise ValueError("Aucun secteur sélectionné.")

        config = {
            "mining_time": mining_time,
            "sector_time": sector_time,
            "sectors": selected_ids
        }
        with open("bsgo_ai/gui_config.json", "w") as f:
            json.dump(config, f, indent=4)
        return True
    except ValueError as e:
        messagebox.showerror("Erreur", str(e))
        return False

def start_miner():
    if save_config_file():
        try:
            subprocess.Popen(["python", "bsgo_ai/status/main.py"])
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de démarrer le script : {e}")

def save_only():
    if save_config_file():
        messagebox.showinfo("Succès", "Configuration sauvegardée.")

# Boutons
ttk.Button(root, text="Start", command=start_miner).pack(pady=20, ipadx=10, ipady=5)
ttk.Button(root, text="Save", command=save_only).pack(pady=5, ipadx=10, ipady=5)

root.mainloop()
