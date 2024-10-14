import datetime as dt
import time
import os
import csv

# 1. A megadott 15 számot tárolja el a program forrásában egy megfelelő adatszerkezetben
tomegek = [16, 8, 9, 4, 3, 2, 4, 7, 7, 12, 3, 5, 4, 3, 2]

# 2. A tárgyak tömege alapján határozza meg és írassa ki az össztömeget a minta szerint
ossztomeg = sum(tomegek)
print("2. feladat")
print(f"Az ossztomeg: {ossztomeg} kg")

# 3. Határozza meg, hogy hány dobozra van szükség, és ezekben mekkora tömegek lesznek
dobozok = []
aktualis_doboz = 0

for tomeg in tomegek:
    if aktualis_doboz + tomeg <= 20:
        aktualis_doboz += tomeg
    else:
        dobozok.append(aktualis_doboz)
        aktualis_doboz = tomeg

# Add the last box
if aktualis_doboz > 0:
    dobozok.append(aktualis_doboz)

print("3. feladat")
print(f"Szukseges dobozok szama: {len(dobozok)}")
print("A dobozok tomegei:")
for i, doboz in enumerate(dobozok, 1):
    print(f"{i}. doboz: {doboz} kg")