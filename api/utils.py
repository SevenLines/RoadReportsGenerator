import os
import subprocess
from tkinter import Tk, filedialog

def open_finder_macos(path):
    path = f"./output/{path}"
    abs_path = os.path.abspath(path)
    subprocess.run(["open", abs_path])


def choose_file():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    root.destroy()

    return file_path