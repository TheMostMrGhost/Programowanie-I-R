def main():
    def check(słowo):
        if fix(słowo) == 0:
            print("Ciąg nawiasów jest zbalansowany")
            return True
        else:
            print("Ciąg nawiasów nie jest zbalansowany")
            return False
    #=================================
    def fix(słowo):
        pasujace = {
           ')':'(',
            ']':'[',
            '}':'{'
        }
        stos = []
        licznik = 0
        ii = 0
        while ii < len(słowo):
            if słowo[ii] in ['(','{','[']:
                stos.append(słowo[ii])
                licznik += 1
            elif słowo[ii] in [')','}',']']:
                while len(stos) != 0 and stos[-1] != pasujace.get(słowo[ii]):
                    stos.pop(-1)
                if len(stos) != 0 and stos[-1] ==  pasujace.get(słowo[ii]):
                    stos.pop(-1)
                    licznik -= 1
            ii += 1
        return licznik
    #=================================
    def pairs(słowo, n):
        start = 0
        while start + 2*n <len(słowo)+1:
            podsłowo = ""
            pom = słowo[start:start + 2*n]
            for ii in pom:
                podsłowo += ii
            if fix(podsłowo) == 0:
                print(podsłowo)
            start += 1
    #=================================
    def wprowadź():
        wejście = input("Wprowadź ciąg nawiasów.\n")
        nawiasy = [wejście[ii] for ii in range(len(wejście))]
        return nawiasy
    #=================================
    # Część główna programu
    #=================================
    wejście = wprowadź()
    decyzja = input("Wybierz opcję\n")
    if decyzja == "fix":
        print(fix(wejście))
    elif decyzja == "check":
        check(wejście)
    elif decyzja == "list":
        n = int(input("Wprowadź n\n"))
        pairs(wejście,n)
if __name__== "__main__":
    main()