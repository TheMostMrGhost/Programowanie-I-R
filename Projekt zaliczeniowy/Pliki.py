import youtube_dl, cv2, pytesseract as pt, Rozpoznawacz as roz, os, shutil

DEFAULTPARSINGTIME = 6

class Plik:
    def __init__(self, url, filename):
        self.url = url
        self.filename = filename
        self.pathToFolder = "./"+self.filename + "Dir"
        self.numberOfFiles = 34
        self.isFileBroken = False
    #====================================================================
    def download(self):
        try:
            os.mkdir(self.pathToFolder)
        except FileExistsError:
            pass
        ydl_opts = {
            'outtmpl': self.pathToFolder + "/" + self.filename + '.mp4',
            'format': 'mp4',
            'quiet': True,
            'no_warnings': True,

        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([self.url])
            except youtube_dl.utils.DownloadError: # TODO naprawić to żeby się błąd nie wypisywał, tylko moja wiadomość
                print("Pobieranie nie powiodło się.")
                self.isFileBroken = True
    #====================================================================
    def hlp(self):#TODO usunąć to
        help(youtube_dl.YoutubeDL)
    #====================================================================
    def parser(self, timeInterval = DEFAULTPARSINGTIME):
        video = cv2.VideoCapture(self.pathToFolder + "/" + self.filename + '.mp4')
        fps = video.get(cv2.CAP_PROP_FPS) # Informacja o klatkach na sekundę, bo chcemy ciąć co 5(chyba, że zmienię w końcowej wersji) sekund
        ii = 0 
        jj = 0 # To jest do licznia ile klatek zapisałem jako pliki
        anyFramesLeft, frame = video.read()
        while anyFramesLeft:
            cv2.imwrite(self.pathToFolder + "/" + "frame{0}.jpg".format(jj), frame)
            jj += 1
            kk = 0
            while anyFramesLeft and kk < timeInterval*fps - 1:
                anyFramesLeft, frame = video.read()
                kk += 1
        self.numberOfFiles = jj
    #====================================================================
    def analyzeVideo(self, show):
        # TODO usunąć to w cholerę
        recog = roz.Rozpoznawacz(self.pathToFolder + "/" + "frame0.jpg")
        for ii in range(1,self.numberOfFiles+1):
            recog.defaultRecognize(show)
            recog.changeImage(self.pathToFolder + "/" + "frame" + str(ii) +".jpg") # TODO zmienić to ewentualnie bo to trochę dziwnie wygląda
        self.writeStringsToFile(recog.text,self.filename)
    #====================================================================
    def writeStringsToFile(self, strings): # TODO ulepszyć, żeby można było dużo stringów na raz zapisać
        """Zapisuje do pliku teksty, usuwa powtórzenia"""
        if len(strings)<1:
            return
        with open(self.filename + " Wycięte Teksty.txt",'a') as file:
            alreadySavedTexts = []
            for ii in strings:
                if ii not in alreadySavedTexts:
                    file.write(ii+"\n")
                    alreadySavedTexts.append(ii)
    #====================================================================
    def cleanAfterWork(self):
        shutil.rmtree(self.pathToFolder)
    #====================================================================
    def analyzeLive(self, show = False, timeInterval = DEFAULTPARSINGTIME):
        video = cv2.VideoCapture(self.pathToFolder + "/" + self.filename + '.mp4')
        fps = video.get(cv2.CAP_PROP_FPS)
        anyFramesLeft = True
        analyzer = roz.Rozpoznawacz("nic")# TODO usunąć to 
        while anyFramesLeft:
            anyFramesLeft, frame = video.read()
            analyzer.addFrameToAnalyze(frame)
            analyzer.defaultRecognize(False)
            self.writeStringsToFile(analyzer.text)
            jj = 0
            for jj in range(int(timeInterval*fps - 1)):
                anyFramesLeft, frame = video.read()
    #====================================================================
    def upgradedAnalyzeLive(self, mode = 1, timeInterval = DEFAULTPARSINGTIME):
        if self.isFileBroken:
            return
        video = cv2.VideoCapture(self.pathToFolder + "/" + self.filename + '.mp4')
        fps = video.get(cv2.CAP_PROP_FPS)
        analyzer = roz.Rozpoznawacz()
        anyFramesLeft, frame = video.read() # TODO ogarnąć jakieś błędy
        analyzer.addFrameToAnalyze(frame)
        analyzer.findTicker()
        analyzer.selectMode(mode)
        if mode == 1:
            timeInterval = 40 # TODO sprawdzić czy takie czasy są ok
        if mode == 2:
            timeInterval = 8

        while anyFramesLeft:
            anyFramesLeft, frame = video.read()
            analyzer.addFrameToAnalyze(frame)
            analyzer.recognize()

            for jj in range(int(timeInterval*fps - 1)):
                anyFramesLeft, frame = video.read()

        if mode >= 1:
            self.writeStringsToFile(analyzer.textMain)
            print("Tryb 1")
        if mode >= 2:
            self.writeStringsToFile(analyzer.textUnderMain)
            print("Tryb 2")
        if mode >= 3: 
            self.writeStringsToFile(analyzer.slidingText)
            print("Tryb 3")