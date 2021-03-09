a=float(input("Podaj współczynnik a prostej\n"))
b=float(input("Podaj współczynnik b prostej\n"))

if(a==0):
    if(b==0):
        print("Dowolna liczba rzeczywista jest rozwiązaniem tego równania liniowego")
    else:
        print("Równanie nie ma rozwiązań")
else:
    print("x={0}".format(-b/a))