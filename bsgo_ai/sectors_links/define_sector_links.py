import json
import tkinter as tk
from tkinter import messagebox, simpledialog

# Charger la liste des secteurs depuis un fichier ou une variable
SECTORS_FILE = 'bsgo_ai/sectors_links/secteurs.json'
LINKS_FILE = 'secteur_liens.json'

with open(SECTORS_FILE, 'r') as f:
    sectors = json.load(f)

sector_dict = {sector['id']: sector['name'] for sector in sectors}

# Initialisation des liens
links = {}

class SectorLinkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Définir les connexions entre les secteurs")
        self.root.attributes("-topmost", True)

        self.current_index = 0
        self.total = len(sector_dict)
        self.selected_links = []

        self.label = tk.Label(root, text="")
        self.label.pack(pady=10)

        self.listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, width=50, height=20)
        self.listbox.pack(pady=10)

        self.next_button = tk.Button(root, text="Suivant", command=self.save_and_next)
        self.next_button.pack(pady=10)

        self.update_interface()

    def update_interface(self):
        self.listbox.delete(0, tk.END)
        self.selected_links = []

        current_sector_id = self.get_current_sector_id()
        current_sector_name = sector_dict[current_sector_id]
        self.label.config(text=f"Quels secteurs sont connectés à : {current_sector_name} ?")

        # Trier les secteurs par nom
        sorted_sectors = sorted([(sid, name) for sid, name in sector_dict.items() if sid != current_sector_id], key=lambda x: x[1])

        for sid, name in sorted_sectors:
            self.listbox.insert(tk.END, f"{sid}: {name}")

    def get_current_sector_id(self):
        return list(sector_dict.keys())[self.current_index]

    def save_and_next(self):
        current_sector_id = self.get_current_sector_id()
        selected_indices = self.listbox.curselection()
        connected_ids = []

        for idx in selected_indices:
            entry = self.listbox.get(idx)
            sid = int(entry.split(":")[0])
            connected_ids.append(sid)

        links[current_sector_id] = connected_ids

        self.current_index += 1
        if self.current_index < self.total:
            self.update_interface()
        else:
            with open(LINKS_FILE, 'w') as f:
                json.dump(links, f, indent=4)
            messagebox.showinfo("Fini", "Toutes les connexions ont été définies !")
            self.root.quit()

if __name__ == '__main__':
    root = tk.Tk()
    app = SectorLinkApp(root)
    root.mainloop()