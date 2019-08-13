import Bottle
import Model
import json
import datetime
import matplotlib.pyplot as plt

@Bottle.route('slike/<picture>')
def server_static(picture):
    return Bottle.static_file(picture, root='slike/')



@Bottle.get("/")
def domaca_stran():
    try: stevec
    except NameError:
         None
    else: 
        stevec = 0
    print(stevec)
    #Model.pita(sizes = Model.nalozi_iz_datoteke('datoteke/statistika.json'), stevec)
    #stevec += 1
    #Model.histogram(seznam = Model.nalozi_iz_datoteke('datoteke/aktivnosti.json'), stevec)
    #stevec += 1
    return Bottle.template("index.html")

@Bottle.get("/ustvari/")
def ustvari():
    return Bottle.template("ustvari.html")

@Bottle.get("/ustvarjeno/")
def ustvarjeno():
    tabela_aktivnosti = [["Zaporedna številka", "Datum", "Šport", "Razdalja", "Čas", "Tempo", "Vrsta"]]
    statistika = [0, 0, 0]
    Model.zapis_v_datoteko('datoteke/aktivnosti.json', tabela_aktivnosti)
    Model.zapis_v_datoteko('datoteke/statistika.json', statistika)
    return Bottle.template("ustvarjeno.html")

@Bottle.get("/dodaj/")
def zahtevaj_vnos():
    return Bottle.template("dodaj.html")


@Bottle.post("/dodano/")
def dodano():
    datum = Bottle.request.forms.getunicode("datum_kdaj")
    sport = Bottle.request.forms.getunicode("sport")
    razdalja = float(Bottle.request.forms.getunicode("razdalja"))
    ura = int(Bottle.request.forms.getunicode("ura"))
    minuta = int(Bottle.request.forms.getunicode("minuta"))
    sekunda = int(Bottle.request.forms.getunicode("sekunda"))
    vrsta = Bottle.request.forms.getunicode("vrsta")
    komentar = Bottle.request.forms.getunicode("komentar")
    nova_aktivnost = Model.Aktivnost(datum, sport, razdalja, ura, minuta, sekunda, vrsta, komentar)
    tabela = Model.nalozi_iz_datoteke('datoteke/aktivnosti.json')
    statistika = Model.nalozi_iz_datoteke('datoteke/statistika.json')
    statistika.append(nova_aktivnost.sport)
    
    if sport == "Plavanje":
        tekst = Model.Aktivnost.str_plavanje(nova_aktivnost)
        statistika = Model.nalozi_iz_datoteke('datoteke/statistika.json')
        statistika[0] += 1
        Model.zapis_v_datoteko('datoteke/statistika.json', statistika)
    
    elif sport == "Kolesarjenje":
        tekst = Model.Aktivnost.str_kolesarjenje(nova_aktivnost)
        statistika = Model.nalozi_iz_datoteke('datoteke/statistika.json')
        statistika[1] += 1
        Model.zapis_v_datoteko('datoteke/statistika.json', statistika)
    
    else:
        tekst = Model.Aktivnost.str_tek(nova_aktivnost)
        statistika = Model.nalozi_iz_datoteke('datoteke/statistika.json')
        statistika[2] += 1
        Model.zapis_v_datoteko('datoteke/statistika.json', statistika)
    
    if len(tabela) == 1:
        nova_tabela = [tabela[0]]
        nova_tabela += [[1] + nova_aktivnost.pripravi_za_zapis()]

    else:
        nova_tabela = [tabela[0]]
        neurejene_vrednosti = [element[1:] for element in tabela[1:]]
        neurejene_vrednosti.append(nova_aktivnost.pripravi_za_zapis())
        urejene_vrednosti = sorted(neurejene_vrednosti, key = lambda x : x[0])
        i = 1
        zapis = []
        for element in urejene_vrednosti:
            zapis += [[i] + element]
            i += 1
        nova_tabela += zapis

    Model.zapis_v_datoteko('datoteke/aktivnosti.json', nova_tabela)

    return Bottle.template("dodano.html", besedilo = tekst)


@Bottle.get("/zgodovina/")
def zgodovina():
    return Bottle.template("zgodovina.html", tabela = Model.nalozi_iz_datoteke('datoteke/aktivnosti.json'))

@Bottle.get("/zgodovina_plavanje/")
def zgodovina_plavanje():
    return Bottle.template("zgodovina_plavanje.html", tabela = Model.nalozi_iz_datoteke('datoteke/aktivnosti.json'))

@Bottle.get("/zgodovina_kolesarjenje/")
def zgodovina_kolesarjenje():
    return Bottle.template("zgodovina_kolesarjenje.html", tabela = Model.nalozi_iz_datoteke('datoteke/aktivnosti.json'))

@Bottle.get("/zgodovina_tek/")
def zgodovina_tek():
    return Bottle.template("zgodovina_tek.html", tabela = Model.nalozi_iz_datoteke('datoteke/aktivnosti.json'))

@Bottle.get("/statistika/")
def statistika():
    sizes = Model.nalozi_iz_datoteke('datoteke/statistika.json')
    najdaljsi = Model.najdaljse('datoteke/aktivnosti.json')
    return Bottle.template("statistika.html", tabela = sizes, najdaljsi = najdaljsi)


@Bottle.get('slike/<ime>')
def vrni_slike(ime):
    return Bottle.static_file(ime, root="img")

@Bottle.get("/izbris/")
def izbris():
    return Bottle.template("izbris.html")

@Bottle.post("/izbrisano/")
def izbrisano():
    tabela = Model.nalozi_iz_datoteke('datoteke/aktivnosti.json')
    stevilo = int(Bottle.request.forms.getunicode("zap"))
    seznam = Model.nalozi_iz_datoteke('datoteke/statistika.json')
    if tabela[stevilo][2] == 'Plavanje':
        seznam[0] -= 1
    elif tabela[stevilo][2] == 'Kolesarjenje':
        seznam[1] -= 1
    else:
        seznam[2] -= 1
    Model.zapis_v_datoteko('datoteke/statistika.json', seznam)
    del tabela[stevilo]
    nova_tabela = [tabela[0]]
    for i in range(1, len(tabela)):
        nova_tabela.append([i] + tabela[i][1:])
    Model.zapis_v_datoteko('datoteke/aktivnosti.json', nova_tabela)
    return Bottle.template("izbrisano.html")

Bottle.run(reloader = "True", debug = "True")

