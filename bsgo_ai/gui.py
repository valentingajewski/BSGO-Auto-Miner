import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import re
import sys
import queue
import threading
import subprocess
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
SECTORS_DIR = os.path.join(BASE_DIR, 'sectors_links')
CONFIG_PATH = os.path.join(BASE_DIR, 'gui_config.json')
MAIN_SCRIPT = os.path.join(BASE_DIR, 'status', 'main.py')

SERVER_FILES = {
    "Exodus": os.path.join(SECTORS_DIR, 'sectors_exodus.json'),
    "Memento": os.path.join(SECTORS_DIR, 'secteurs_memento.json'),
}

# --- Dark theme palette -------------------------------------------------
BG = 'black'
FG = 'white'
FG_MUTED = '#888888'
ACCENT = '#333333'
FONT = ('Courier', 10)
FONT_BOLD = ('Courier', 10, 'bold')
FONT_TITLE = ('Courier', 11, 'bold')

# Log level -> color mapping for the log widget tags
LEVEL_COLORS = {
    'INFO': '#d0d0d0',
    'ACTION': '#ffd24d',
    'WARNING': '#ff5c5c',
    'DEBUG': '#7fd0ff',
    'STAT': '#5cff8f',
    'WATER': '#4da6ff',
}

ANSI_ESCAPE = re.compile(r'\x1b\[[0-9;]*m')
LEVEL_RE = re.compile(r'\[(INFO|ACTION|WARNING|DEBUG|STAT)\]')


def load_existing_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def load_sectors(server_name):
    filepath = SERVER_FILES.get(server_name, SERVER_FILES["Exodus"])
    with open(filepath, 'r') as f:
        return json.load(f)


