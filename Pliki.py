def zrobListęKolumn(*args):
    with open("./owid-covid-data.csv") as file:
        tytuły = file.readline()
        tytuły = list(tytuły.split(","))
        tytuły[-1] = str.rstrip(tytuły[-1])
        kolumny = []
        ktoraKolumna = 0 # Patrzę które kolumny potrzebuję
        for ii in tytuły:
            if ii in args:
                kolumny.append(ktoraKolumna)
            ktoraKolumna += 1
    return kolumny
#===========================================================
def wczytajKolumny(nazwaKraju,*args):
    """Zwraca listę zawierającą kolumny o numerach z listaKolumn, dla podanego kraju"""
    listaKolumn = zrobListęKolumn(*args)
    with open("./owid-covid-data.csv") as file:
        dane = [] # Robię to w liście bo łatwiej jest nią uogólnić niż słownik, ewentualnie można jakiegoś enuma wmiksować czy coś TODO
        tytuły = file.readline() # Pomijam pierwszą linijkę
        flaga = False # Czy już trafiliśmy na kraj
        for ii in range(len(listaKolumn)):
            dane.append([])
        for line in file:
            temp = line.split(",")
            if temp[2] != nazwaKraju:
                # print(nazwaKraju,temp[2])
                if flaga:
                    return dane
            else:
                flaga = True # Ustawiamy flagę wielokrotnie, może można to przyspieszyć
                for ii in range(len(listaKolumn)):
                    if listaKolumn[ii] < 4: # Pierwsze cztery kolumny to słowa, nie chcemy ich konwertować na liczby
                        dane[ii].append(temp[listaKolumn[ii]])
                    else:
                        if temp[listaKolumn[ii]] != '':
                            dane[ii].append(int(float(temp[listaKolumn[ii]])))
        return dane # Wyklucza niezwrócenie danych w wyniku wywołania ostatniego kraju na liście