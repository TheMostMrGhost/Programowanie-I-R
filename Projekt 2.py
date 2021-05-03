# Najważniejsze pola w tym csv: Czas, kraj, nowe zakażenia, total cases, total deaths,
# ew total tests, positive rate, total vaccinations, new vaccinations
import Pliki, Kraj, matplotlib.pyplot as plt, numpy as np, Region, os, time
def testy():
    kraje = []
    nazwy = ["Poland", "Spain", "Russia","Saint Vincent and the Grenadines", "World", "Australia"]
    for ii in range(len(nazwy)):
        kraje.append(Kraj.Kraj(nazwy[ii]))
        # kraje[ii].piszPlik("total_vaccinations") Zrobić to mapem TODO
        # print(kraje[ii].location,kraje[ii].total_cases)
        # kraje[ii].noweWykres()
        # kraje[ii].wszystkieWykres()
    nowyRegion = kraje[0] + kraje[2] 
    nowyRegion.wszystkieWykres()
    nowyRegion.piszPlik("total_vaccinations")
#=================================================
def pokażOpcje():
    print("Wybierz co chcesz zrobić. W celu wybrania opcji wpisz znak umieszczony w nawiasie kwadratowym:\n" +
        "- Pokaż dostępne kraje [p]\n"+ 
        "- Dodaj nowy kraj [n]\n" +
        "- Pokaż stworzone kraje [k]\n" +
        "- Rysuj wykres danych dla kraju (dodatkowe parametry dostępne po wybraniu tej opcji) [r]\n" +
        "- Zapisz dane z tabeli do pliku [z]\n" +
        "- Dodaj nowy region (region to połączenie już istniejących krajów/regionów) [d]\n" +
        "- Wyjdź [q]")
#=================================================
def wyświetlListę(lista):
    for ii in lista:
        print(ii)
#=================================================
def main():
    clear = lambda: os.system('cls')
    clear()
    print("Witaj w programie do wizualizacji danych dotyczących epidemii COVID-19.")
    Pliki.sprawdźCzySąDane()
    kraje = []
    odpowiedź = ""
    while odpowiedź != "q":
        pokażOpcje()
        odpowiedź = input()
         # Czemu w pythonie nie ma switch casów :(    
        if odpowiedź == "p":
            clear()
            Pliki.pokażDostępneKraje()

        elif odpowiedź == "k":
            clear()
            wyświetlListę(kraje)

        elif odpowiedź == "n":
            nazwa = input("Wpisz nazwę kraju:\n")
            if nazwa in Pliki.dajDostępneKraje(): #TODO Zrobić żeby nie mogły się powtarzać
                kraje.append(Kraj.Kraj(nazwa))
                clear()
            else:
                print("Nie ma takiego kraju, przerywam dodawanie")
                time.sleep(2)
                clear()

        elif odpowiedź == "r":
            print("Wybierz kraj z dostępnych na liście:")
            wyświetlListę(kraje)
            nazwa = input("Wpisz nazwę kraju:\n")
            temp = Kraj.szukajKraju(kraje,nazwa)
            if temp != None:
                tabela = input("Wybierz co pokazać na wykresie:\n - Nowe zachorowania [n]\n - Wszystkie zachorowania [w]\n - Łączna liczba zgonów [s]\n" + 
                " - Łączna liczba zaszczepionych [z]\n")
                if tabela == "n":
                    temp.noweWykres()
                elif tabela == "w":
                    temp.wszystkieWykres()
                elif tabela == "s":
                    temp.wszystkieŚmierciWykres()
                elif tabela == "z":
                    temp.zaszczepieniWykres()
                else:
                    print("Nie ma takiej opcji, przerywam rysowanie")
                    time.sleep(2)
                clear()
            else:
                print("Nie ma takiego kraju, przerywam rysowanie\n")
                time.sleep(2)
                clear()

        elif odpowiedź == "z":
            print("Wybierz kraj z listy:\n")
            wyświetlListę(kraje)
            który = input()
            res = Kraj.szukajKraju(kraje,nazwa)
            if res != None:
                print("Wybierz tabelę którą chcesz zapisać:\n")
                Pliki.pokażDostępneKolumny()
                który = input()
                dos = Pliki.dajDostępneKolumny()
                if który in dos:
                    res.piszPlik(który)
                else:
                    print("Nie ma takiej kolumny, zatrzymuję zapisywanie")
                    time.sleep(2)
                    clear()

        elif odpowiedź == "d":
            print("Dostępne kraje:\n")
            wyświetlListę(kraje)
            pierwszy = input("Wybierz pierwszy kraj:\n")
            drugi = input("Wybierz drugi kraj:\n")
            pierwszy = Kraj.szukajKraju(kraje,pierwszy)
            drugi = Kraj.szukajKraju(kraje,drugi)

            if pierwszy != None and drugi != None:
                kraje.append(pierwszy + drugi)
                print("Dodawanie zakończone sukcesem")
                time.sleep(2)
                clear()
            else:
                print("Któryś z krajów nie należy do listy, przerywam dodawanie regionu")
                time.sleep(2)
                clear()

        elif odpowiedź == "q":
            break

        else:
            print("Nieznana odopwiedź, spróbuj ponownie")
            time.sleep(2)
            clear()
        
if __name__ == "__main__":
    main()