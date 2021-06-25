from Pliki import *
import Rozpoznawacz as roz
# Przykładowy plik: https://www.youtube.com/watch?v=fxvg_xOy4Y4
def main(link, name, czyPrzygotowane, czyPokazywać = False):
    # file = Plik('https://www.youtube.com/watch?v=fxvg_xOy4Y4', 'elolo')
    # file.parser()
    file2 = Plik(link,name)
    if not czyPrzygotowane:
        file2.download()
        file2.parser(10)
    file2.analyzeVideo(czyPokazywać)
    # rozpoznawacz = roz.Rozpoznawacz('frame0.jpg')
    # tekst = rozpoznawacz.recognize(850,980,350,1800)
    # print(rozpoznawacz.text)
    # file2 = Plik('https://github.com/ytdl-org/youtube-dl#format-selection-examples', 'hihi')
    # file2.download()https://www.tvp.info/54526597/premier-podsumowuje-szczyt-ue?copyId=54146645
    


if __name__ == "__main__":
    main('https://www.tvp.info/54522642/czym-grozi-nam-udar-cieplny','Udar',True)