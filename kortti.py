import random, pygame 
from ase import *

maat = ["pata","hertta","risti","ruutu"]
arvot = [range(2,14)]

class Kortti():
    maa = "pata"
    arvo = 2

    def luo_kortti(self, maa, arvo):
        self.maa = maa
        self.arvo = arvo
        return
        
    def nayta(self):
        isomaa = str(self.maa).capitalize()
        korttiInfo = isomaa + " " + str(self.arvo)
        return korttiInfo
        
    def vaikutus(self):
        
        if self.maa == "hertta":
            return self.arvo
        
        elif self.maa == "pata":
            return -self.arvo
        
        elif self.maa == "risti":
            return -self.arvo
        
        else:
            uusiAse = Ase()
            return(uusiAse.poimi(self.arvo))
        
