# Najważniejsze pola w tym csv: Czas, kraj, nowe zakażenia, total cases, total deaths,
# ew total tests, positive rate, total vaccinations, new vaccinations
import Pliki, Kraj, matplotlib.pyplot as plt, numpy as np, sys
# print(Pliki.zrobListęKolumn("iso_code","location"))
# arg = ("iso_code","location")
# x = Pliki.wczytajKolumny("Armenia",*arg)
# print(x)
kraj = Kraj.Kraj("Poland")
# print(kraj.location)
# print(kraj.date)
# print(kraj.total_cases)
kraj.wykresujSię(kraj.new_cases)