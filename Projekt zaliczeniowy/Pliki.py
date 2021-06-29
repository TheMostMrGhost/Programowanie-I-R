import youtube_dl, cv2, pytesseract as pt, Rozpoznawacz as roz, os, shutil

DEFAULTPARSINGTIME = 7

class Plik:
    def __init__(self, url, filename):
        self.url = url
        self.filename = filename
        self.pathToFolder = "./"+self.filename + "Dir"
        self.numberOfFiles = 34
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
            'writedescription': True, # Czy to jest potrzebne?
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([self.url])
            except youtube_dl.utils.DownloadError: # TODO naprawić to żeby się błąd nie wypisywał, tylko moja wiadomość
                print("Pobieranie nie powiodło się.")
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
        recog = roz.Rozpoznawacz(self.pathToFolder + "/" + "frame0.jpg")
        for ii in range(1,self.numberOfFiles+1):
            recog.defaultRecognize(show)
            recog.changeImage(self.pathToFolder + "/" + "frame" + str(ii) +".jpg") # TODO zmienić to ewentualnie bo to trochę dziwnie wygląda
        self.writeStringsToFile(recog.text,self.filename)
    #====================================================================
    def writeStringsToFile(self, strings, filename):
        """Zapisuje do pliku teksty, usuwa powtórzenia"""
        if len(strings)<1:
            return
        with open(filename + " Wycięte Teksty.txt",'w') as file:
            alreadySavedTexts = []
            for ii in strings:
                if ii not in alreadySavedTexts:
                    file.write(ii+"\n")
                    alreadySavedTexts.append(ii)
    #====================================================================
    def cleanAfterWork(self):
        print(self.pathToFolder)
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
            self.writeStringsToFile(analyzer.text,self.filename)
            jj = 0
            for jj in range(int(timeInterval*fps - 1)):
                anyFramesLeft, frame = video.read()
            # jj = 0
            # while anyFramesLeft and jj < timeInterval*fps - 1:
            #     anyFramesLeft, frame = video.read(5) # FIXME być może to nie działą tutaj
            #     jj += 1
    #====================================================================
    def upgradedAnalyzeLive(self, show = False, timeInterval = DEFAULTPARSINGTIME):
        video = cv2.VideoCapture(self.pathToFolder + "/" + self.filename + '.mp4')
        fps = video.get(cv2.CAP_PROP_FPS)
        anyFramesLeft = True
        analyzer = roz.Rozpoznawacz() 
        while anyFramesLeft:
            anyFramesLeft, frame = video.read()
            analyzer.addFrameToAnalyze(frame)
            analyzer.upgradedRecognize(show)
            jj = 0
            for jj in range(int(timeInterval*fps - 1)):
                anyFramesLeft, frame = video.read()
        self.writeStringsToFile(analyzer.text, self.filename)
        self.writeStringsToFile(analyzer.slidingText, self.filename)