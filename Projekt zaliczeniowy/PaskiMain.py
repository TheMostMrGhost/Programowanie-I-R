from Pliki import *
import Rozpoznawacz as roz, os
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
def clean(filmy): # TODO przenieść do do Pliki 
    czyścimy = input("Czy chcesz po sobie posprzątać [y/n]?\n") == "y"
    if czyścimy:
        any(map(lambda x: x.cleanAfterWork(),filmy))
#=======================================================================================
def chooseMode():
    print("W programie dostępne są trzy tryby:\n 1) Podstawowy. Odczytuje tylko napisy z głównego " + 
    "tickera.\n 2) Rozszerzony. Odczytuje napisy z tickera głównego i tickera dodatkowego.\n "+
    "3) Eksperymentaly. Odczytuje ticker główny, tiker ,,Pilne\'\' i pasek przesuwny. UWAGA! Wykonanie programu w tym trybie trwa"+ 
    " bardzo długo i nie zawsze daje poprawne rezultaty.") # FIXME sprawdzić czy ten opis dalej działa
    choice = input("Wybierz tryb wpisując jego numer i naciskając ENTER.\n")
    while True:
        if choice == '1':
            return 1
        elif choice == '2':
            return 2
        elif choice == '3':
            return 3
        else: 
            print("Nieprawidłowy wybór, spróbój ponownie\n")
            choice = input("Wybierz tryb wpisując jego numer i naciskając ENTER.\n")
    # TODO dokończyć to
#=======================================================================================
def main():
    os.system('cls')
    print("Witaj w programie do wycinania tickerów.")
    filmy = podajFilmy()
    if len(filmy) == 0:
        return
    mode = chooseMode()
    any(map(lambda x: x.upgradedAnalyzeLive(mode), filmy))
    clean(filmy)
    

    # if len(filmy) == 0:
    #     return
    # answer = int(input("Czy korzystasz z wersji starej (1), podstawowej (2), czy ulepszonej (3)?\n"))
    # if answer == 1:
    #     any(map(lambda x: x.parser(), filmy))
    #     any(map(lambda x: x.analyzeVideo(czyPokazywać), filmy))
    #     if input("Sprzątać [y/n]?\n") == 'y':
    #         clean(filmy)
    # elif answer == 2:
    #     any(map(lambda x: x.analyzeLive(), filmy))
    # elif answer == 3:
    #     any(map(lambda x: x.upgradedAnalyzeLive(), filmy))
    # else:
    #     print("Nie ma takiej opcji, do widzenia.\n")
    


if __name__ == "__main__":
    main()