from Pliki import *
import Rozpoznawacz as roz, os, time
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
    "tickera.\n 2) Rozszerzony. Odczytuje napisy z tickera głównego i tickera dodatkowego.\n ")
    choice = input("Wybierz tryb wpisując jego numer i naciskając ENTER.\n")
    while True:
        if choice == '1':
            return 1
        elif choice == '2':
            return 2
        else: 
            print("Nieprawidłowy wybór, spróbój ponownie\n")
            choice = input("Wybierz tryb wpisując jego numer i naciskając ENTER.\n")
    print("Wybrano tryb " + choice + ".\n")
    input("Naciśnij ENTER by kontynuować.\n")
    os.system('cls')
#=======================================================================================
def main():
    os.system('cls')
    print("Witaj w programie do wycinania tickerów.")
    filmy = podajFilmy()
    if len(filmy) == 0:
        return
    mode = chooseMode()
    start = time.perf_counter_ns()
    any(map(lambda x: x.upgradedAnalyzeLive(mode), filmy))
    stop = time.perf_counter_ns()
    print((stop-start)/1000_000_000) # TODO usunąć czas
    clean(filmy)

#=======================================================================================
if __name__ == "__main__":
    main()