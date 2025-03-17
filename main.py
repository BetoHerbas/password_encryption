import tkinter as tk
from UI import PasswordManager
import ttkbootstrap as ttk

if __name__ == "__main__":
    root = ttk.Window(themename="cosmo")  # Usar un tema moderno
    app = PasswordManager(root)
    root.mainloop()