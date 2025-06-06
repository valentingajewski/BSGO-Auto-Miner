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
root.geometry("500x650")
root.configure(bg='black')

style = ttk.Style()
style.theme_use('default')
style.configure('TButton', font=('Courier', 10, 'bold'), foreground='white', background='black', borderwidth=2)
style.map('TButton', background=[('active', '#333')])
style.configure('TCombobox', fieldbackground='black', background='black', foreground='white')

# Champs utilisateur
tk.Label(root, text="Mining Duration (min):", fg="white", bg="black", font=("Courier", 10)).pack(pady=5)
mining_time_entry = tk.Entry(root)
mining_time_entry.pack(pady=5)

tk.Label(root, text="Sector Duration (min):", fg="white", bg="black", font=("Courier", 10)).pack(pady=5)
sector_time_entry = tk.Entry(root)
sector_time_entry.pack(pady=5)

tk.Label(root, text="Mining Sectors:", fg="white", bg="black", font=("Courier", 10)).pack(pady=5)

# Trier les secteurs par nom
sorted_sectors = sorted(SECTORS_JSON, key=lambda s: s["name"])

# Mettre à jour le listbox avec la liste triée
sector_listbox = tk.Listbox(root, selectmode="multiple", bg="black", fg="white", font=("Courier", 10), height=10)
for s in sorted_sectors:
    sector_listbox.insert(tk.END, s["name"])
sector_listbox.pack(pady=10)


# Checkbox First connection
first_conn_var = tk.BooleanVar()
first_conn_checkbox = tk.Checkbutton(root, text="First connection", variable=first_conn_var,
                                     onvalue=True, offvalue=False,
                                     font=("Courier", 10), bg='black', fg='white', selectcolor='black', activebackground='black')
first_conn_checkbox.pack(pady=10)

# Option de démarrage différé
start_option_var = tk.StringVar(value="now")  # Valeur par défaut

tk.Label(root, text="Start mining:", fg="white", bg="black", font=("Courier", 10)).pack(pady=5)

start_frame = tk.Frame(root, bg='black')
start_frame.pack()

tk.Radiobutton(start_frame, text="Now", variable=start_option_var, value="now",
               font=("Courier", 10), bg="black", fg="white", selectcolor='black').pack(anchor="w")
tk.Radiobutton(start_frame, text="In X days / hours", variable=start_option_var, value="delayed",
               font=("Courier", 10), bg="black", fg="white", selectcolor='black').pack(anchor="w")

# Champs pour le délai (initialement visibles car ça évite de devoir gérer l'affichage dynamique)
delay_frame = tk.Frame(root, bg='black')
delay_frame.pack(pady=5)

tk.Label(delay_frame, text="Jours :", fg="white", bg="black", font=("Courier", 10)).grid(row=0, column=0, padx=5)
days_entry = tk.Entry(delay_frame, width=5)
days_entry.insert(0, "0")
days_entry.grid(row=0, column=1)

tk.Label(delay_frame, text="Heures :", fg="white", bg="black", font=("Courier", 10)).grid(row=0, column=2, padx=5)
hours_entry = tk.Entry(delay_frame, width=5)
hours_entry.insert(0, "0")
hours_entry.grid(row=0, column=3)

tk.Label(delay_frame, text="Minutes:", fg="white", bg="black", font=("Courier", 10)).grid(row=0, column=4, padx=5)
minutes_entry = tk.Entry(delay_frame, width=5)
minutes_entry.insert(0, "0")
minutes_entry.grid(row=0, column=5)


# Fonctions
def get_selected_sector_ids():
    selected_indices = sector_listbox.curselection()
    return [sorted_sectors[i]["id"] for i in selected_indices]


def save_config_file():
    try:
        # Récupération des durées
        mining_time = int(mining_time_entry.get())
        sector_time = int(sector_time_entry.get())

        # Récupération des secteurs sélectionnés (depuis la liste triée)
        selected_indices = sector_listbox.curselection()
        selected_ids = [sorted_sectors[i]["id"] for i in selected_indices]

        if not selected_ids:
            raise ValueError("Aucun secteur sélectionné.")

        # Récupération de l'option de démarrage     
        if start_option_var.get() == "now":
            start_delay = {"mode": "now"}
        else:
            try:
                days = int(days_entry.get())
                hours = int(hours_entry.get())
                minutes = int(minutes_entry.get())
                start_delay = {"mode": "delayed", "days": days, "hours": hours, "minutes": minutes}
            except ValueError:
                raise ValueError("Veuillez entrer un nombre entier pour les jours et les heures.")

        # Construction du dictionnaire de configuration
        config = {
            "mining_time": mining_time,
            "sector_time": sector_time,
            "sectors": selected_ids,
            "first_connection": first_conn_var.get(),
            "start_delay": start_delay
        }

        # Sauvegarde dans le fichier JSON
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
