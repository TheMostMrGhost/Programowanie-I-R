import numpy as np
a=float(input("Podaj współczynnik a równania kwadratowego\n"))
b=float(input("Podaj współczynnik b\n"))
c=float(input("Podaj współczynnik c\n"))

if(a==0):
    print("To nie jest równanie kwadratowe")
else:
    delta=b**2-4*a*c
    if(delta<0):
        print("Rozwiązaniami równania są: {0} -{1}i i {0}+{1}i".format(-b/(2*a), np.sqrt(-delta)/(2*a)))
    else:
        print("Rozwiązaniami równania są: {0} -{1} i {0}+{1}".format(-b/(2*a), np.sqrt(delta)/(2*a)))