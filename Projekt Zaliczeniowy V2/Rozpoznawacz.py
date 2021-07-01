import youtube_dl, cv2, pytesseract as pt, matplotlib.pyplot as plt, imutils, numpy as np
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
    def __init__(self, filename = None): #TODO dodać wybór formatu osobno TODO 2 usunąć inicjalizownaie plikiem 
        if filename != None:
            self.image = cv2.imread(filename, cv2.IMREAD_COLOR)# Robimy w odcieniach szarości bo inaczej wykrywacz świruje
        else:
            self.image = None
        
        self.textMain = ["Główny Ticker:"]
        self.textUnderMain = ["Ticker Dodatkowy:"]
        # FIXME poniższe usunąć
        self.slidingBarCoordinates = (975, 1050, 350, 1720)
        self.temporalSliding = [""]
        self.slidingText = []
    #====================================================================
    def __recognize(self, convert, startY = 0, endY = -1, startX = 0, endX = -1):
        if endX == -1:
            endX = self.image.shape[1]
        if endY == -1:
            endY = self.image.shape[0]
        try: # TODO usunąć to
            roi = self.image[startY:endY, startX:endX] 
        except TypeError:
            print(type(self.image)) 
            return
        config = ("-l pol --oem 2 --psm 7") # język polski, traktujamy całość wycinka jako tekst, wybór trybu pracy silnika Tesseract
        if convert: 
            # Główny ticker jest czerwono - biały, przez co Tesseract ma niekiedy problem z odczytaniem go.
            # Żeby polepszyć rozpoznawalność zmieniam czerwone tło na białe, a napisy na czarne
            roi = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
            whiteLower = np.array([50,50,50])
            whiteUpper = np.array([255,255,255])
            mask = cv2.inRange(roi, whiteLower, whiteUpper)
            roi[mask > 0] = (0,0,0)
            roi[mask == 0] = (255,255,255)
        else:
            roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        
        text = pt.image_to_string(roi) #FIXME sprawdzić czy to jest ok, config = config
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
        if self.mode >= 1:
            self.__recognizeMain()
        if self.mode >= 2:
            self.__recognizeUnderMain()
        # if self.mode >= 3:
        #     self.__recognizeSliding()
    #====================================================================
    def __recognizeMain(self):
        self.textMain.append(self.__recognize(True,*self.mainTickerCoordinates))
    #====================================================================
    def __recognizeUnderMain(self): # TODO zmienić tą nazwę na jakąś sensowną
        self.textUnderMain.append(self.__recognize(False,*self.underMainTickerCoordinates))
    # #====================================================================
    # #TODO usunąć
    # def __recognizeSliding(self):
    #     """Czyta z paska przesuwnego"""
    #     slidingBarCord = list(self.defaultCoordinates2)
    #     squarePosition = self.findSquare(*self.defaultCoordinates2)
    #     if squarePosition == None:
    #         self.temporalSliding.append(self.__recognize(*self.defaultCoordinates2))
    #     else:
    #         slidingBarLeft = slidingBarCord.copy()
    #         slidingBarRight = slidingBarCord.copy()
    #         slidingBarLeft[3] = slidingBarLeft[2] + squarePosition[0]
    #         slidingBarRight[2] = slidingBarRight[2] + squarePosition[0] + squarePosition[1]
    #         self.slidingText.append(self.__recognize(*slidingBarLeft))
    #         self.combine() # TODO sprawdzić czy w funkcji dałem że to się automatycznie dołącza do końca listy tekstów
    #         self.temporalSliding = []
    #         self.temporalSliding.append(self.__recognize(*slidingBarRight))
    #====================================================================
    def addFrameToAnalyze(self, image):
        self.image = image # TODO zmienić być może
    # #====================================================================
    # #TODO usunąć
    # def findSquare(self, startY, endY, startX, endX):
    #     image = self.image.copy()
    #     image = image[startY:endY, startX:endX]
    #     blurred = cv2.GaussianBlur(image, (5, 5), 3)
    #     thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
    #     cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #     cnts = imutils.grab_contours(cnts)
    #     kwadrat = None
    #     for c in cnts:
    #         czyKwadrat, wymiary = Rozpoznawacz.checkIfSquare(c)
    #         if czyKwadrat:
    #             kwadrat = wymiary
    #     return kwadrat
    #====================================================================
    def findTicker(self): # Konwencja: najpierw y potem x, ustawiamy gdzie są tickery

        def checkIfRectangle(krzywa):
            peri = cv2.arcLength(krzywa,True)
            approx = cv2.approxPolyDP(krzywa,0.05*peri,True)
            (x, y, w, h) = cv2.boundingRect(approx)

            if w > TICKERWIDTHLOWERBOUND and h < TICKERWIDTHUPPERBOUND:
                print(w,h)
                return True, (x, y, w, h)
            return False, (x, y, w, h)
        #================================================================
        # if self.image == None: # TODO zrobić to jakiś custom wyjątek
        #     return
        roi = self.image[UNDERMAINLOWER_Y:UNDERMAINUPPER_Y, UNDERMAINLOWER_X:]# TODO sprawdzić czy takie wymiary są ok
        roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(roi, (5, 5), 1)
        thresh = cv2.threshold(blurred,150,255,cv2.THRESH_BINARY)[1]
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        rectangle = None
        roiCopy = roi.copy()

        for c in cnts:
            isRectangle, mes = checkIfRectangle(c)
            if isRectangle:
                cv2.drawContours(roiCopy, [c], -1, (255, 0, 255), 5) # TODO usunąć
                # plt.imshow(roiCopy)
                # plt.show()
                rectangle = mes
        if rectangle != None:
            self.mainTickerCoordinates = (UNDERMAINLOWER_Y + rectangle[1] - MAINTICKERHEIGHT, 
            UNDERMAINLOWER_Y + rectangle[1], UNDERMAINLOWER_X + rectangle[0], self.image.shape[1])
            self.underMainTickerCoordinates = (UNDERMAINLOWER_Y + rectangle[1],
                UNDERMAINLOWER_Y + rectangle[1] + rectangle[3], UNDERMAINLOWER_X + UNDERMAINSQUARESIZE + rectangle[0],
                UNDERMAINLOWER_X + UNDERMAINSQUARESIZE + rectangle[0] + rectangle[2])
        else:
            self.underMainTickerCoordinates = DEFAULTUNDERMAINCOORDINATES # Jeżeli uda się znaleźć pasek PILNE to te wartości zostaną nadpisane, ale 
            # w przypadku błędu funkcji szukającej paska zostaną użyte te dane
        
            self.mainTickerCoordinates = (DEFAULTUNDERMAINCOORDINATES[0] - MAINTICKERHEIGHT, 
                    DEFAULTUNDERMAINCOORDINATES[0], DEFAULTUNDERMAINCOORDINATES[2] - UNDERMAINSQUARESIZE, self.image.shape[1])
    #====================================================================
    # FIXME strefa eksperymentalna
    #====================================================================
    # def combine(self):
    #     # FIXME Zrobić żeby działało i dodać jako opcję
    #     def attach(string, listOfStrings):
    #         for ii in listOfStrings:
    #             string += " " + ii
    #         return string
    #     #====================================================================
    #     def findWordInString(string, word):
    #         temp = string.split()
    #         ii = 0
    #         while ii< len(temp) and temp[ii] != word:
    #             ii+=1
    #         return ii
    #     #====================================================================
    #     res = ""
    #     if len(self.temporalSliding) == 0:
    #         return
    #     first = self.temporalSliding[0].split()
    #     if len(first)<=1:
    #         print("Co tu zrobić?") # TODO
    #         return
    #     res += first[0]
    #     for ii in range(1,len(first)):
    #         res += " " + first[ii]
    #     last = first[-2] # TODO być moze tu jest off by 1
    #     for ii in range(1,len(self.temporalSliding)-1):
    #         index = findWordInString(last,self.temporalSliding[ii])
    #         temp = self.temporalSliding[ii].split()
    #         if index < len(self.temporalSliding[ii]):
    #             res = attach(res,temp[index:-1])
    #         last = temp[-2] # TODO ogarnąć to off by 1
    #     # Obsługa ostatniego słowa
    #     index = findWordInString(last,self.temporalSliding[-1])
    #     temp = self.temporalSliding[-1].split()
    #     if index < len(self.temporalSliding[-1]):
    #         res = attach(res,temp[index:])
    #     self.slidingText.append(res)
    #====================================================================
    def selectMode(self, mode):
        self.mode = mode
    #====================================================================
    # #TODO usunąć
    # @staticmethod
    # def checkIfSquare(krzywa):
    #     peri = cv2.arcLength(krzywa,True)
    #     approx = cv2.approxPolyDP(krzywa,0.05*peri,True)
    #     if len(approx)!=4:
    #         return False, (0,0,0,0)
    #     (x, y, w, h) = cv2.boundingRect(approx)
    #     ar = w/float(h)
    #     if ar>0.87 and ar<1/0.87 and y>20 and y<32: # TODO sprawdzić czy to jest gites
    #         return True, (x, y, w, h)
    #     return False, (x, y, w, h)