"""
Real-time cursor coordinate display.
Press J to freeze/unfreeze the display.
Press Esc to exit.
"""

import tkinter as tk
from pynput import keyboard
import threading
import time


class CursorTracker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Cursor Coordinates")
        self.root.attributes("-topmost", True)
        self.root.geometry("320x80")
        self.root.resizable(False, False)

        self.frozen = False
        self.frozen_x = 0
        self.frozen_y = 0
        self.running = True

        self.label = tk.Label(
            self.root,
            text="X: 0  Y: 0",
            font=("Consolas", 18),
            fg="#00ff00",
            bg="#111111",
            padx=20,
            pady=15,
        )
        self.label.pack(fill=tk.BOTH, expand=True)

        self.status_label = tk.Label(
            self.root,
            text="[LIVE]  Press J to freeze  |  Esc to quit",
            font=("Consolas", 9),
            fg="#666666",
            bg="#111111",
        )
        self.status_label.pack(fill=tk.X)

        # Keyboard listener thread
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.daemon = True
        self.listener.start()

        self.update_display()

    def on_press(self, key):
        try:
            if hasattr(key, "char") and key.char and key.char.lower() == "j":
                self.frozen = not self.frozen
                if self.frozen:
                    self.frozen_x, self.frozen_y = self.root.winfo_pointerxy()
                    self.status_label.config(
                        text="[FROZEN]  Press J to unfreeze  |  Esc to quit",
                        fg="#ff4444",
                    )
                else:
                    self.status_label.config(
                        text="[LIVE]  Press J to freeze  |  Esc to quit",
                        fg="#666666",
                    )
            elif key == keyboard.Key.esc:
                self.running = False
                self.root.after(0, self.root.destroy)
        except Exception:
            pass

    def update_display(self):
        if not self.running:
            return

        if not self.frozen:
            x, y = self.root.winfo_pointerxy()
            self.label.config(text=f"X: {x:5d}  Y: {y:5d}")
        else:
            self.label.config(text=f"X: {self.frozen_x:5d}  Y: {self.frozen_y:5d}")

        self.root.after(50, self.update_display)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    tracker = CursorTracker()
    tracker.run()
