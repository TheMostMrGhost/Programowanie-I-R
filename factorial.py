import time
#====================================
def ifactorial(n):
    result=1
    while n>0:
        result*=n
        n-=1
    return result
#====================================
def rfactorial(n):
    if n<=1:
        return 1
    return rfactorial(n-1)*n
#====================================
#Dla małych wartości program zwraca podobne czasy wykonania, a dla większych dostajemy max recursion exceeded
def factorial(n):
    istart=time.perf_counter_ns()
    ires=ifactorial(n)
    istop=time.perf_counter_ns()
    print("Czas wykonywania wersji iteracyjnej: {0}\n Wynik: {1}".format(istop-istart,ires))

    rstart=time.perf_counter_ns()
    rres=rfactorial(n)
    rstop=time.perf_counter_ns()
    print("Czas wykonywania wersji rekurencyjnej: {0}\n Wynik: {1}".format(rstop-rstart,rres))

#====================================
#Program właściwy
#====================================
n=int(input("Podaj liczbę naturalną:\n"))
factorial(n)