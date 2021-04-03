import matplotlib.pyplot as plt, math, numpy as np
#======================================
def wczytajWartości():
    print("Witaj w programie wizualizującym ruch punktu materialnego w rzucie ukośnym")
    wynik = {}
    wynik.update({"masa" : float(input("Podaj masę ciała:\n"))})
    wynik.update({"wysokość" : float(input("Podaj wysokość z jakiej zrzucane jest ciało:\n"))})
    wynik.update({"współczynnik" : float(input("Podaj współczynnik oporu powietrza:\n"))})
    wynik.update({"początkowa" : float(input("Podaj prędkość początkową:\n"))})
    wynik.update({"kąt" : float(input("Podaj kąt (liczony od osi OX):\n"))})
    return  wynik
#======================================
def droga(dane,ile, interwał):
    def liczX(V0, B, m, ile, interwał):
        for ii in range(ile):
            print(V0)
            V0 = V0 - B*V0*V0*interwał/m
            yield V0

    def liczY(V0, B, m, ile, interwał):
        for ii in range(ile):
            V0 = V0 - np.sign(V0)*B*V0*V0*interwał/m - 9.81*interwał
            yield V0

    szybkoscWPionie = dane["początkowa"]*math.sin( math.radians(dane["kąt"])  )
    szybkoscWPoziomie = np.abs(dane["początkowa"]*math.cos( math.radians( dane["kąt"])) )

    print("Szybkość w pionie: {0}\n".format(szybkoscWPionie))
    print("Szybkość w poziomie: {0}\n".format(szybkoscWPoziomie))
    wynikX = list(liczX(szybkoscWPoziomie, dane["współczynnik"], dane["masa"], ile, interwał))
    wynikY = list(liczY(szybkoscWPionie, dane["współczynnik"], dane["masa"], ile, interwał))

    wysokości = [dane["wysokość"]]
    odległości = [0]
    ii = 1
    while wysokości[ii-1]>=0:
        wysokości.append(wysokości[ii-1] + wynikY[ii-1]*interwał)
        odległości.append(odległości[ii-1] + wynikX[ii-1]*interwał)
        ii+=1
    return wysokości, odległości
#======================================
#Część główna programu
#======================================
INTERWAŁ = 0.01
dane = wczytajWartości()
ile = int(input())

wysokości, odległości = droga(dane, ile,INTERWAŁ)
for ii in range(len(wysokości)):
    print("{0}   {1}".format(wysokości[ii], odległości[ii]))

fig, ax = plt.subplots()
ax.plot(odległości, wysokości)
plt.show()