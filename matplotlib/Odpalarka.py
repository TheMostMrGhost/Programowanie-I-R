import projectile
with open("./Dane do rzutów.csv") as file:
    for linia in file:
        x = linia.split(",")
        projectile.main(x)