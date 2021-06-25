import Pliki, matplotlib.pyplot as plt, numpy as np, operator as op, Kraj
class Region:
    def __init__(self,name,*args):
        self.name = name
        self.location = ""
        self.date = args[0].date
        self.total_cases = []
        self.new_cases = []
        self.total_deaths = []
        self.total_vaccinations = []
        for ii in range(len(args[0].total_cases)): # Chyba działa ale trzeba to zrobić mapem i maksymalną długość brać, bo tak to to syfne jest
            totcas = 0
            newcas = 0
            totdeath = 0
            totvacc = 0
            for jj in range(len(args)):
                if ii < len(args[jj].total_cases):
                    totcas += args[jj].total_cases[ii]
                    newcas += args[jj].new_cases[ii]
                    totdeath += args[jj].total_deaths[ii]
                    totvacc += args[jj].total_vaccinations[ii]
            self.total_cases.append(totcas)
            self.new_cases.append(newcas)
            self.total_deaths.append(totdeath)
            self.total_vaccinations.append(totvacc)
    #=================================================
    def wykresujSię(self, ludzie, title = None):
        dni = np.arange(0,len(self.date))
        plt.plot(dni, ludzie, 'g')
        plt.grid()
        plt.xlabel("Czas trwania epidemii (w dniach)")
        plt.ylabel("Liczba zakażonych w danym dniu")
        if title != None:
            plt.title(title)
        wykres = plt.get_current_fig_manager()
        wykres.window.showMaximized()
        plt.show()
        plt.close()
    #=================================================
    def noweWykres(self):
        self.wykresujSię(self.new_cases)
    #=================================================
    def wszystkieWykres(self):
        self.wykresujSię(self.total_cases)
    #=================================================
    def wszystkieŚmierciWykres(self):
        self.wykresujSię(self.total_deaths)
    #=================================================
    def zaszczepieniWykres(self):
        self.wykresujSię(self.total_vaccinations)
    #=================================================
    def __add__(self,second):
        res = Region(self.name+ " " + second.name, self, second)
        return Kraj.Kraj.cast(res)
