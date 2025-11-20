import os
import sys

def resource_path(*paths):
    relative_path = os.path.join(*paths)
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)