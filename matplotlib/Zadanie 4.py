import matplotlib.pyplot as plt, requests, sys
#Wersja alpha, jeszcze nie ściąga informacji z internetu
#===================================
def robWykres(dni, ludzie):
    plt.plot(dni, ludzie, 'g')
    plt.grid()
    plt.xlabel("Czas trwania epidemii (w dniach)")
    plt.ylabel("Liczba zakażonych w danym dniu")
    plt.legend("Nowi zakażeni")
    plt.show()
    plt.close()
#===================================
def pobierzDane():
    r = requests.get('https://covid.ourworldindata.org/data/jhu/full_data.csv')
    file = open("./full_data.csv", "w")
    file.write(r.text)
    file.close()
#===================================
def dostepneKraje():
    with open("./full_data.csv") as file:
        dostepne = []
        poprzedni = "location"
        for linia in file:
            x = linia.split(",")
            if x[1]!=poprzedni:
                dostepne.append(x[1])
            poprzedni = x[1]
        return dostepne
#===================================
def daneZachorowań(kraj): 
    #Funkcję wywołujemy tylko pod warunkiem, że kraju nie ma w słowniku
    with open("./full_data.csv") as file:
        zachorowania = []
        flaga = False
        for linia in file:
            x = linia.split(",")
            if x[1] != kraj:
                if flaga==False:
                    continue
                else:
                    return zachorowania
            else:
                flaga = True
                print(linia.split(",")[2])
                if linia.split(",")[2] != None:
                    zachorowania.append(int(float(linia.split(",")[2])))             
#===================================
#Główny program
#===================================
#Sprawdzamy czy taki plik istnieje
czyPobranoNowy = False
print("Witaj w programie pokazującym liczbę zachorowań na COVID-19 w różnych krajach na świecie.")
try:
    tymczasowy = open("./full_data.csv")
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

if czyPobranoNowy == False:
    print("Wykryto dane ale mogą być nieaktualne.\n")
    odp = input("Czy chcesz pobrać nowe dane? y/n\n")
    if odp == "y":
        pobierzDane()


kraje = dostepneKraje()
for kk in kraje:
    print(kk)
przypadki = {}
while True:
    wybrany = input("Wybierz kraj z dostępnych na liście\n")
    if wybrany not in kraje:
        print("Nie ma kraju o tej nazwie")
    else:
        if wybrany not in przypadki:
            przypadki[wybrany] = daneZachorowań(wybrany) 
        dni = [ii+1 for ii in range(len(przypadki[wybrany]))] #To możnaby zoptymalizować
        robWykres(dni, przypadki[wybrany])