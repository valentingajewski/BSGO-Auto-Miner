import tkinter as tk
import pyautogui
from pynput import keyboard
import threading

class CursorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Coordonnées du Curseur")

        # Label pour les coordonnées en direct
        self.live_label = tk.Label(root, text="Live: x=0, y=0", font=("Arial", 14))
        self.live_label.pack(pady=10)

        # Label pour les coordonnées figées (lors de l'appui sur J)
        self.frozen_label = tk.Label(root, text="Freeze: x=0, y=0", font=("Arial", 14), fg="blue")
        self.frozen_label.pack(pady=10)

        # Mise à jour en temps réel
        self.update_cursor_position()

        # Lancer le listener clavier dans un thread
        listener_thread = threading.Thread(target=self.keyboard_listener, daemon=True)
        listener_thread.start()

    def update_cursor_position(self):
        x, y = pyautogui.position()
        self.live_label.config(text=f"Live: x={x}, y={y}")
        self.root.after(100, self.update_cursor_position)

    def on_press(self, key):
        try:
            if key.char == 'j':
                x, y = pyautogui.position()
                self.frozen_label.config(text=f"Freeze: x={x}, y={y}")
        except AttributeError:
            # Ignore special keys like shift, ctrl etc.
            pass

    def keyboard_listener(self):
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()

if __name__ == "__main__":
    root = tk.Tk()
    app = CursorApp(root)
    root.mainloop()
