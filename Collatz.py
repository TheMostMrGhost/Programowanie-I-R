#=====================================================================
def obrotyCollatza(n):
    def decyzja(n):
        if n%2==0:
            return int(n/2)
        return 3*n+1
    licznik=1
    while n!=1:
        n=decyzja(n)
        print(n)
        licznik+=1
    return licznik
#=====================================================================
def licznikCollatza(n):
    def decyzja(n):
        if n%2==0:
            return int(n/2)
        return 3*n+1
    licznik=1
    while n!=1:
        n=decyzja(n)
        licznik+=1
    return licznik
#=====================================================================
def lcollatz():
    maks=0
    liczba=0
    ii=1
    while ii<1000000:
        ile=licznikCollatza(ii+1)
        if maks<ile: 
            maks=ile
            liczba=ii
        ii+=1
        print(ii)
    return liczba
#837798
#=====================================================================
n=int(input())
obrotyCollatza(n)
#print(lcollatz())
print(obrotyCollatza(837798))