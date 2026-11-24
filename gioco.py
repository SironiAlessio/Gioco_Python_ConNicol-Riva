import tkinter as tk
import tkinter.font as tkfont
import random
import ctypes
from pathlib import Path
from PIL import Image, ImageOps, ImageTk


LARGHEZZA = 800
ALTEZZA = 600
TURNI = 5
squadra_avversaria = ""

finestra = tk.Tk()
finestra.title("Soccer Penalty 6.7")
finestra.resizable(True, True)
finestra.geometry(f"{LARGHEZZA}x{ALTEZZA}")
finestra.configure(bg="#071916")
