import tkinter as tk
from UI import PasswordManager

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManager(root)
    root.mainloop()