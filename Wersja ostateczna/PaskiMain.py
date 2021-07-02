from Pliki import *
import Rozpoznawacz as roz, os
#=======================================================================================
def loadFilms():
    films = []
    newFilm = "foo"
    while newFilm != 'q':
        newFilm = input("Podaj link do filmu lub wpisz \'q\' by zakończyć dodawanie\n")
        if newFilm == 'q':
            break
        films.append(Plik(newFilm))
    any(map(lambda x: x.download(), films))
    return films
#=======================================================================================
def clean(films):
    doYouWantToClean = input("Czy chcesz usunąć produkty pośrednie (pobrane filmy i utworzone foldery) [y/n]?\n") == "y"
    if doYouWantToClean:
        any(map(lambda x: x.cleanAfterWork(), films))
#=======================================================================================
def chooseMode():
    print("W programie dostępne są natępujące tryby:\n 1) Podstawowy. Odczytuje tylko napisy z głównego " + 
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
#=======================================================================================
def main():
    os.system('cls')
    print("Witaj w programie do wycinania tickerów.")
    films = loadFilms()
    if len(films) == 0:
        return
    mode = chooseMode()
    any(map(lambda x: x.upgradedAnalyzeLive(mode), films))
    clean(films)


if __name__ == "__main__":
    main()