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
def liczX(V0, B, m, ile, interwał):
    for ii in range(ile):
        V0 = V0 - B*V0*V0*interwał/m
        yield V0
#======================================
def liczY(V0, B, m, ile, interwał):
    for ii in range(ile):
        V0 = V0 - np.sign(V0)*B*V0*V0*interwał/m - 9.81*interwał
        yield V0
#======================================
#Część główna programu
#======================================
INTERWAŁ = 0.1
dane = wczytajWartości()
ile = int(input())
szybkoscWPionie = dane["początkowa"]*math.sin( math.radians(dane["kąt"])  )
szybkoscWPoziomie = np.abs(dane["początkowa"]*math.cos( math.radians( dane["kąt"])) )

wynikX = list(liczX(szybkoscWPoziomie, dane["współczynnik"], dane["masa"], ile, INTERWAŁ))

wynikY = list(liczY(szybkoscWPionie, dane["współczynnik"], dane["masa"], ile, INTERWAŁ))


baza = np.arange(0, ile*INTERWAŁ , INTERWAŁ)

figX, axX = plt.subplots()
axX.plot(baza, wynikX)

figY, axY = plt.subplots()
axY.plot(baza,wynikY)

wartosci = [np.sqrt(wynikX[ii]**2 + wynikY[ii]**2) for ii in range(ile)]
fig, ax = plt.subplots()
ax.plot(baza, wartosci)
plt.show()