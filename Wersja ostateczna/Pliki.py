import youtube_dl, cv2, pytesseract as pt, Rozpoznawacz as roz, os, shutil
#====================================================================
DEFAULTPARSINGTIME = 6
#====================================================================
class Plik:
    def __init__(self, url):
        self.url = url
        self.isFileBroken = False
        # Tworzę nazwę pliku na podstawie adresu URL
        try:
            parsed = self.url.split("/")[4].split('-')
            self.filename = parsed[0] + '-' + parsed[1] + '-' + parsed[2] 
        except IndexError: # jeżeli dostaniemy ten błąd to link jest niepoprawny, nazwa katalogu nie jest 
            # istotna, bo i tak w procesie pobierania usuwane są wadliwe pliki i katalogi
            self.isFileBroken = True
            self.filename = 'Wrong URL'
        self.pathToFolder = "./"+self.filename + "Dir"
    #====================================================================
    def download(self):
        if self.isFileBroken ==  True:
            return
        
        try:
            os.mkdir(self.pathToFolder)
        except FileExistsError: # Jeśli dany folder już istnieje to nic nie robimy
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
            except youtube_dl.utils.DownloadError: # Jeżeli nawet plik przejdzie test nazwy ale URL z jakiegoś powodu nie działa
                # to błąd zostanie wykryty w tym momencie i dalej nic już się nie stanie
                print("Pobieranie nie powiodło się.")
                self.isFileBroken = True
                self.cleanAfterWork()
    #====================================================================
    def writeStringsToFile(self, strings):
        """Zapisuje do pliku teksty, usuwa powtórzenia"""
        if len(strings)<2 or self.isFileBroken == True: # Zawsze jest jeden napis mówiący o tym z którego tickera czytamy
            return
        with open(self.filename + " Wycięte Teksty.txt",'a', encoding = 'utf8') as file:
            alreadySavedTexts = []
            for ii in strings:
                if ii not in alreadySavedTexts: # Napisy na tickerach mogą się powtarzać, dlatego usuwam duplikaty
                    # Może się zdarzyć, że tesseract coś źle odczyta i przez to pojawią się duplikaty, jednak nie można przewidzieć 
                    # jakiego rodzaju będzie błąd i przez to trudno wyeliminować tego typu pomyłki
                    file.write(ii+"\n")
                    alreadySavedTexts.append(ii)
    #====================================================================
    def cleanAfterWork(self):
        # Usuwam folder z filmem, plik z tekstem nie zostaje usunięty bo jest zapisywany poza nim
        shutil.rmtree(self.pathToFolder)
    #====================================================================
    def analyzeLive(self, mode = 1, timeInterval = DEFAULTPARSINGTIME):
        if self.isFileBroken:
            return
        video = cv2.VideoCapture(self.pathToFolder + "/" + self.filename + '.mp4')
        # Nie trzeba analizować każdej klatki, wystarczy co kilka sekund
        fps = video.get(cv2.CAP_PROP_FPS)
        analyzer = roz.Rozpoznawacz()
        anyFramesLeft, frame = video.read()
        analyzer.addFrameToAnalyze(frame)
        # Lokalizujmy gdzie dokładnie znajduje się ticker, gdyż zmienia się to w zależności od filmu
        analyzer.findTicker()
        analyzer.setMode(mode)
        # Na podstawie doświadczeń przyjąłem takie czasy jako optymalne dla poszczególnych trybów
        if mode == 1:
            timeInterval = 30
        if mode == 2:
            timeInterval = 7

        while anyFramesLeft:
            anyFramesLeft, frame = video.read()
            analyzer.addFrameToAnalyze(frame)
            analyzer.recognize()

            # grab() ,,zdejmuje'' klatkę bez zapisywania jej, co jest szybsze niż powtarzanie read()
            for jj in range(int(timeInterval*fps - 1)):
                anyFramesLeft = video.grab()

        if mode >= 1:
            self.writeStringsToFile(analyzer.textMain)
        if mode >= 2:
            with open(self.filename + " Wycięte Teksty.txt",'a', encoding = 'utf8') as file:
                file.write("\n") # Rozdzielam napisy z tickera głównego i dodatkowego
            self.writeStringsToFile(analyzer.textUnderMain)