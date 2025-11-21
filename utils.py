import os
import sys

def resource_path(*paths):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, *paths)

def writable_path(*paths):
    if getattr(sys, "frozen", False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.abspath(".")
    
    full_path = os.path.join(base_path, *paths)

    # garante que o diretório existe
    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    return full_path