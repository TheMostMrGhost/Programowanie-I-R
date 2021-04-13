def main():
    def check(otwierające, zamykające):
        pasujace = {
            '(':')',
            '[':']',
            '{':'}'
        }
        if len(otwierające) != len(zamykające):
            print("Ciąg nawiasów nie jest zbalansowany")
            return
        while len(otwierające) != 0 :
            otw = otwierające.pop(len(otwierające)-1)
            zam = zamykające.pop(len(zamykające)-1)
            if zam != pasujace.get(otw):
                print("Ciąg nawiasów nie jest zbalansowany")
        print("Ciąg nawiasów jest zbalansowany")

    #=================================
    # def fix():

    #=================================
    # def pairs():

    #=================================
    def wprowadź():
        wejście = input("Wprowadź ciąg nawiasów.\n")
        nawiasy = [wejście[ii] for ii in range(len(wejście))]
        return nawiasy
    #=================================
    def dziel(nawiasy):
        otwierające = []
        zamykające = []
        for ii in nawiasy:
            if ii in ['(','{','[']:
                otwierające.append(ii)
            elif ii in [')','}',']']:
                zamykające.append(ii)
            else:
                print("Wyrażenie zawiera znaki inne niż nawiasy, przerywam pracę.")
                exit()
        return otwierające, zamykające
    #=================================
    wejście = wprowadź()
    otwierające, zamykające = dziel(wejście)
    check(otwierające, zamykające)

if __name__== "__main__":
    main()