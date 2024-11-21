import os
import subprocess


def open_finder_macos(path):
    path = f"./output/{path}"
    abs_path = os.path.abspath(path)
    subprocess.run(["open", abs_path])
