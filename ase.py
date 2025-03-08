class Ase():
    voima = 2
    kestavyys = 15
   
    def poimi(self, arvo):
       self.voima = arvo
       return self
       
    def kayta(self, hyokkays):
        self.kestavyys = hyokkays
        vahinko = self.voima - hyokkays
        return(vahinko)
    
        