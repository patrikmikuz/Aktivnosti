import datetime
import matplotlib.pyplot as plt
import json
import os

class Aktivnost:
    def __init__(self, datum, sport, razdalja, trajanje, vrsta, komentar):
        self.datum = datum
        self.sport = sport
        self.razdalja = razdalja
        self.trajanje = trajanje
        ura = int(self.trajanje.split(':')[0])
        minuta = int(self.trajanje.split(':')[1])
        sekunda = int(self.trajanje.split(':')[2])
        self.cas_v_sekundah = ura * 3600 + minuta * 60 + sekunda
        self.vrsta = vrsta
        self.komentar = komentar

        

    def str_plavanje(self):
        return ("Zabeležena aktivnost je {}. Za razdaljo {} metrov, ste porabili {}.").format(self.sport, str(self.razdalja), self.trajanje)

    def str_kolesarjenje(self):
        return ("Zabeležena aktivnost je {}. Za razdaljo {} kilometrov, ste porabili {}.").format(self.sport, str(self.razdalja), self.trajanje)

    def str_tek(self):
        return ("Zabeležena aktivnost je {}. Za razdaljo {} kilometrov, ste porabili {}.").format(self.sport, str(self.razdalja), self.trajanje)
    

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
            self.trajanje, str(self.tempo()) + " min / 100 m", self.vrsta, self.komentar.replace(" ", "_")]
        if self.sport == "Kolesarjenje":
            return [self.datum, self.sport, str(self.razdalja) + " km", 
            self.trajanje, str(self.tempo()) + " km / h", self.vrsta, self.komentar.replace(" ", "_")]
        if self.sport == "Tek":
            return [self.datum, self.sport, str(self.razdalja) + " km", 
            self.trajanje, str(self.tempo()) + " min / km", self.vrsta, self.komentar.replace(" ", "_")]
    
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

    if os.path.exists('slike/pita.png'):
        os.remove('slike/pita.png')
    plt.figure()
    plt.pie(sizes, colors = colors, labels = labels, autopct='%1.1f%%')
    plt.title('Delež vseh vpisanih aktivnosti')
    plt.savefig('static/pita.png')
    plt.clf()

def najdaljse(datoteka):
    with open(datoteka) as dat:
        zapis = json.load(dat)
    najdaljse_plavanje = 0
    indeks_plavanje = 0
    najdaljse_kolo = 0
    indeks_kolo = 0
    najdaljsi_tek = 0
    indeks_tek = 0
    indeks = 1
    for aktivnost in zapis[1:]:
        if aktivnost[2] == "Plavanje" and float(aktivnost[3].split(" ")[0]) > najdaljse_plavanje:
            indeks_plavanje = indeks
            najdaljse_plavanje = float(aktivnost[3].split(" ")[0])
        elif aktivnost[2] == "Kolesarjenje" and float(aktivnost[3].split(" ")[0]) > najdaljse_kolo:
            indeks_kolo = indeks
            najdaljse_kolo = float(aktivnost[3].split(" ")[0])
        elif aktivnost[2] == "Tek" and float(aktivnost[3].split(" ")[0]) > najdaljsi_tek:
            indeks_tek = indeks
            najdaljsi_tek = float(aktivnost[3].split(" ")[0])
        indeks += 1
    return [zapis[indeks_plavanje], zapis[indeks_kolo], zapis[indeks_tek]]

def prestej_po_mesecih(datoteka):
    slovar = {}

    slovar_plavanje = {}
    slovar_kolesarjenje = {}
    slovar_tek = {}

    slovar_plavanje_razdalje = {}
    slovar_kolesarjenje_razdalje = {}
    slovar_tek_razdalje = {}

    tabela = nalozi_iz_datoteke(datoteka)
    for element in tabela[1:]:
        datum = element[1].split('-')
        razdalja = float(element[3].split(' ')[0])
        vrednost = (int(datum[0]), int(datum[1]))
        if vrednost not in list(slovar.keys()):
            slovar[vrednost] = 1
            if element[2] == 'Plavanje':
                slovar_plavanje[vrednost] = 1
                slovar_kolesarjenje[vrednost] = 0
                slovar_tek[vrednost] = 0
                slovar_plavanje_razdalje[vrednost] = razdalja
                slovar_kolesarjenje_razdalje[vrednost] = 0
                slovar_tek_razdalje[vrednost] = 0
            elif element[2] == 'Kolesarjenje':
                slovar_plavanje[vrednost] = 0
                slovar_kolesarjenje[vrednost] = 1
                slovar_tek[vrednost] = 0
                slovar_plavanje_razdalje[vrednost] = 0
                slovar_kolesarjenje_razdalje[vrednost] = razdalja
                slovar_tek_razdalje[vrednost] = 0
            else:
                slovar_plavanje[vrednost] = 0
                slovar_kolesarjenje[vrednost] = 0
                slovar_tek[vrednost] = 1
                slovar_plavanje_razdalje[vrednost] = 0
                slovar_kolesarjenje_razdalje[vrednost] = 0
                slovar_tek_razdalje[vrednost] = razdalja
        else:
            slovar[vrednost] += 1
            if element[2] == 'Plavanje':
                slovar_plavanje[vrednost] += 1
                slovar_plavanje_razdalje[vrednost] += razdalja
            elif element[2] == 'Kolesarjenje':
                slovar_kolesarjenje[vrednost] += 1
                slovar_kolesarjenje_razdalje[vrednost] += razdalja
            else:
                slovar_tek[vrednost] += 1 
                slovar_tek_razdalje[vrednost] += razdalja
        
    meseci = ['Januar', 'Februar', 'Marec', 'April', 'Maj', 'Junij', 'Julij', 'Avgust', 'September', 'Oktober','November', 'December']
    kljuci = list(slovar.keys())
    plavanja = list(slovar_plavanje.values())
    plavanja_razdalje = list(slovar_plavanje_razdalje.values())
    kolesarjenja = list(slovar_kolesarjenje.values())
    kolesarjenja_razdalje = list(slovar_kolesarjenje_razdalje.values())
    teki = list(slovar_tek.values())
    teki_razdalje = list(slovar_tek_razdalje.values())
    novi_kljuci = []
    for kljuc in kljuci:
        novi_kljuci.append(str(meseci[int(kljuc[1]) - 1]) + " " + str(kljuc[0]))
    vrednosti = list(slovar.values())
    seznam = []
    for i in range(len(slovar)):
        seznam.append([novi_kljuci[i], vrednosti[i], plavanja[i], str(plavanja_razdalje[i]) + ' m',
        kolesarjenja[i], str(kolesarjenja_razdalje[i]) + " km", teki[i], str(teki_razdalje[i]) + " km"])
    return seznam

