import matplotlib.pyplot as plt, math, numpy as np, matplotlib.animation as animation
def dajInterwał():
    return 0.02
#======================================
def wczytajWartości():
    print("Witaj w programie wizualizującym ruch punktu materialnego w rzucie ukośnym")
    wynik = {}
    wynik.update({"masa" : float(input("Podaj masę ciała:\n"))})
    wynik.update({"wysokość" : float(input("Podaj wysokość z jakiej zrzucane jest ciało:\n"))})
    wynik.update({"współczynnik" : float(input("Podaj współczynnik oporu powietrza:\n"))})
    wynik.update({"początkowa" : float(input("Podaj prędkość początkową:\n"))})
    wynik.update({"kąt" : int(input("Podaj kąt (liczony od osi OX):\n"))})
    return  wynik
#======================================
def trajektoria(dane):
    interwał = dajInterwał()
    masa = dane["masa"]
    wysokość = dane["wysokość"]
    opór = dane["współczynnik"]
    szybX = dane["początkowa"]*np.cos(math.radians(dane["kąt"]))
    szybY = dane["początkowa"]*np.sin(math.radians(dane["kąt"]))

    wysokości = [wysokość]
    odległości = [0]
    ii = 1
    while wysokości[ii-1]>=0:
        szybY = szybY - np.sign(szybY)*opór*szybY*szybY*interwał/masa - 9.81*interwał
        wysokości.append(wysokości[ii-1] + szybY*interwał)
        szybX = szybX - opór*szybX*szybX*interwał/masa
        odległości.append(odległości[ii-1] + szybX*interwał)
        ii += 1
    return wysokości, odległości
#======================================
def droga(dane,ile):
    interwał = interwał()
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
def szukajMaksa(dane):#Ta funkcja jest po to żeby móc ładnie ustawić zakres na Y
    maks = - np.inf
    for ii in dane:
        if(ii>maks):
            maks = ii
    return maks
#======================================
#Część główna programu
#======================================
INTERWAŁ = dajInterwał() #Ogarnąć czy ten interwał można dawać jakiś większy czy zawsze taki
dane = wczytajWartości()

wysokości, odległości = trajektoria(dane)

fig, ax = plt.subplots(tight_layout = True)
ax.set_xlim(0, 11*odległości[-1]/10)
ax.set_ylim(0,11*szukajMaksa(wysokości)/10)

obj, = ax.plot([],[],'g', markersize = 3)
obj2, = ax.plot([],[], 'r.')
wykres = plt.get_current_fig_manager()
wykres.window.showMaximized()
xdata = []
ydata = []

def dajDane(i):
    xdata.append(odległości[i])
    ydata.append(wysokości[i])
    obj.set_data(xdata,ydata)
    obj2.set_data(odległości[i],wysokości[i])
    return obj, obj2

ani = animation.FuncAnimation(fig,dajDane,len(wysokości),interval = 20/len(wysokości), blit = True, repeat = False)
plt.show()