def Fibb(n):
    if (n==1):
        return 1, 0
    poprzednia, przedpoprzednia=Fibb(n-1)
    return poprzednia+przedpoprzednia, poprzednia
#=================================================================
n=int(input("podaj naturala:\n"))
while n>0:
    print(Fibb(n)[0])
    n=int(input("podaj naturala:\n"))

ii=2
fibo=Fibb(ii)[0]
suma=0
while fibo<3E6:
    fibo=Fibb(ii)[0]
    suma+=fibo
    ii+=2
print(suma)