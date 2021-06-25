import youtube_dl, cv2, pytesseract as pt, matplotlib.pyplot as plt

class Rozpoznawacz:
    def __init__(self, filename): #TODO dodać wybór formatu osobno
        self.image = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)# Robimy w odcieniach szarości bo inaczej wykrywacz świruje
        self.text = []
        self.defaultCoordinates1 = (910,970,510,1850)
        self.defaultCoordinates2 = (975,1050,350,1720)
    # Dane: Środkowy pasek: początekX = 510, koniecX = 1850, początekY = 910, koniecY = 970
# Dolny pasek: początekX = około 360, koniecX = 1720, początekY = 975, koniecY = 1050
    def recognize(self, show, startY, endY, startX, endX):
        try: # TODO usunąć to
            roi = self.image[startY:endY, startX:endX]
        except TypeError:
            print(type(self.image))
            return
        config = ("-l pol --oem 1 --psm 7") # język polski, traktujamy całość wycinka jako tekst, TODO to trzecie, wybór algorytmu szukającego chyba
        if show:
            plt.imshow(roi) # TODO wrzucić resize'a jakiegoś bo inaczej trochę świruje
            plt.show()
        self.text.append(pt.image_to_string(roi)) 
        self.validCharacters(-1)
    def validCharacters(self, index):
        """Sprawdza czy dany znak jest w miarę legalny""" # TODO Dodać lepszy opis
        polishCharacters = ['ą','ę','ś','ć','ó','ż','ź','ł',' ','!', ',', '.','?',':',';']
        res = ""
        for letter in self.text[index]: 
            temp = letter.lower()
            if (ord(temp)>64 and  ord(temp)<123) or (ord(temp)>47 and ord(temp) < 58) or temp in polishCharacters:
                res +=letter
        # TODO usunąć puste spacje
        res = res.strip()
        self.text[index] = res
    def changeImage(self, newFilename):
        print(newFilename)
        self.image = cv2.imread(newFilename, cv2.IMREAD_GRAYSCALE)
    def defaultRecognize(self, show):
        self.recognize(show,*self.defaultCoordinates1)
        self.recognize(show,*self.defaultCoordinates2)
        # """Rozpoznawanie wybranych przez autora fragmentów obrazu"""
    def sciągnijRamkę(self, newW, newH):
        (origH, origW) = self.image.shape[:2]
        rW = origW / float(newW)
        rH = origH / float(newH)
        self.image = cv2.resize(image, (newW, newH))
        (H, W) = self.image.shape[:2]
        print(origH, origW)
        print(H, W)
        