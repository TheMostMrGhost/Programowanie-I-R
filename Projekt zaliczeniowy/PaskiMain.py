from Pliki import *
import Rozpoznawacz as roz
#=======================================================================================
def podajFilmy(): 
    filmy = []
    nowyFilm = "a"
    while nowyFilm!= 'q':
        nowyFilm = input("Podaj link do filmu lub wpisz \'q\' by zakończyć dodawanie\n")
        if nowyFilm == 'q':
            break
        filmy.append(Plik(nowyFilm,"film" + str(len(filmy))))# TODO zrobić to regexpami 
    wybór = input("Czy chcesz ominąć proces pobierania? [y/n]") == "y"# TODO to do usunięcia
    if not wybór:
        any(map(lambda x: x.download(), filmy))
    return filmy
#=======================================================================================
def clean(filmy):
    czyścimy = input("Czy chcesz po sobie posprzątać [y/n]?\n") == "y"
    if czyścimy:
        any(map(lambda x: x.cleanAfterWork(),filmy))
#=======================================================================================
def main(link, name, czyPrzygotowane, czyPokazywać = False):
    # file = Plik('https://www.youtube.com/watch?v=fxvg_xOy4Y4', 'elolo')
    # file.parser()
    print("Witaj w programie do wycinania z tickerów.")
    filmy = podajFilmy()
    if len(filmy) == 0:
        return
    answer = int(input("Czy korzystasz z wersji starej (1), podstawowej (2), czy ulepszonej (3)?\n"))
    if answer == 1:
        any(map(lambda x: x.parser(), filmy))
        any(map(lambda x: x.analyzeVideo(czyPokazywać), filmy))
        if input("Sprzątać [y/n]?\n") == 'y':
            clean(filmy)
    elif answer == 2:
        any(map(lambda x: x.analyzeLive(), filmy))
    elif answer == 3:
        any(map(lambda x: x.upgradedAnalyzeLive(), filmy))
    else:
        print("Nie ma takiej opcji, do widzenia.\n")
    # file2 = Plik(link,name)
    # if not czyPrzygotowane:
    #     file2.download()
    #     file2.parser()
    # file2.analyzeVideo(czyPokazywać)
    # file2.cleanAfterWork()
    # rozpoznawacz = roz.Rozpoznawacz('frame0.jpg')
    # tekst = rozpoznawacz.recognize(850,980,350,1800)
    # print(rozpoznawacz.text)
    # file2 = Plik('https://github.com/ytdl-org/youtube-dl#format-selection-examples', 'hihi')
    # file2.download()https://www.tvp.info/54526597/premier-podsumowuje-szczyt-ue?copyId=54146645
    


if __name__ == "__main__":
    main('https://www.tvp.info/54522642/czym-grozi-nam-udar-cieplny','Udar',True)