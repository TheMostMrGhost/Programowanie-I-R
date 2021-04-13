def main():
    def check(słowo):
        if fix(słowo) == 0:
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
    #def pairs(słowo):

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
    # Część główna programu
    #=================================
    wejście = wprowadź()
    check(wejście)
    print(fix(wejście))
if __name__== "__main__":
    main()