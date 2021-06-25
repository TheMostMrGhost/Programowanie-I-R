import Kraj, requests, sys
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
                        else:
                            dane[ii].append(0)
        return dane # Wyklucza niezwrócenie danych w wyniku wywołania ostatniego kraju na liście
#===========================================================
def zapiszKolumnę(kraj, nazwaTablicy, format = ".txt"):
    if kraj.name == "No name":
        return
    with open("./" + kraj.name + " " + nazwaTablicy + format,"w") as file:
        if kraj[nazwaTablicy] != None and len(kraj[nazwaTablicy]) > 0:
            file.write(str(kraj[nazwaTablicy][0]))
            for ii in range(1,len(kraj[nazwaTablicy])):
                file.write("," + str(kraj[nazwaTablicy][ii]))
#===========================================================
def pokażWszystkieKolumny():
    with open("./owid-covid-data.csv") as file:
        tytuły = file.readline()
        tytuły = list(tytuły.split(","))
        for ii in tytuły:
            print(ii)
#===========================================================
def pokażDostępneKolumny():
    temp = dajDostępneKolumny()
    for ii in temp:
        print(ii)
#===========================================================
def pokażDostępneKraje():
    with open("./owid-covid-data.csv") as file:
        ostatni = file.readline().split(",")[2]
        for linia in file:
            if ostatni != linia.split(",")[2]:
                ostatni = linia.split(",")[2]
                print(ostatni)
#===========================================================
def dajDostępneKraje():
    dostępne = []
    with open("./owid-covid-data.csv") as file:
        ostatni = file.readline().split(",")[2]
        for linia in file:
            if ostatni != linia.split(",")[2]:
                ostatni = linia.split(",")[2]
                dostępne.append(ostatni)
    return dostępne
#===========================================================
def dajDostępneKolumny():
    res = ["total_cases","new_cases","total_deaths","total_vaccinations"]
    return res
#===========================================================
def sprawdźCzySąDane():
    czyPobranoNowy = False
    try:
        tymczasowy = open("./owid-covid-data.csv")
    except IOError:
        while True:
            odp = input("Nie wykryto pliku z danymi. Czy chcesz pobrać nowe dane? y/n \n")
            if odp == "y":
                czyPobranoNowy = True
                pobierzDane()
                break
            elif odp == "n":
                print("Nic więcej nie mogę zrobić, do widzenia\n")
                tymczasowy.close()
                sys.exit()
            else: 
                print("Nieznana odpowiedź, spróbuj ponownie\n")
    finally:
        if czyPobranoNowy == False:
            tymczasowy.close()
#===========================================================
def pobierzDane():
        r = requests.get('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv')
        file = open("./owid-covid-data.csv", "w", encoding='utf8')
        file.write(r.text)
        file.close()