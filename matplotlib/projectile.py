import matplotlib.pyplot as plt, math, numpy as np, matplotlib.animation as animation

def dajInterwał():
    return 0.01
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
def trajektoria(dane,interwał = dajInterwał()):
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
def szukajMaksa(dane):#Ta funkcja jest po to żeby móc ładnie ustawić zakres na Y
    maks = - np.inf
    for ii in dane:
        if(ii>maks):
            maks = ii
    return maks
#======================================
def szukajOptymalnegoPrzedziału(dane):
    optymalny = dajInterwał()
    wysokości, odległości = trajektoria(dane)
    for ii in range(10):
        wysokości, odległości = trajektoria(dane,optymalny)
        if(len(wysokości)<400):
            optymalny /=2
        elif(len(wysokości)>800):
            optymalny *=2
        else:
            return optymalny
    return optymalny
#======================================
def przygotujWykres(wysMaks, odlMaks):
    ax.set_xlim(0, 11*odlMaks/10)
    ax.set_ylim(0,11*wysMaks/10)
    ax.set_xlabel("Odległość [m]", fontsize = 15)
    ax.set_ylabel("Wysokość [m]", fontsize = 15)
    ax.set_title(r"Rzut ukośny ciała z oporem $\sim V^2$", fontsize = 20)
    wykres = plt.get_current_fig_manager()
    wykres.window.showMaximized()
#======================================
#Część główna programu
#======================================
dane = wczytajWartości()
INTERWAŁ = szukajOptymalnegoPrzedziału(dane)
wysokości, odległości = trajektoria(dane, INTERWAŁ)

hmax = szukajMaksa(wysokości)

fig, ax = plt.subplots(tight_layout = True)
obj, = ax.plot([],[],'g', markersize = 3)
obj2, = ax.plot([],[], 'ro', markersize = 10)
czas = ax.annotate(0, xy=(1, 1), xytext=( odległości[1],wysokości[-10]))

xdata = []
ydata = []

def dajDane(i):
    xdata.append(odległości[i])
    ydata.append(wysokości[i])
    obj.set_data(xdata,ydata)
    obj2.set_data(odległości[i],wysokości[i])
    licznik = i*INTERWAŁ
    licznik = round(licznik, -int(np.log10(INTERWAŁ)))
    czas.set_text("Czas spadku [s]:\n      " + str(licznik))
    return obj, obj2, czas


ani = animation.FuncAnimation(fig,dajDane,len(wysokości),interval = 20/len(wysokości), blit = True, repeat = False, init_func =przygotujWykres(hmax,odległości[-1]))
plt.show()