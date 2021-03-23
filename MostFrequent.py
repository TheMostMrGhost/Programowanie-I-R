def mostFrequent(lista):
    słownik={}
    for el in lista:
        if str(el) not in słownik:
            słownik[str(el)]=1
        else:
            słownik[str(el)]+=1
    ktoryToMaks=str(lista[0])
    maks=słownik[str(lista[0])]
    akt=0
    print(słownik)
    for el in słownik:
        akt=słownik[el]
        if akt>maks:
            maks=akt
            ktoryToMaks=el
    return ktoryToMaks
#=======================================
listka=[4,5,3,3,3,9,9,9,9,"a","a","a","a","a"]
print(mostFrequent(listka))