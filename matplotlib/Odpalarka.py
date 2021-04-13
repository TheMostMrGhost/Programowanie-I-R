import projectile
odKtorego = int(input("Od którego pomiaru zacząć?\n"))
ii = 1
with open("./Dane do rzutów.csv") as file:
    for linia in file:
        ii +=1
        x = linia.split(",")
        if ii >odKtorego:
            projectile.main(x)
        