import tkinter as tk
from tkinter import filedialog
import shutil
import os

def fileChooser():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        filetypes=[
            ("Image files", "*.jpg *.jpeg *.png *.gif *.bmp"),
            ("All files", "*.*")
        ]
    )

    if file_path:
        return file_path
        
