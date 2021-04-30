import Pliki, matplotlib.pyplot as plt, numpy as np, sys
class Kraj:
    # Tutal sobie ustalam jakie są domyślnie najważniejsze pola ale wykorzystywana funkcja jest ogólna
    def __init__(self,nazwa):
        self.nazwa = nazwa
        args = ("location","date","total_cases","new_cases","total_deaths","total_vaccinations")
        data = Pliki.wczytajKolumny(nazwa,*args) # Pomyśleć jeszcze jak to fajnie rozwiązać
        self.location = data[0]
        self.date = data[1]
        self.total_cases = data[2]
        self.new_cases = data[3]
        self.total_deaths = data[4]
        self.total_vaccinations = data[5]
    def wypiszNazwy(self):
        for ii in range(len(self.data)):
            print(self.data[ii])
    def wykresujSię(self, ludzie):
        dni = np.arange(0,len(self.date))
        plt.plot(dni, ludzie, 'g')
        plt.grid()
        plt.xlabel("Czas trwania epidemii (w dniach)")
        plt.ylabel("Liczba zakażonych w danym dniu")
        plt.legend("Nowi zakażeni")
        wykres = plt.get_current_fig_manager()
        wykres.window.showMaximized()
        plt.show()
        plt.close()