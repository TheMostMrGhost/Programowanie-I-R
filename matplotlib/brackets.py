def main():
    def check(słowo):
        pasujace = {
           ')':'(',
            ']':'[',
            '}':'{'
        }
        stos = []
        czyjJestGit = True
        for ii in range(len(słowo)):
            if słowo[ii] in ['(','{','[']:
                stos.append(słowo[ii])
            elif słowo[ii] in [')','}',']']:
                if stos.pop(-1) != pasujace.get(słowo[ii]):
                    czyjJestGit = False
                    break
        if czyjJestGit:
            print("Ciąg nawiasów jest zbalansowany")
        else:
            print("Ciąg nawiasów nie jest zbalansowany")
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
        while ii <len(słowo):
            if słowo[ii] in ['(','{','[']:
                stos.append(słowo[ii])
            elif słowo[ii] in [')','}',']']:
                while len(stos) != 0 and stos[-1] != słowo[ii]:
                    licznik += 1
                    stos.pop(-1)
                if stos[-1] == słowo[ii]:
                    stos.pop(-1)
            ii += 1
        licznik += len(słowo) - ii
        return licznik
    #=================================
    # def pairs():

    #=================================
    def wprowadź():
        wejście = input("Wprowadź ciąg nawiasów.\n")
        nawiasy = [wejście[ii] for ii in range(len(wejście))]
        return nawiasy
    #=================================
    # def dziel(nawiasy):
    #     otwierające = []
    #     zamykające = []
    #     for ii in nawiasy:
    #         if ii in ['(','{','[']:
    #             otwierające.append(ii)
    #         elif ii in [')','}',']']:
    #             zamykające.append(ii)
    #         else:
    #             print("Wyrażenie zawiera znaki inne niż nawiasy, przerywam pracę.")
    #             exit()
    #     return otwierające, zamykające
    #=================================
    wejście = wprowadź()
    check(wejście)

if __name__== "__main__":
    main()