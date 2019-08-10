import datetime
import matplotlib.pyplot as plt
import json
from PIL import Image
import os

class Aktivnost:
    def __init__(self, datum, sport, razdalja, ura, minuta, sekunda, vrsta = "trening"):
        self.datum = datum
        self.sport = sport
        self.razdalja = razdalja
        self.ura = ura
        self.minuta = minuta
        self.sekunda = sekunda
        self.cas_v_sekundah = ura * 3600 + minuta * 60 + sekunda
        self.vrsta = vrsta
        datum_priprava = datum.split('-')
        teden = datetime.date(int(datum_priprava[0]), int(datum_priprava[1]), int(datum_priprava[2])).isocalendar()[1]
        leto = datetime.date(int(datum_priprava[0]), int(datum_priprava[1]), int(datum_priprava[2])).isocalendar()[0]
        self.teden = teden
        self.leto = leto


    def pretvori_cas(self):
        return (str(self.ura) + ":" + str(self.minuta) + ":" + str(self.sekunda))

    def str_plavanje(self):
        return ("Zabeležena aktivnost je {}. Za razdaljo {} metrov, ste porabili {}.").format(self.sport, str(self.razdalja), Aktivnost.pretvori_cas(self))

    def str_kolesarjenje(self):
        return ("Zabeležena aktivnost je {}. Za razdaljo {} kilometrov, ste porabili {} ur, {} minut in {} sekund.").format(self.sport, str(self.razdalja), str(self.ura), str(self.minuta), str(self.sekunda))

    def str_tek(self):
        return ("Zabeležena aktivnost je {}. Za razdaljo {} kilometrov, ste porabili {}.").format(self.sport, str(self.razdalja), Aktivnost.pretvori_cas(self))
    

    def __str__(self):
        if self.sport == "Plavanje":
            return Aktivnost.str_plavanje(self)
        elif self.sport == "Kolesarjenje":
            return Aktivnost.str_kolesarjenje(self)
        elif self.sport == "Tek":
            return Aktivnost.str_tek(self)
    
    def tempo(self):
        if self.sport == "Plavanje":
            hitrost = round(self.cas_v_sekundah / self.razdalja * 1.66, 2)
            return round((hitrost % 1) * 0.6 + hitrost // 1, 2)
        elif self.sport == "Kolesarjenje":
            return round(self.razdalja / self.cas_v_sekundah * 3600, 1)
        else:
            hitrost = round(self.cas_v_sekundah / self.razdalja / 60, 2)
            return round((hitrost % 1) * 0.6 + hitrost // 1, 2)
    
    def pripravi_za_zapis(self):
        if self.sport == "Plavanje":
            return [self.datum, self.sport, str(self.razdalja) + " m", 
            self.pretvori_cas(), str(self.tempo()) + " min / 100 m", self.vrsta]
        if self.sport == "Kolesarjenje":
            return [self.datum, self.sport, str(self.razdalja) + " km", 
            self.pretvori_cas(), str(self.tempo()) + " km / h", self.vrsta]
        if self.sport == "Tek":
            return [self.datum, self.sport, str(self.razdalja) + " km", 
            self.pretvori_cas(), str(self.tempo()) + " min / km", self.vrsta]
    
def zapis_v_datoteko(datoteka1, tabela):
    with open(datoteka1, 'w') as dat1:
        zapis = json.dumps(tabela)
        dat1.write(zapis)


def nalozi_iz_datoteke(datoteka):
    with open(datoteka) as dat:
        zapis = json.load(dat)
    return zapis

def pita(sizes):
    labels = ["Plavanje", "Kolesarjenje", "Tek"]
    colors = ["skyblue", "yellowgreen", "lightcoral"]
    plt.pie(sizes, colors = colors, labels = labels, autopct='%1.1f%%')
    
    if os.path.exists('slike/pita.png'):
        os.remove('slike/pita.png')

    plt.savefig('slike/pita.png')
   
def najdaljse(datoteka):
    with open(datoteka) as dat:
        zapis = json.load(dat)
    najdaljse_plavanje = 0
    indeks_plavanje = 0
    najdaljse_kolo = 0
    indeks_kolo = 0
    najdaljsi_tek = 0
    indeks_tek = 0
    for aktivnost in zapis[1:]:
        indeks = 1
        if aktivnost[2] == "Plavanje" and float(aktivnost[3].strip(" ")[0]) > najdaljse_plavanje:
            indeks_plavanje = indeks
            najdaljse_plavanje = float(aktivnost[3].strip(" ")[0])
        elif aktivnost[2] == "Kolesarjenje" and float(aktivnost[3].strip(" ")[0]) > najdaljse_kolo:
            indeks_kolo = indeks
            najdaljse_kolo = float(aktivnost[3].strip(" ")[0])
        elif aktivnost[2] == "Tek" and float(aktivnost[3].strip(" ")[0]) > najdaljsi_tek:
            indeks_tek = indeks
            najdaljsi_tek = float(aktivnost[3].strip(" ")[0])
        indeks += 1
    return [zapis[indeks_plavanje], zapis[indeks_kolo], zapis[indeks_tek]]