#Wersja alpha, jeszcze nie ściąga informacji z internetu

#===================================
def dostepneKraje():
    with open("./full_data.csv") as file:
        poprzedni = "location"
        for linia in file:
            x = linia.split(",")
            if x[1]!=poprzedni:
                print(x[1])
            poprzedni = x[1]
    #     return
    # data = []
    # x = lines[0]
    # print(lines[0])
    # print(type(x))
    # x = x.split(",")
    # print(x)
    # for ii in lines:
    #     data.append((lines[1].split(","))[2])
    # poprzedni = "location"
    # for e in data:
    #     if(e[2] != poprzedni):
    #         print(e[2])
    #     poprzedni = e[2]
    
#===================================
#Główny program
#===================================
print("Witaj w programie pokazującym liczbę zachorowań na COVID-19 w różnych krajach na świecie.\n Oto lista dostępnych " +
        "krajów:\n")
dostepneKraje()