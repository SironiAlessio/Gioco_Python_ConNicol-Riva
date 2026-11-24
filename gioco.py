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

def attiva_schermo_intero(evento=None):
    finestra.attributes("-fullscreen", not finestra.attributes("-fullscreen"))

finestra.bind("<F11>", attiva_schermo_intero)
finestra.bind("<Escape>", lambda evento: finestra.attributes("-fullscreen", False))

stati_canvas = {}

def adatta_canvas(canvas, aggiorna_immagini=None):
    caratteri = []
    for elemento in canvas.find_all():
        if canvas.type(elemento) == "text":
            font = tkfont.Font(root=finestra, font=canvas.itemcget(elemento, "font"))
            misura = abs(font.cget("size"))
            caratteri.append((elemento, font, misura))
            canvas.itemconfig(elemento, font=font)

    def ridimensiona(evento=None):
        larghezza = max(canvas.winfo_width(), 1)
        altezza = max(canvas.winfo_height(), 1)
        scala = min(larghezza / LARGHEZZA, altezza / ALTEZZA)
        offset_x = (larghezza - LARGHEZZA * scala) / 2
        offset_y = (altezza - ALTEZZA * scala) / 2
        stato = stati_canvas.get(canvas, {"scala": 1.0, "x": 0.0, "y": 0.0})
        fattore = scala / stato["scala"]
        canvas.scale("all", 0, 0, fattore, fattore)
        canvas.move("all", offset_x - stato["x"] * fattore, offset_y - stato["y"] * fattore)
        stati_canvas[canvas] = {"scala": scala, "x": offset_x, "y": offset_y}
        for elemento, font, misura in caratteri:
            font.configure(size=max(6, round(misura * scala)))
        if aggiorna_immagini is not None:
            aggiorna_immagini(scala)

    canvas.bind("<Configure>", ridimensiona)
    canvas.after_idle(ridimensiona)

def coordinate_canvas(canvas, *coordinate):
    stato = stati_canvas.get(canvas, {"scala": 1.0, "x": 0.0, "y": 0.0})
    return [valore * stato["scala"] + (stato["x"] if indice % 2 == 0 else stato["y"])
            for indice, valore in enumerate(coordinate)]

def coordinate_logiche(canvas, evento):
    stato = stati_canvas.get(canvas, {"scala": 1.0, "x": 0.0, "y": 0.0})
    return ((evento.x - stato["x"]) / stato["scala"], (evento.y - stato["y"]) / stato["scala"])