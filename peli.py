import random, os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame 

from kortti import *
from muuttujat import *
from ase import *

# Scoundrel-pelin maat:
# Ruutu (2-10) - Ase (vähentää vihollisten tekemää vahinkoa)
# Hertta (2-10) - Taikajuoma/ruoka (parantaa sinua)    
# Pata (2-14) - Vihollinen (tekee sinuun vahinkoa)
# Risti (2-14) - Vihollinen (ks. pata)

korttienMaara = {
    "ruutu": 9,
    "hertta": 9,
    "pata": 13,
    "risti": 13
}

nostoPakka = []
poistoPakka = []
poyta = []
nykyinenAse = []

# Yhden kortin siirtäminen nostopakasta pöydälle
def paljasta_kortti():
    
    ylinKortti = nostoPakka[-1]
    poydattyKortti = ylinKortti
    nostoPakka.pop()
    poyta.append(poydattyKortti)
    return

# Ilmoittaa: nykyinen ase, mahdollisuus parantaa,
# HP, nostopakan koko ja pöydän kortit
def nayta_poyta():
    
    if nykyinenAse.__len__() > 0:
        print("Aseen voima: " + str(nykyinenAse[0].voima) 
              + "; Aseen kestävyys: " + str(nykyinenAse[0].kestavyys))
    
    if not Muuttujat.voiParantua:
        print("<[Et voi enää parantaa itseäsi tässä huoneessa!]>")
    
    print("HP = " + str(Muuttujat.HP))
    print("Nostopakassa on " + str(nostoPakka.__len__()) + " korttia.")
    
    poytaInfo = "Pöydässä olevat kortit: "
    for kortti in poyta:
        poytaInfo += " [" + kortti.nayta() +"] "
        
    print(poytaInfo)
    return

# Ilmoittaa näppäinvaihtoehdot      
def nayta_ohjeet():
    
    for k in range(poyta.__len__()):
        print(str(k + 1) + " - Ota kortti: " + poyta[k].maa + " " + str(poyta[k].arvo))
    
    if Muuttujat.voiJuosta and nostoPakka.__len__() > 0:
        if poyta.__len__() < 2:
            print("5 - Etene seuraavaan huoneeseen")
        elif poyta.__len__() == 4: 
            print("5 - Karkaa huoneesta")
    return

def hylkaa_ase():
    
    poistoPakka.extend(nykyinenAse)
    nykyinenAse.clear()
    print("Hylkäsit aseen.")
    return

def pelaa_kortti(i):
    
    pelattavaKortti = poyta[i-1]
    vaikutus = pelattavaKortti.vaikutus()
    poyta.pop(i-1)
    
    # Jos pelattu kortti on ruutu (=ase)
    if type(vaikutus) is not int:
        
        if nykyinenAse.__len__() > 0: hylkaa_ase()
            
        print("Poimit uuden aseen.")
        uusiAse = vaikutus
        nykyinenAse.append(uusiAse)
    
    else:
        # Vihollinen haastetaan aseen kanssa
        if nykyinenAse.__len__() > 0 and vaikutus < 0:
            vihollisenVoima = -1 * vaikutus
            
            # Ase kuluu käytössä: Aseella päihitettävän vihollisen
            # on oltava pienempi kuin edellinen sillä aseella
            # päihitetty vihollinen
            if nykyinenAse[0].kestavyys > vihollisenVoima:
                hpMuutos = int(nykyinenAse[0].kayta(vihollisenVoima))
                nykyinenAse.append(pelattavaKortti)
            
                if hpMuutos > 0:
                    hpMuutos = 0
                    
            else:
                
                hylkaa_ase()
                hpMuutos = int(vaikutus)
                poistoPakka.append(pelattavaKortti)
        
        
        # Pelattu kortti on parannuskortti tai 
        # ilman asetta kohdattu vihollinen
        else:
            
            # Vain yksi parannus huoneessa
            if Muuttujat.voiParantua or vaikutus < 0: hpMuutos = vaikutus 
            else: hpMuutos = 0  
                 
            poistoPakka.append(pelattavaKortti)
            if hpMuutos > 0: Muuttujat.voiParantua = False
            
        Muuttujat.HP = Muuttujat.HP + hpMuutos
        Muuttujat.voiJuosta = False
    
    if poyta.__len__() < 2:
        Muuttujat.voiJuosta = True
    
    if poyta.__len__() == 0:
        Muuttujat.voiParantua = True
    
    if Muuttujat.HP > 20:
        Muuttujat.HP = 20
    
    korttejaJaljella = nostoPakka.__len__() + poyta.__len__()
    if Muuttujat.HP < 1 or korttejaJaljella == 0:
        Muuttujat.peliOhi = True
  
    return

