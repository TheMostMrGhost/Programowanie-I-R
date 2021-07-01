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
    #====================================================================
    def __recognize(self, convert, startY = 0, endY = -1, startX = 0, endX = -1):
        if endX == -1:
            endX = self.image.shape[1]
        if endY == -1:
            endY = self.image.shape[0]
        try:
            roi = self.image[startY:endY, startX:endX] 
        except TypeError: # TODO polepszyć to
            print(type(self.image)) 
            return

        if convert:
            roi = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
            whiteLower = np.array([50,50,50])
            whiteUpper = np.array([255,255,255])
            mask = cv2.inRange(roi, whiteLower, whiteUpper)
            roi[mask > 0] = (0,0,0)
            roi[mask==0] = (255,255,255)
            # plt.imshow(roi) # TODO wrzucić resize'a jakiegoś bo inaczej trochę świruje
            # plt.show()
        else:
            roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        
        text = pt.image_to_string(roi)
        return Rozpoznawacz.validCharacters(text)
    #====================================================================
    @staticmethod
    def validCharacters(text):
        """Sprawdza czy dany znak jest w miarę legalny""" # TODO Dodać lepszy opis
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
    #====================================================================
    def __recognizeMain(self):
        self.textMain.append(self.__recognize(True,*self.mainTickerCoordinates))
    #====================================================================
    def __recognizeUnderMain(self): # TODO zmienić tą nazwę na jakąś sensowną
        self.textUnderMain.append(self.__recognize(False,*self.underMainTickerCoordinates))
    #====================================================================
    def addFrameToAnalyze(self, image):
        self.image = image # TODO zmienić być może
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
        roi = self.image[UNDERMAINLOWER_Y:UNDERMAINUPPER_Y, UNDERMAINLOWER_X:]
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
    def selectMode(self, mode):
        self.mode = mode