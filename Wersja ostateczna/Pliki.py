import youtube_dl, cv2, pytesseract as pt, Rozpoznawacz as roz, os, shutil

DEFAULTPARSINGTIME = 6

class Plik:
    def __init__(self, url, filename):
        self.url = url
        self.filename = filename
        self.pathToFolder = "./"+self.filename + "Dir"
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
                anyFramesLeft = video.grab()

        if mode >= 1:
            self.writeStringsToFile(analyzer.textMain)
        if mode >= 2:
            self.writeStringsToFile(analyzer.textUnderMain)