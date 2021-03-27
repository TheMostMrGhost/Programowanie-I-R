import matplotlib.pyplot as plt
#Wersja alpha, jeszcze nie ściąga informacji z internetu

#===================================
def dostepneKraje():
    with open("./full_data.csv") as file:
        poprzedni = "location"
        for linia in file:
            x = linia.split(",")
            if x[1]!=poprzedni:
                print(x[1])
            poprzedni = x[1]
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
                zachorowania.append(int(float(linia.split(",")[2])))             
#===================================
#Główny program
#===================================
print("Witaj w programie pokazującym liczbę zachorowań na COVID-19 w różnych krajach na świecie.\n Oto lista dostępnych " +
        "krajów:\n")
dostepneKraje()
przypadki = {}
wybrany = input("Wybierz kraj z dstępnych na liście\n")
chorzy = daneZachorowań(wybrany)
dni = [ii+1 for ii in range(len(chorzy))]
# for ee in range(len(chorzy)):
#     print(dni[ee], chorzy[ee])]
plt.plot(dni, chorzy)
plt.show()
plt.close()