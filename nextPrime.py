#=========================================================================================
#Poniższą funkcję skopiowałem z udostępnionego nam repozytorium B.Zglinickiego,
#Funkcja była omawiana na zajęciach
#=========================================================================================
def isPrime(liczba):
    if liczba <= 3:
        return liczba > 1
    if  liczba % 2 == 0 or liczba % 3 == 0:
        return False
    i=5
    while i ** 2 <= liczba:
        if liczba % i == 0 or liczba % (i + 2) == 0:
            return False
        i += 6
    return True
#=========================================================================================    
def nextPrime(liczba):
    ii=1
    while isPrime(liczba+ii)!=True:
        ii+=1;
    return liczba+ii
#=========================================================================================
#Część właściwa programu
#=========================================================================================
n=int(input("Podaj liczbę naturalną:\n"))
print(nextPrime(n))