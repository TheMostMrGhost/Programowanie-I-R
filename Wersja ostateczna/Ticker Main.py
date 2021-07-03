from Pliki import *
import Rozpoznawacz as roz, os
import tkinter as tk
from Pliki import *
from tkinter import ttk
import tkinter.font as tkf
import time
#====================================================================
# Nie będę przesadnie komentował poszczególnych elementów kodu zawartych w tym pliku, 
# bo nie dzieje się tu nic szczególnego, po prostu żmudnie ustawiłem kolejne elementy GUI
#====================================================================
def main():
    DEFAULTWIDTH = 100
    LABELTEXTCOLOR = 'gray16'
    LABELBACKGROUND = 'pale green'
    BUTTONCOLOR = 'forest green'
    films = []
    mode = 1 
    #====================================================================
    root = tk.Tk()
    root.title("Ticker reader")
    root.geometry("1000x200")
    root.configure(bg = LABELBACKGROUND)
    font = tkf.Font(size = 20)
    objectFont = tkf.Font(size = 12)
    #====================================================================
    lblGreetings = tk.Label(root, text = "Witaj w programie do wycinania tickerów.\n"
        + "Podaj linki do filmów z których chcesz wyciąć tickery.", font = font, bg = LABELBACKGROUND, fg = LABELTEXTCOLOR )
    lblModes = tk.Label(root, text = "Wybierz tryb pracy programu.", font = font, bg = LABELBACKGROUND, fg = LABELTEXTCOLOR)
    lblWait = tk.Label(root, text = "Proszę czekać, przetwarzam filmy.", font = font, bg = LABELBACKGROUND, fg = LABELTEXTCOLOR)
    lblDownloadFinished = tk.Label(root, text = "Pobieranie zakończone.", font = font, bg = LABELBACKGROUND, fg = LABELTEXTCOLOR)
    lblClean = tk.Label(root, text = "Czy chcesz usunąć pliki pośrednie?", font = font, bg = LABELBACKGROUND, fg = LABELTEXTCOLOR)
    lblZero = tk.Label(root, text = "Brak plików, kończę działanie programu...", font = font, bg = LABELBACKGROUND, fg = LABELTEXTCOLOR)
    lblDownload = tk.Label(root, text = "Trwa pobieranie filmów, proszę czekać...", font = font, bg = LABELBACKGROUND, fg = LABELTEXTCOLOR)
    lblAnalyze = tk.Label(root, text = "Trwa przetwarzanie filmów, proszę czekać...", font = font, bg = LABELBACKGROUND, fg = LABELTEXTCOLOR)
    lblAnalyzeFinished = tk.Label(root, text = "Analiza zakończona, możesz zamknąć okno.", font = font, bg = LABELBACKGROUND, fg = LABELTEXTCOLOR)
    lblEnd = tk.Label(root, text = "Przetwarzanie zakończone.\n Program ulegnie samozniszczeniu za:", font = font, bg = LABELBACKGROUND, fg = LABELTEXTCOLOR)
    #====================================================================
    entNewFilms = tk.Entry(
        root,
        width = int(0.8*DEFAULTWIDTH),
        justify = 'center',
        font = objectFont,
        bg = BUTTONCOLOR,
        fg = 'white'
    )
    #===========================================
    progressDown = ttk.Progressbar(
        root,
        orient = 'horizontal',
        length = 3*DEFAULTWIDTH,
        mode = 'determinate'
    )
    #===========================================
    progressAnalyze = ttk.Progressbar(
        root,
        orient = 'horizontal',
        length = 3*DEFAULTWIDTH,
        mode = 'determinate'
    )
    #===========================================
    modeOptions = [
        "Tryb podstawowy: czytanie z głównego tickera.",
        "Tryb rozszerzony: czytanie z tickera głównego i dodatkowego."
    ] 
    #====================================================================
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
        if len(films) == 0:
            
            lblZero.pack()
            root.update()
            time.sleep(2)
            root.destroy()
            return
        
        lblDownload.pack(pady = 20)
        progressDown.pack(pady = 10)
        root.update()

        any(map(lambda x: downloadBar(x, 100/len(films)), films))
        
        root.update()
        time.sleep(1)
        progressDown.destroy()
        lblDownload.destroy()

        showAvailableModes()
    #===========================================
    def downloadBar(file, step = 100):
        file.download()
        progressDown['value'] += step
        root.update()
    #===========================================
    def showAvailableModes():
        lblModes.pack()
        modeChoice.config(
            font = objectFont,
            bg = BUTTONCOLOR,
            fg = 'white'
        )
        modeChoice.pack()
        modeConfirm.pack()
        root.update()
    #===========================================
    def confirmMode():
        temp = front.get()
        if temp == modeOptions[0]:
            mode = 1
        if temp == modeOptions[1]:
            mode = 2

        analyze(mode)
    #===========================================
    def analyze(mode):
        lblModes.destroy()
        modeChoice.destroy()
        modeConfirm.destroy()
        root.update()
        
        if len(films) == 0:
            lblZero.pack()
            root.update()
            time.sleep(2)
            root.destroy()
            return
        
        lblAnalyze.pack(pady = 20)
        progressAnalyze.pack(pady = 10)
        root.update()
    
        any(map(lambda x: analyzeBar(x, mode, 100/len(films)), films))
        
        root.update()
        time.sleep(1)
        progressAnalyze.destroy()
        lblAnalyze.destroy()

        cleaningStage()
    #===========================================
    def analyzeBar(file, mode, step = 100):
        file.analyzeLive(mode)
        progressAnalyze['value'] += step
        root.update()
    #===========================================
    def cleaningStage():
        lblClean.pack()
        cleanDismiss.pack(side = tk.RIGHT)
        cleanConfirm.pack(side = tk.RIGHT)
    #===========================================
    def clean():
        any(map(lambda x: x.cleanAfterWork(), films))
        endProgram()
    #===========================================
    def endProgram():
        lblClean.destroy()
        cleanConfirm.destroy()
        cleanDismiss.destroy()
        ii = 5
        tempText = tk.StringVar(root)
        tempText.set(str(ii))
        lblCount = tk.Label(root, textvariable = tempText, font = font, bg = LABELBACKGROUND, fg = LABELTEXTCOLOR)
        lblEnd.pack()
        lblCount.pack()
        root.update()

        while ii > 0:
            time.sleep(1)
            ii-=1
            tempText.set(str(ii))
            root.update()
        
        root.destroy()
    #===========================================
    lblGreetings.pack()
    entNewFilms.insert(0, "Link do filmu")
    entNewFilms.pack()

    endAdding = tk.Button(
        root,
        text = "Zakończ dodawanie",
        command = finishAdding,
        font = objectFont,
        bg = BUTTONCOLOR,
        fg = 'white'
    )

    addFilm = tk.Button(
        root,
        text = "Dodaj",
        command = addNewFilm,
        font = objectFont,
        bg = BUTTONCOLOR,
        fg = 'white'
    )

    modeConfirm = tk.Button(
        root,
        text = "Zatwierdź",
        command = confirmMode,
        font = objectFont,
        bg = BUTTONCOLOR,
        fg = 'white'
    )

    cleanConfirm = tk.Button(
        root,
        text = "Posprzątaj",
        command = clean,
        font = objectFont,
        bg = BUTTONCOLOR,
        fg = 'white'
    )
    cleanDismiss = tk.Button(
        root,
        text = "Wyjdź bez sprzątania",
        command = endProgram,
        font = objectFont,
        bg = BUTTONCOLOR,
        fg = 'white'
    )

    front = tk.StringVar(root)
    front.set(modeOptions[0])
    modeChoice = tk.OptionMenu(
        root,
        front,
        *modeOptions
    )

    endAdding.pack(side = tk.RIGHT)
    addFilm.pack(side = tk.RIGHT)

    root.mainloop()

if __name__ == "__main__":
    main()