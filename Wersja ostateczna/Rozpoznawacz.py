import youtube_dl, cv2, pytesseract as pt, matplotlib.pyplot as plt, imutils, numpy as np, sys
#====================================================================
TICKERWIDTHLOWERBOUND = 1000
TICKERWIDTHUPPERBOUND = 75
UNDERMAINLOWER_Y = 780
UNDERMAINUPPER_Y = 1100
UNDERMAINLOWER_X = 340
MAINTICKERHEIGHT = 110
UNDERMAINSQUARESIZE = 60 # W pasku PILNE jest taki mały prostokąt na początku linii i tesseract go czyta, trzeba go pominąć
DEFAULTUNDERMAINCOORDINATES = (970, 1040, 420, 1700)
#====================================================================
class Rozpoznawacz:
    def __init__(self, filename = None):
        if filename != None:
            self.image = cv2.imread(filename, cv2.IMREAD_COLOR)
        else:
            self.image = None
        
        self.textMain = ["Główny Ticker:"]
        self.textUnderMain = ["Ticker Dodatkowy:"]
    #====================================================================
    def __recognize(self, convert, startY = 0, endY = -1, startX = 0, endX = -1):
        """Rozpoznaje tekst z wskazanego obszaru danego obrazu"""
        if endX == -1:
            endX = self.image.shape[1]
        if endY == -1:
            endY = self.image.shape[0]
        try:
            roi = self.image[startY:endY, startX:endX] 
        except TypeError: 
            sys.stderr.write("Błąd rozpoznawania, upenij się, że wskazany obraz istnieje.")
            return

        # Wyróżnienie poniższych przypadków wynika stąd, że tiker główny to biały tekst na czerwonym tle i prawdopodobnie przez 
        # słaby kontrast powoduje to, że tesseract często błędnie rozpoznaje tekst. By to poprawić zamieniam kolor czerwony na biały, a kolor napisów na czarny.
        # Tikcer dodatkowy jest dobrze czytelny, w jeg przypadku nic nie trzeba zmieniać
        if convert:
            roi = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
            whiteLower = np.array([50,50,50])
            whiteUpper = np.array([255,255,255])
            mask = cv2.inRange(roi, whiteLower, whiteUpper)
            roi[mask > 0] = (0,0,0)
            roi[mask==0] = (255,255,255)
        else:
            roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        
        text = pt.image_to_string(roi)
        return Rozpoznawacz.validCharacters(text)
    #====================================================================
    @staticmethod
    def validCharacters(text):
        """Sprawdza czy znaki odczytane przez silnik Tesseract należą do alfabetu polskiego"""
        polishCharacters = ['ą','ę','ś','ć','ó','ż','ź','ł',' ','!', ',', '.','|','?',':',';']
        res = ""
        for letter in text: 
            temp = letter.lower()
            if (ord(temp)>64 and  ord(temp)<123) or (ord(temp)>47 and ord(temp) < 58) or temp in polishCharacters:
                res += letter
        return res.strip()
    #====================================================================
    def recognize(self):
        """Wybiera odpowiedni tryb rozpoznawania tekstu"""
        if self.mode >= 1:
            self.__recognizeMain()
        if self.mode >= 2:
            self.__recognizeUnderMain()
    #====================================================================
    def __recognizeMain(self):
        self.textMain.append(self.__recognize(True,*self.mainTickerCoordinates))
    #====================================================================
    def __recognizeUnderMain(self):
        self.textUnderMain.append(self.__recognize(False,*self.underMainTickerCoordinates))
    #====================================================================
    def addFrameToAnalyze(self, image):
        self.image = image
    #====================================================================
    def findTicker(self): 
        """Znajduje położenie małego tickera i na jego podstawie określa położenie dużego"""
        # Konwencja zapisu współrzędnych podczas wycinania fragmentu obrazu: najpierw y potem x

        # Zdecydowałem się na poszukiwanie tickera dodatkowego zamiast głównego, bo ticker główny ,,dotyka'' lewej krawędzi obrazu, 
        # przez co cv2 nie jest w stanie go rozpoznać. Ticker dodatkowy bardzo wyróżnia się z tła i występuje w każdym programie, 
        # a poza tym na podstawie jego połozenia łatwo jest ustalić położenie tickera głównego, bo ich położenie względne się nie zmienia
        def checkIfRectangle(krzywa):
            peri = cv2.arcLength(krzywa,True)
            # Kształt dopasowania nie jest do końca ważny, liczy się tylko czy otaczający prostokąt ma odpowiednie wymiary (wymiary tikerów są niezmienne)
            approx = cv2.approxPolyDP(krzywa,0.05*peri,True)
            (x, y, w, h) = cv2.boundingRect(approx)

            if w > TICKERWIDTHLOWERBOUND and h < TICKERWIDTHUPPERBOUND:
                return True, (x, y, w, h)
            return False, (x, y, w, h)
        #================================================================
        # Definiuję obaszar w granicach którego znajduje się ticker, przygotowuję obraz do szukania ram tickera
        roi = self.image[UNDERMAINLOWER_Y:UNDERMAINUPPER_Y, UNDERMAINLOWER_X:]
        roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(roi, (5, 5), 1)
        thresh = cv2.threshold(blurred, 150, 255, cv2.THRESH_BINARY)[1]
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        rectangle = None
        # Podczas szukania znajdujemy dużo konturów ale z nich wybieramy ten spełniający warunki na ticker pomocniczy
        for c in cnts:
            isRectangle, mes = checkIfRectangle(c)
            if isRectangle:
                rectangle = mes

        # Ustalam położenie bezwzględne poszczególych tickeró (bo cv2 szukając w roi traktuje je tak jakby to był nowy obraz)
        if rectangle != None:
            self.mainTickerCoordinates = (UNDERMAINLOWER_Y + rectangle[1] - MAINTICKERHEIGHT, 
            UNDERMAINLOWER_Y + rectangle[1], UNDERMAINLOWER_X + rectangle[0], self.image.shape[1])
            self.underMainTickerCoordinates = (UNDERMAINLOWER_Y + rectangle[1],
                UNDERMAINLOWER_Y + rectangle[1] + rectangle[3], UNDERMAINLOWER_X + UNDERMAINSQUARESIZE + rectangle[0],
                UNDERMAINLOWER_X + UNDERMAINSQUARESIZE + rectangle[0] + rectangle[2])
        else:
            self.underMainTickerCoordinates = DEFAULTUNDERMAINCOORDINATES 
            # Jeżeli uda się znaleźć pasek PILNE to te wartości zostaną nadpisane, ale 
            # w przypadku błędu funkcji szukającej paska zostaną użyte domyślne dane
        
            self.mainTickerCoordinates = (DEFAULTUNDERMAINCOORDINATES[0] - MAINTICKERHEIGHT, 
                    DEFAULTUNDERMAINCOORDINATES[0], DEFAULTUNDERMAINCOORDINATES[2] - UNDERMAINSQUARESIZE, self.image.shape[1])
    #====================================================================
    def setMode(self, mode):
        """Ustawienie trybu rozpoznawania"""
        # Wiem, że atrybuty w Pythonie są publiczne ale lepszym strukturalnie wydaje mi się myślenie, że tak nie jest, stąd setter
        self.mode = mode