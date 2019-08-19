# Aktivnosti

Spletna aplikacija Sledilec aktivnosti je namenjena vsem amaterskim in "wanna be" profesionalim športnikom, ki se ukvarjajo s plavanjem, 
kolesarjenjem in/ali tekom. Zato je lahko odličen pripomoček za spremljanje in beleženje treningov tudi za triatlonce, in seveda 
ugotavljanje napredovanja v posamezni disciplini posebej. 
    
Po vsakem treningu je potrebno le vnesti čas treninga in opravljeno razdaljo ter aktivnost. Vsi treningni so hitro dostopni, prav tako 
pa je mogoče tudi iskanje po mesecih, tekmah in disciplini. Na koncu vsakega meseca je tudi izračunana skupna opralvjena razdalja v 
posamezni disciplini in število opravljenih aktivnosti.

V python datoteki Model so zapisane vse funkcije in razred aktivnost, ki se uporablja pri beleženju. V python datoteki Vmesnik, je 
uvožena knjižnjica Bottle in Model, ter napisane vse funkcije za spletni vmesnik. V mapi views so shranjene html datoteke vseh spletnih 
strani, ki se uporabljajo v aplikaciji. V mapi static so shranjene slike, ki se prikazujejo na spletnih straneh. V mapi datoteke sta shranjeni 
json datoteki, v katerih je zapisana vsa zgodovina aktivnosti, ki se potem tudi izpisuje na spletni strani. 

Za pravilno delovanje aplikacije, je potrebno pognati Vmesnik.py v okolju z nameščeno matplotlib knjižnjico.