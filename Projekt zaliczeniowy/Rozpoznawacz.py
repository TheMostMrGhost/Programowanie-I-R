import youtube_dl, cv2, pytesseract as pt, matplotlib.pyplot as plt, imutils

class Rozpoznawacz:
    def __init__(self, filename = None): #TODO dodać wybór formatu osobno TODO 2 usunąć inicjalizownaie plikiem
        if filename != None:
            self.image = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)# Robimy w odcieniach szarości bo inaczej wykrywacz świruje
        else:
            self.image = None
        # print(self.image.shape)
        self.text = []
        self.slidingText = [""]
        self.defaultCoordinates1 = (910,970,510,1850)
        self.defaultCoordinates2 = (975,1050,350,1720)
        self.licznikQuadratow = 0 # FIXME usunąć to
    #====================================================================
    # Dane: Środkowy pasek: początekX = 510, koniecX = 1850, początekY = 910, koniecY = 970
# Dolny pasek: początekX = około 360, koniecX = 1720, początekY = 975, koniecY = 1050
    def recognize(self, show, startY = 0, endY = -1, startX = 0, endX = -1):
        if endX == -1:
            endX = self.image.shape[1]
        if endY == -1:
            endY = self.image.shape[0]
        try: # TODO usunąć to
            roi = self.image[startY:endY, startX:endX] 
        except TypeError:
            print(type(self.image)) 
            return
        config = ("-l pol --oem 2 --psm 7") # język polski, traktujamy całość wycinka jako tekst, TODO to trzecie, wybór algorytmu szukającego chyba
        if show:
            plt.imshow(roi) # TODO wrzucić resize'a jakiegoś bo inaczej trochę świruje
            plt.show()
        text = pt.image_to_string(roi)
        return Rozpoznawacz.validCharacters(text)
    #====================================================================
    @staticmethod
    def validCharacters(text):
        """Sprawdza czy dany znak jest w miarę legalny""" # TODO Dodać lepszy opis
        polishCharacters = ['ą','ę','ś','ć','ó','ż','ź','ł',' ','!', ',', '.','?',':',';','Ł','Ż','Ą','Ę','Ź','Ś','Ć']
        res = ""
        for letter in text: 
            temp = letter.lower()
            if (ord(temp)>64 and  ord(temp)<123) or (ord(temp)>47 and ord(temp) < 58) or temp in polishCharacters:
                res +=letter
        return res.strip()
    #====================================================================
    def changeImage(self, newFilename):
        self.image = cv2.imread(newFilename, cv2.IMREAD_GRAYSCALE)
    #====================================================================
    def defaultRecognize(self, show):
        self.text.append(self.recognize(show, *self.defaultCoordinates1))
        self.text.append(self.recognize(show, *self.defaultCoordinates2))
        # """Rozpoznawanie wybranych przez autora fragmentów obrazu"""
    # def sciągnijRamkę(self, newW, newH): #TODO zmienić nazwe
    #     (origH, origW) = self.image.shape[:2]
    #     rW = origW / float(newW)
    #     rH = origH / float(newH)
    #     self.image = cv2.resize(image, (newW, newH))
    #     (H, W) = self.image.shape[:2]
    #     print(origH, origW)
    #     print(H, W)
    #====================================================================
    def upgradedRecognize(self, show):
        self.text.append(self.recognize(show, *self.defaultCoordinates1))
        self.recognizeSliding(show)
    #====================================================================
    def recognizeSliding(self, show):
        """Czyta z paska przesuwnego"""
        slidingBarCord = list(self.defaultCoordinates2)
        # x = self.defaultCoordinates2[0]
        # y = self.defaultCoordinates2[1]
        # z = self.defaultCoordinates2[2]
        # t = self.defaultCoordinates2[3]
        # xd = self.image[x:y, z: t]
        # plt.imshow(xd)
        # plt.show()
        squarePosition = self.findSquare(*self.defaultCoordinates2)
        if squarePosition == None:
            self.slidingText[-1] += self.recognize(show, *self.defaultCoordinates2)
        else:
            slidingBarLeft = slidingBarCord.copy()
            slidingBarRight = slidingBarCord.copy()
            slidingBarLeft[3] = slidingBarLeft[2] + squarePosition[0]
            slidingBarRight[2] = slidingBarRight[2] + squarePosition[0] + squarePosition[1]
            self.slidingText[-1] += self.recognize(show, *slidingBarLeft)
            self.slidingText.append(self.recognize(show, *slidingBarRight))
    #====================================================================
    def addFrameToAnalyze(self, image):
        self.image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    #====================================================================
    def findSquare(self, startY, endY, startX, endX):
        image = self.image.copy()
        image = image[startY:endY, startX:endX]
        blurred = cv2.GaussianBlur(image, (5, 5), 3)
        thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        kwadrat = None
        for c in cnts:
            czyKwadrat, wymiary = Rozpoznawacz.checkIfSquare(c)
            if czyKwadrat:
                kwadrat = wymiary
                self.licznikQuadratow +=1
        return kwadrat
    #====================================================================
    @staticmethod
    def checkIfSquare(krzywa):
        peri = cv2.arcLength(krzywa,True)
        approx = cv2.approxPolyDP(krzywa,0.05*peri,True)
        if len(approx)!=4:
            return False, (0,0,0,0)
        (x, y, w, h) = cv2.boundingRect(approx)
        ar = w/float(h)
        # print(ar)
        # print((x, y, w, h))
        if ar>0.87 and ar<1/0.87 and y>20 and y<32: # TODO sprawdzić czy to jest gites
            return True, (x, y, w, h)
        return False, (x, y, w, h)