class MinerGUI:
    def __init__(self, root):
        self.root = root
        self.existing_config = load_existing_config()
        default_server = self.existing_config.get("server", "Exodus")

        self.sectors_json = load_sectors(default_server)
        self.sorted_sectors = sorted(self.sectors_json, key=lambda s: s["name"])

        # Runtime state
        self.process = None
        self.reader_thread = None
        self.log_queue = queue.Queue()
        self.running = False
        self.start_epoch = None
        self.stats = {"scanned": 0, "water": 0, "tylium": 0,
                      "titanium": 0, "sector": "-"}

        self._build_window(default_server)
        self._configure_style()
        self._build_controls()

        self._on_start_option_change()
        self.root.after(100, self._drain_log_queue)
        self.root.after(1000, self._tick_elapsed)
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    # ------------------------------------------------------------------
    # Window / theme
    # ------------------------------------------------------------------
    def _build_window(self, default_server):
        self.root.title("BSGO Auto Miner")
        self.root.geometry("640x860")
        self.root.minsize(560, 640)
        self.root.configure(bg=BG)

        self.server_var = tk.StringVar(value=default_server)
        self.first_conn_var = tk.BooleanVar(
            value=self.existing_config.get("first_connection", False))
        self.start_option_var = tk.StringVar(
            value=self.existing_config.get("start_delay", {}).get("mode", "now"))

    def _configure_style(self):
        style = ttk.Style()
        style.theme_use('default')

        style.configure('TFrame', background=BG)
        style.configure('Dark.TLabelframe', background=BG,
                        bordercolor=ACCENT, relief='groove')
        style.configure('Dark.TLabelframe.Label', background=BG,
                        foreground=FG, font=FONT_TITLE)
        style.configure('TLabel', background=BG, foreground=FG, font=FONT)
        style.configure('Muted.TLabel', background=BG,
                        foreground=FG_MUTED, font=FONT)
        style.configure('Stat.TLabel', background=BG,
                        foreground=LEVEL_COLORS['STAT'], font=FONT_BOLD)
        style.configure('TButton', font=FONT_BOLD, foreground=FG,
                        background=BG, borderwidth=2)
        style.map('TButton',
                  background=[('active', ACCENT), ('disabled', '#111')],
                  foreground=[('disabled', FG_MUTED)])
        style.configure('TCheckbutton', background=BG, foreground=FG, font=FONT)
        style.map('TCheckbutton', background=[('active', BG)])
        style.configure('TRadiobutton', background=BG, foreground=FG, font=FONT)
        style.map('TRadiobutton', background=[('active', BG)])
        style.configure('TCombobox', fieldbackground=BG, background=BG,
                        foreground=FG, arrowcolor=FG)
        style.map('TCombobox', fieldbackground=[('readonly', BG)],
                  foreground=[('readonly', FG)])
        style.configure('Dark.TEntry', fieldbackground=BG, foreground=FG,
                        insertcolor=FG, bordercolor=ACCENT)

    # ------------------------------------------------------------------
    # Controls (top pane)
    # ------------------------------------------------------------------
    def _build_controls(self):
        # Vertical paned window: controls on top, log at bottom (resizable)
        self.paned = ttk.PanedWindow(self.root, orient=tk.VERTICAL)
        self.paned.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        top = ttk.Frame(self.paned)
        self.paned.add(top, weight=0)
        self._top_frame = top

        # --- Server section ---
        server_frame = ttk.LabelFrame(top, text="Server",
                                      style='Dark.TLabelframe', padding=8)
        server_frame.pack(fill=tk.X, pady=(0, 6))
        server_frame.columnconfigure(1, weight=1)
        ttk.Label(server_frame, text="Server:").grid(
            row=0, column=0, sticky='w', padx=(0, 8))
        self.server_combo = ttk.Combobox(
            server_frame, textvariable=self.server_var,
            values=list(SERVER_FILES.keys()), state="readonly")
        self.server_combo.grid(row=0, column=1, sticky='ew')
        self.server_combo.bind("<<ComboboxSelected>>", self._on_server_change)

        # --- Timing section ---
        timing_frame = ttk.LabelFrame(top, text="Timing",
                                      style='Dark.TLabelframe', padding=8)
        timing_frame.pack(fill=tk.X, pady=6)
        timing_frame.columnconfigure(1, weight=1)
        ttk.Label(timing_frame, text="Mining Duration (min):").grid(
            row=0, column=0, sticky='w', padx=(0, 8), pady=2)
        self.mining_time_entry = ttk.Entry(timing_frame, style='Dark.TEntry')
        self.mining_time_entry.grid(row=0, column=1, sticky='ew', pady=2)
        self.mining_time_entry.insert(
            0, str(self.existing_config.get("mining_time", "")))

        ttk.Label(timing_frame, text="Sector Duration (min):").grid(
            row=1, column=0, sticky='w', padx=(0, 8), pady=2)
        self.sector_time_entry = ttk.Entry(timing_frame, style='Dark.TEntry')
        self.sector_time_entry.grid(row=1, column=1, sticky='ew', pady=2)
        self.sector_time_entry.insert(
            0, str(self.existing_config.get("sector_time", "")))

        # --- Sectors section ---
        sectors_frame = ttk.LabelFrame(top, text="Sectors",
                                       style='Dark.TLabelframe', padding=8)
        sectors_frame.pack(fill=tk.BOTH, pady=6)
        list_container = ttk.Frame(sectors_frame)
        list_container.pack(fill=tk.BOTH, expand=True)
        list_scroll = ttk.Scrollbar(list_container, orient=tk.VERTICAL)
        self.sector_listbox = tk.Listbox(
            list_container, selectmode="multiple", bg=BG, fg=FG,
            font=FONT, height=8, highlightthickness=1,
            highlightbackground=ACCENT, highlightcolor=ACCENT,
            selectbackground=ACCENT, selectforeground=FG,
            borderwidth=0, activestyle='none',
            yscrollcommand=list_scroll.set)
        list_scroll.config(command=self.sector_listbox.yview)
        list_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.sector_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self._populate_sectors()

        # --- Scheduling section ---
        sched_frame = ttk.LabelFrame(top, text="Scheduling",
                                     style='Dark.TLabelframe', padding=8)
        sched_frame.pack(fill=tk.X, pady=6)

        self.first_conn_checkbox = ttk.Checkbutton(
            sched_frame, text="First connection", variable=self.first_conn_var)
        self.first_conn_checkbox.grid(row=0, column=0, columnspan=3,
                                      sticky='w', pady=(0, 4))

        ttk.Radiobutton(sched_frame, text="Now",
                        variable=self.start_option_var, value="now",
                        command=self._on_start_option_change).grid(
            row=1, column=0, sticky='w')
        ttk.Radiobutton(sched_frame, text="In X days / hours",
                        variable=self.start_option_var, value="delayed",
                        command=self._on_start_option_change).grid(
            row=1, column=1, columnspan=2, sticky='w')

        self.delay_frame = ttk.Frame(sched_frame)
        self.delay_frame.grid(row=2, column=0, columnspan=3,
                              sticky='w', pady=(6, 0))
        delay = self.existing_config.get("start_delay", {})
        self.days_entry = self._delay_field(self.delay_frame, "Days:", 0,
                                            delay.get("days", 0))
        self.hours_entry = self._delay_field(self.delay_frame, "Hours:", 2,
                                             delay.get("hours", 0))
        self.minutes_entry = self._delay_field(self.delay_frame, "Minutes:", 4,
                                               delay.get("minutes", 0))

        # --- Controls section ---
        ctrl_frame = ttk.LabelFrame(top, text="Controls",
                                    style='Dark.TLabelframe', padding=8)
        ctrl_frame.pack(fill=tk.X, pady=6)
        ctrl_frame.columnconfigure(2, weight=1)

        self.start_button = ttk.Button(ctrl_frame, text="Start",
                                       command=self.start_miner)
        self.start_button.grid(row=0, column=0, padx=(0, 6), ipadx=8, ipady=3)
        self.stop_button = ttk.Button(ctrl_frame, text="Stop",
                                      command=self.stop_miner, state='disabled')
        self.stop_button.grid(row=0, column=1, padx=6, ipadx=8, ipady=3)
        ttk.Button(ctrl_frame, text="Save", command=self.save_only).grid(
            row=0, column=2, padx=6, ipadx=8, ipady=3)

        self.status_dot = tk.Canvas(ctrl_frame, width=14, height=14,
                                    bg=BG, highlightthickness=0)
        self._dot = self.status_dot.create_oval(2, 2, 12, 12,
                                                fill=FG_MUTED, outline='')
        self.status_dot.grid(row=0, column=3, padx=(6, 4))
        self.status_label = ttk.Label(ctrl_frame, text="Idle",
                                      style='Muted.TLabel')
        self.status_label.grid(row=0, column=4, sticky='e')

        self._build_log_pane()

    def _delay_field(self, parent, label, col, value):
        ttk.Label(parent, text=label).grid(row=0, column=col, padx=(0, 4))
        entry = ttk.Entry(parent, width=5, style='Dark.TEntry')
        entry.insert(0, str(value))
        entry.grid(row=0, column=col + 1, padx=(0, 10))
        return entry

    def _populate_sectors(self):
        self.sector_listbox.delete(0, tk.END)
        saved = set(self.existing_config.get("sectors", []))
        for i, s in enumerate(self.sorted_sectors):
            self.sector_listbox.insert(tk.END, s["name"])
            if s["id"] in saved:
                self.sector_listbox.selection_set(i)

    # ------------------------------------------------------------------
    # Log panel (bottom pane)
    # ------------------------------------------------------------------
    def _build_log_pane(self):
        bottom = ttk.Frame(self.paned)
        self.paned.add(bottom, weight=1)

        # Stats bar
        stats_frame = ttk.LabelFrame(bottom, text="Live stats",
                                     style='Dark.TLabelframe', padding=6)
        stats_frame.pack(fill=tk.X, pady=(0, 6))
        for c in range(4):
            stats_frame.columnconfigure(c, weight=1)

        self.stat_labels = {}
        specs = [
            ("scanned", "Scanned", 0, 0),
            ("water", "Water", 0, 1),
            ("tylium", "Tylium", 0, 2),
            ("titanium", "Titanium", 0, 3),
            ("elapsed", "Elapsed", 1, 0),
            ("sector", "Sector", 1, 1),
        ]
        for key, title, r, c in specs:
            cell = ttk.Frame(stats_frame)
            cell.grid(row=r, column=c, sticky='w', padx=4, pady=2)
            ttk.Label(cell, text=f"{title}:", style='Muted.TLabel').pack(
                side=tk.LEFT, padx=(0, 4))
            lbl = ttk.Label(cell, text="0", style='Stat.TLabel')
            lbl.pack(side=tk.LEFT)
            self.stat_labels[key] = lbl
        self.stat_labels["elapsed"].config(text="00:00:00")
        self.stat_labels["sector"].config(text="-")

        # Log header + clear button
        log_header = ttk.Frame(bottom)
        log_header.pack(fill=tk.X)
        ttk.Label(log_header, text="Bot log", style='Muted.TLabel').pack(
            side=tk.LEFT)
        ttk.Button(log_header, text="Clear log",
                   command=self.clear_log).pack(side=tk.RIGHT)

        # Log text widget
        log_container = ttk.Frame(bottom)
        log_container.pack(fill=tk.BOTH, expand=True, pady=(4, 0))
        log_scroll = ttk.Scrollbar(log_container, orient=tk.VERTICAL)
        self.log_text = tk.Text(
            log_container, bg=BG, fg=FG, font=FONT, wrap='word',
            state='disabled', highlightthickness=1,
            highlightbackground=ACCENT, borderwidth=0,
            insertbackground=FG, yscrollcommand=log_scroll.set)
        log_scroll.config(command=self.log_text.yview)
        log_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        for level, color in LEVEL_COLORS.items():
            self.log_text.tag_configure(level, foreground=color)

    # ------------------------------------------------------------------
    # Sector / scheduling handlers
    # ------------------------------------------------------------------
    def _on_server_change(self, event=None):
        server = self.server_var.get()
        self.sectors_json = load_sectors(server)
        self.sorted_sectors = sorted(self.sectors_json, key=lambda s: s["name"])
        self.sector_listbox.delete(0, tk.END)
        for s in self.sorted_sectors:
            self.sector_listbox.insert(tk.END, s["name"])

    def _on_start_option_change(self):
        if self.start_option_var.get() == "delayed":
            self.delay_frame.grid()
        else:
            self.delay_frame.grid_remove()

    # ------------------------------------------------------------------
    # Config persistence
    # ------------------------------------------------------------------
    def save_config_file(self):
        try:
            mining_time = int(self.mining_time_entry.get())
            sector_time = int(self.sector_time_entry.get())

            selected_indices = self.sector_listbox.curselection()
            selected_ids = [self.sorted_sectors[i]["id"]
                            for i in selected_indices]
            if not selected_ids:
                raise ValueError("Aucun secteur sélectionné.")

            if self.start_option_var.get() == "now":
                start_delay = {"mode": "now"}
            else:
                try:
                    start_delay = {
                        "mode": "delayed",
                        "days": int(self.days_entry.get()),
                        "hours": int(self.hours_entry.get()),
                        "minutes": int(self.minutes_entry.get()),
                    }
                except ValueError:
                    raise ValueError(
                        "Veuillez entrer un nombre entier pour les jours et les heures.")

            config = {
                "server": self.server_var.get(),
                "mining_time": mining_time,
                "sector_time": sector_time,
                "sectors": selected_ids,
                "first_connection": self.first_conn_var.get(),
                "start_delay": start_delay,
            }

            with open(CONFIG_PATH, "w") as f:
                json.dump(config, f, indent=4)

            self.existing_config = config
            return True

        except ValueError as e:
            messagebox.showerror("Erreur", str(e))
            return False

    def save_only(self):
        if self.save_config_file():
            messagebox.showinfo("Succès", "Config saved")

    # ------------------------------------------------------------------
    # Bot process control
    # ------------------------------------------------------------------
    def start_miner(self):
        if self.running:
            return
        if not self.save_config_file():
            return
        try:
            env = os.environ.copy()
            env["KMP_DUPLICATE_LIB_OK"] = "TRUE"
            env["PYTHONIOENCODING"] = "utf-8"
            self.process = subprocess.Popen(
                [sys.executable, "-u", MAIN_SCRIPT],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
                bufsize=1,
                cwd=ROOT_DIR,
                env=env,
            )
        except Exception as e:
            messagebox.showerror("Erreur",
                                 f"Impossible de démarrer le script : {e}")
            return

        self._reset_stats()
        self.running = True
        self.start_epoch = time.time()
        self._set_status(True)

        self.reader_thread = threading.Thread(
            target=self._read_process_output, daemon=True)
        self.reader_thread.start()

    def stop_miner(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.process.kill()
        self.running = False
        self._set_status(False)

    def _read_process_output(self):
        try:
            for line in self.process.stdout:
                self.log_queue.put(line.rstrip("\n"))
        except Exception:
            pass
        finally:
            self.log_queue.put(("__DONE__", None))

    # ------------------------------------------------------------------
    # UI update loop
    # ------------------------------------------------------------------
    def _drain_log_queue(self):
        try:
            while True:
                item = self.log_queue.get_nowait()
                if isinstance(item, tuple) and item[0] == "__DONE__":
                    self.running = False
                    self._set_status(False)
                    continue
                self._handle_line(item)
        except queue.Empty:
            pass
        self.root.after(100, self._drain_log_queue)

    def _handle_line(self, raw_line):
        line = ANSI_ESCAPE.sub("", raw_line)
        if "[STAT]" in line:
            self._parse_stat(line)
        self._append_log(line)

    def _append_log(self, line):
        tag = None
        m = LEVEL_RE.search(line)
        if m:
            tag = m.group(1)
        elif "WATER" in line.upper():
            tag = 'WATER'
        self.log_text.config(state='normal')
        if tag:
            self.log_text.insert(tk.END, line + "\n", tag)
        else:
            self.log_text.insert(tk.END, line + "\n")
        self.log_text.config(state='disabled')
        self.log_text.see(tk.END)

    def _parse_stat(self, line):
        body = line.split("[STAT]", 1)[1].strip()
        if body.startswith("sector="):
            self.stats["sector"] = body[len("sector="):].strip() or "-"
        else:
            for pair in body.split():
                if "=" in pair:
                    k, v = pair.split("=", 1)
                    if k in self.stats and v.isdigit():
                        self.stats[k] = int(v)
        self._refresh_stat_labels()

    def _refresh_stat_labels(self):
        for key in ("scanned", "water", "tylium", "titanium"):
            self.stat_labels[key].config(text=str(self.stats[key]))
        self.stat_labels["sector"].config(text=self.stats["sector"])

    def _tick_elapsed(self):
        if self.running and self.start_epoch is not None:
            elapsed = int(time.time() - self.start_epoch)
            h, rem = divmod(elapsed, 3600)
            m, s = divmod(rem, 60)
            self.stat_labels["elapsed"].config(
                text=f"{h:02d}:{m:02d}:{s:02d}")
        self.root.after(1000, self._tick_elapsed)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _reset_stats(self):
        for k in ("scanned", "water", "tylium", "titanium"):
            self.stats[k] = 0
        self.stats["sector"] = "-"
        self.stat_labels["elapsed"].config(text="00:00:00")
        self._refresh_stat_labels()

    def _set_status(self, running):
        if running:
            self.status_dot.itemconfig(self._dot, fill=LEVEL_COLORS['STAT'])
            self.status_label.config(text="Running")
            self.start_button.config(state='disabled')
            self.stop_button.config(state='normal')
        else:
            self.status_dot.itemconfig(self._dot, fill=FG_MUTED)
            self.status_label.config(text="Idle")
            self.start_button.config(state='normal')
            self.stop_button.config(state='disabled')

    def clear_log(self):
        self.log_text.config(state='normal')
        self.log_text.delete('1.0', tk.END)
        self.log_text.config(state='disabled')

    def _on_close(self):
        if self.process and self.process.poll() is None:
            try:
                self.process.terminate()
                self.process.wait(timeout=2)
            except Exception:
                try:
                    self.process.kill()
                except Exception:
                    pass
        self.running = False
        self.root.destroy()


def main():
    root = tk.Tk()
    MinerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
