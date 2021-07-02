from Pliki import *
import Rozpoznawacz as roz, os
import tkinter as tk
from Pliki import *
from tkinter import ttk
import tkinter.font as tkf
#====================================================================
def main():
    DEFAULTWIDTH = 100
    films = []

    root = tk.Tk()
    root.title("Ticker reader")
    root.geometry("800x150")
    font = tkf.Font(size = 20)

    lblGreetings = tk.Label(root, text = "Witaj w programie do wycinania tickerów.\n"
        + "Podaj linki do filmów z których chcesz wyciąć tickery.")

    lblWait = tk.Label(root, text = "Proszę czekać, przetwarzam filmy.", font = font)

    entNewFilms = tk.Entry(
        root,
        width = DEFAULTWIDTH,
        justify = 'center'
    )

    progress = ttk.Progressbar(
        root,
        orient = 'horizontal',
        length = 3*DEFAULTWIDTH,
        mode = 'determinate'
    )
    #===========================================
    def addNewFilm():
        temp = entNewFilms.get() 
        if temp != "" and temp != "Link do filmu":
            films.append(Plik(temp))
        entNewFilms.delete(0, tk.END)
    #===========================================
    def finishAdding():
        addFilm.destroy()
        entNewFilms.destroy()
        endAdding.destroy()
        lblGreetings.destroy()

        download()
    #===========================================
    def download():
        lblDownload = tk.Label(root, text = "Trwa pobieranie filmów, proszę czekać...", font = font)
        lblDownload.pack()
        progress.pack()
        root.update()
        numberOfVideos = len(films)
        any(map(lambda x: downloadBar(x, 100/numberOfVideos), films))
    #===========================================
    def downloadBar(file, step = 100):
        file.download()
        progress['value'] += step
        root.update()
    #===========================================
    lblGreetings.pack()
    entNewFilms.insert(0, "Link do filmu")
    entNewFilms.pack()

    endAdding = tk.Button(
        root,
        text = "Zakończ dodawanie",
        command = finishAdding,
    )

    addFilm = tk.Button(
        root,
        text = "Dodaj",
        command = addNewFilm
    )

    addFilm.pack()
    endAdding.pack()

    root.mainloop()

if __name__ == "__main__":
    main()