def karkaa_huoneesta():

    random.shuffle(poyta)
    nostoPakka[:0] = poyta
    poyta.clear()
    Muuttujat.voiJuosta = False
    return

def etene():  
          
    while poyta.__len__() < 4 and nostoPakka.__len__() > 0:
        paljasta_kortti()
    
    Muuttujat.voiParantua = True    
    return

def peli_ohi():
    print("Peli ohi!")
    pisteet = Muuttujat.HP
    
    # Pisteiden lasku pelin hävittyä
    if Muuttujat.HP < 1:
        nostoPakka.extend(poyta)
        poyta.clear()
        
        for k in nostoPakka:
            if k.maa == "pata" or k.maa == "risti":
                pisteet -= k.arvo
    
    # Pisteiden lasku pelin voitettua    
    if Muuttujat.HP > 0:

        viimeinenKortti = poistoPakka[-1]
        
        if viimeinenKortti.maa == "hertta" and Muuttujat.HP == 20: 
            pisteet += viimeinenKortti.arvo    
        
    print("Tuloksesi: " + str(pisteet) + " pistettä")
        
    while True:
        vastaus = input("Haluatko aloittaa uuden pelin? (y/n) ")
    
        if vastaus == "y": return(True)
        elif vastaus == "n": return(False)
        
def nollaa_peli():
    nostoPakka.clear()
    poyta.clear()
    poistoPakka.clear()
    nykyinenAse.clear()
    Muuttujat.HP = 20
    Muuttujat.peliOhi = False
    Muuttujat.voiJuosta = True
    Muuttujat.voiParantua = True

# Pelin alussa luodaan ja sekoitetaan korttipakka.
# Pakasta poistetaan punaiset kuvakortit ja ässät.
def aloita_peli():
    nollaa_peli()

    for m in maat:
        for a in range(korttienMaara[m]):
            uusiKortti = Kortti()
            uusiKortti.luo_kortti(m,a + 2)
            nostoPakka.append(uusiKortti)
    
    random.shuffle(nostoPakka)
    
    # Pelin pääasiallinen looppi. Pelaajalle kerrotaan tiedot ja
    # odotetaan komentoa (numero 1-5)
    while not Muuttujat.peliOhi:
        while nostoPakka.__len__() > 0:
            while poyta.__len__() < 4 and nostoPakka.__len__() > 0:
                    paljasta_kortti()
            
            while poyta.__len__() > 0:    
                
                nayta_poyta()
                nayta_ohjeet()
                
                try:
                    valinta = int(input("> "))
                    print()
                    
                    if valinta <= poyta.__len__():
                        pelaa_kortti(valinta)
                                                
                        if Muuttujat.peliOhi:
                            aloitaUusi = peli_ohi()
                            if aloitaUusi: aloita_peli()
                            else: quit()
                    
                    elif valinta == 5:
                        if poyta.__len__() == 4 and Muuttujat.voiJuosta:
                            karkaa_huoneesta()
                        elif poyta.__len__() == 1:
                            etene()
                        else:
                            print("Et voi poistua huoneesta nyt.")
                        
                except ValueError:
                    print("Kirjoita numero.")
                    
    
aloita_peli()

quit()