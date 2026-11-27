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

# Riproduce audio quando il giocatore segna. Commit3 
percorso_audio_gol = Path(__file__).with_name("Score a goal Sound effect  HD.mp3")
_alias_audio_gol = "audio_gol"
_mci = ctypes.windll.winmm.mciSendStringW
_mci(f'open "{percorso_audio_gol}" type mpegvideo alias {_alias_audio_gol}', None, 0, None)

def riproduci_audio_gol():
    _mci(f"stop {_alias_audio_gol}", None, 0, None)
    _mci(f"play {_alias_audio_gol} from 0", None, 0, None)

percorso_audio_parata = Path(__file__).with_name("OOOHHH YESSS!! - Football Commentary Sound Effect.mp3")
_alias_audio_parata = "audio_parata"
_mci(f'open "{percorso_audio_parata}" type mpegvideo alias {_alias_audio_parata}', None, 0, None)

def riproduci_audio_parata():
    _mci(f"stop {_alias_audio_parata}", None, 0, None)
    _mci(f"play {_alias_audio_parata} from 0", None, 0, None)

percorso_audio_vittoria = Path(__file__).with_name("Victory Sound Effect.mp3")
_alias_audio_vittoria = "audio_vittoria"
_mci(f'open "{percorso_audio_vittoria}" type mpegvideo alias {_alias_audio_vittoria}', None, 0, None)

def riproduci_audio_vittoria():
    ferma_audio_rigori()
    _mci(f"setaudio {_alias_audio_vittoria} volume to 1000", None, 0, None)
    _mci(f"play {_alias_audio_vittoria} from 0", None, 0, None)

percorso_audio_sconfitta = Path(__file__).with_name("Sad Trombone - Sound Effect (HD).mp3")
_alias_audio_sconfitta = "audio_sconfitta"
_mci(f'open "{percorso_audio_sconfitta}" type mpegvideo alias {_alias_audio_sconfitta}', None, 0, None)

def riproduci_audio_sconfitta():
    ferma_audio_rigori()
    _mci(f"setaudio {_alias_audio_sconfitta} volume to 1000", None, 0, None)
    _mci(f"play {_alias_audio_sconfitta} from 0", None, 0, None)

def ferma_audio_rigori():
    for alias in (_alias_audio_gol, _alias_audio_parata, _alias_audio_gol_computer, _alias_audio_parata_computer):
        _mci(f"stop {alias}", None, 0, None)
    _mci(f"stop {_alias_audio_vittoria}", None, 0, None)
    _mci(f"stop {_alias_audio_sconfitta}", None, 0, None)

percorso_audio_gol_computer = Path(__file__).with_name("Noooo! sound effect.mp3")
_alias_audio_gol_computer = "audio_gol_computer"
_mci(f'open "{percorso_audio_gol_computer}" type mpegvideo alias {_alias_audio_gol_computer}', None, 0, None)

def riproduci_audio_gol_computer():
    # Riapre il gioco al gol, così l'audio riparte anche dopo.
    _mci(f"close {_alias_audio_gol_computer}", None, 0, None)
    codice = _mci(f'open "{percorso_audio_gol_computer}" alias {_alias_audio_gol_computer}', None, 0, None)
    if codice == 0:
        _mci(f"play {_alias_audio_gol_computer} from 0", None, 0, None)

percorso_audio_parata_computer = Path(__file__).with_name("Boo - Sound Effects.mp3")
_alias_audio_parata_computer = "audio_parata_computer"
_mci(f'open "{percorso_audio_parata_computer}" type mpegvideo alias {_alias_audio_parata_computer}', None, 0, None)

def riproduci_audio_parata_computer():
    _mci(f"stop {_alias_audio_parata_computer}", None, 0, None)
    _mci(f"play {_alias_audio_parata_computer} from 0", None, 0, None)

#Commit4 
percorso_immagine = Path(__file__).with_name("Immagine 2 generata.png")
with Image.open(percorso_immagine) as immagine_originale:   # Open Apre l’immagine, with invece chiude correttamente il file.
    immagine_adattata = ImageOps.fit(immagine_originale, (LARGHEZZA, ALTEZZA))
immagine_iniziale = ImageTk.PhotoImage(immagine_adattata)

schermata_iniziale = tk.Canvas(finestra, width=LARGHEZZA, height=ALTEZZA, highlightthickness=0, cursor="arrow")
schermata_iniziale.place(x=0, y=0, relwidth=1, relheight=1) # Posiziona la finestra del gioco in alto a sinistra e lafa occupare tutta la finestra.
sfondo_iniziale_item = schermata_iniziale.create_image(0, 0, image=immagine_iniziale, anchor="nw") #  mette l’immagine con nw partendo dall’angolo in alto a sinistra
schermata_iniziale.create_text(390, 50, text="SOCCER PENALTY 6.7", fill="#D4AF37", font=("Ravie", 30))
for dx in range(-2, 3):
    for dy in range(-2, 3):
        if dx != 0 or dy != 0:
            schermata_iniziale.create_text(600 + dx, 500 + dy, text="GIOCA", fill="black", font=("Ravie", 30), tags="gioca")
schermata_iniziale.create_text(600, 500, text="GIOCA", fill="#D4AF37", font=("Ravie", 30), tags="gioca")
