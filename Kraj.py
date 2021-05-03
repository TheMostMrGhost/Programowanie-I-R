import Pliki, matplotlib.pyplot as plt, numpy as np, Region
class Kraj(Region.Region):
    # Tutaj sobie ustalam jakie są domyślnie najważniejsze pola ale wykorzystywana funkcja jest ogólna
    def __init__(self,name = None): # Dlaczego Python nie wspomaga przeciążania konstruktorów, no dlaczego?!
        if name == None:
            self.name = "No name"
            self.location = None
            self.date = None
            self.total_cases = None
            self.new_cases = None
            self.total_deaths = None
            self.total_vaccinations = None
        else:
            self.name = name
            args = ("location","date","total_cases","new_cases","total_deaths","total_vaccinations")
            data = Pliki.wczytajKolumny(name,*args) # Pomyśleć jeszcze jak to fajnie rozwiązać
            self.location = data[0]
            self.date = data[1]
            self.total_cases = data[2]
            self.new_cases = data[3]
            self.total_deaths = data[4]
            self.total_vaccinations = data[5]
    #=================================================
    def __getitem__(self,key):
        if key == "location":
            return self.location
        elif key == "total_cases":
            return self.total_cases
        elif key == "new_cases":
            return self.new_cases
        elif key == "total_deaths":
            return self.total_deaths
        elif key == "total_vaccinations":
            return self.total_vaccinations
        else:
            return None
    #=================================================
    def średnia7Dniowa(self, key):
        tab = self[key]
        tab = tab[len(tab) - 7:]
        return sum(tab)/7
    #=================================================
    def noweŚrednia(self):
        return self.średnia7Dniowa("new_cases")
    #=================================================
    def piszDoPliku(self,key): #TODO usunąć ją jak nowa metoda zadziała
        file = open("./" + self.name + key + ".csv","w")
        res = ""
        temp = self[key]
        for ii in temp:
            res += str(ii) + ","
        file.write(res)
        file.close()
    #=================================================
    def piszPlik(self,key):
        Pliki.zapiszKolumnę(self,key,'.csv')
    #=================================================
    def __repr__(self):
        return self.name
    #=================================================
    @staticmethod
    def cast(region):
        res = Kraj()
        res.name = region.name
        res.location = region.location
        res.date = region.date
        res.total_cases = region.total_cases
        res.new_cases = region.new_cases
        res.total_deaths = region.total_deaths
        res.total_vaccinations = region.total_vaccinations
        return res
#=================================================
def szukajKraju(listaKrajów, nazwa):
    for ii in listaKrajów:
        if ii.name == nazwa:
            return ii
    return None