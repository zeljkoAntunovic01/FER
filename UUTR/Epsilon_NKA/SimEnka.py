import pprint
import sys


class Automat():
    def __init__(self,ulazniNizovi,stanja,abeceda,pocetnoStanje,prijelazi):
        self.ulazniNizovi = ulazniNizovi
        self.stanja = stanja
        self.abeceda = abeceda
        self.pocetnoStanje = pocetnoStanje
        self.prijelazi = prijelazi
    def getPrijelazi(self):
        return self.prijelazi
    def epsilonOkolina(self,stanje): #racunanje epsilon okoline stanja
        i = 0
    
        okolina = list()
        okolina.append(stanje) #samo stanje je u svojoj okolini
        while (i<len(okolina)): #svaki prolaz inkrementiramo "i" => petlja zavrsava kada  i == len(okolina) tj. nismo dodali snova stanja dovoljno puno puta
            if (okolina[i],"$") in self.prijelazi: #ako postoji epsilon prijelaz
                sljStanja = self.prijelazi[(okolina[i],"$")] #dohvati sljedeca stanja
                for stanje in sljStanja: #dodaj stanja u okolinu, ali samo ako vec nisu u listi
                    if not(stanje in okolina):
                        okolina.append(stanje)
            i+=1           
                    
        return okolina
    
    def obradiUlazneNizove(self):
        nizovi = self.ulazniNizovi.split("|") #splitaj nizove po "|"
        
        pomocniSkup = set()
        pomocniSkup.add(self.pocetnoStanje)
        
        eOkolina = self.epsilonOkolina(self.pocetnoStanje)
        
        pomocniSkup.update(eOkolina)
            
        self.pocetnoStanje = set()
        for stanje in pomocniSkup:
            self.pocetnoStanje.add(stanje)
        for niz in nizovi:
            
            novaStanja = set()
            znakovi = niz.split(",")
            
            novaStanja = novaStanja.union(self.pocetnoStanje)
            sortiranaPocetna = sorted(self.pocetnoStanje)
            for i in range (len(sortiranaPocetna)):
                if i!=len(sortiranaPocetna)-1:
                    print(sortiranaPocetna[i],end=",")
                else:
                    print(sortiranaPocetna[i],end="")
        
            for znak in znakovi:
                
                print("|",end ="")
                #EPSILON OKOLINA OVDJE
                pomocniSkup = novaStanja.copy()
                for stanje in novaStanja:
                    eOkolina = self.epsilonOkolina(stanje)
                    pomocniSkup.update(eOkolina)
                    
            
                for stanje in pomocniSkup:
                    
                    novaStanja.add(stanje)
                
                pomocniSkup.clear()
                
                
                for stanje in novaStanja:
                    if (stanje,znak) in self.prijelazi.keys():
                        nStanja = self.prijelazi[(stanje,znak)]
                        for nStanje in nStanja:
                            if (nStanje!="#"):
                                pomocniSkup.add(nStanje)
                        
                if len(pomocniSkup)==0:
                    pomocniSkup.add("#")
                    
            
                novaStanja = pomocniSkup.copy() 
                
                for stanje in novaStanja:
                    eOkolina = self.epsilonOkolina(stanje)
                    
                    
                    pomocniSkup.update(eOkolina)
                    
                
                for stanje in pomocniSkup:
                    
                    novaStanja.add(stanje)
                
                sortiranaStanja = sorted(novaStanja)
                pomocnaLista = sortiranaStanja.copy()
                for stanje in sortiranaStanja:
                    if stanje=="#" and len(sortiranaStanja)>1:
                        pomocnaLista.remove(stanje)
                sortiranaStanja = pomocnaLista.copy()
                for i in range(len(sortiranaStanja)):
                    if i!=len(sortiranaStanja)-1:
                        print(sortiranaStanja[i],end=",")
                    else:
                        print(sortiranaStanja[i],end="")

        
                pomocniSkup.clear()
                
                
            print("")
        return
                    
                    
                    
                
list1=[] #linije od 1-5
list2=[] #linije 6-n (varijabilan broj upisa)
for i in range(5): #upis prvih 5 linija
    list1.append(str(input()))
list2 = sys.stdin.read().splitlines() #upis ostalih linija


for i in range (len(list2)): #svaku liniju 6-n splitaj po "->", zato sto su sve te linije prijelazi
    list2[i] = list2[i].split("->") 

prijelazi = {} #dictionary, key = uredeni par (stanje,ulazni znak), value = sljedece stanje
for prijelaz in list2:
    
    stanjeUlaz = prijelaz[0].split(",") #splitanje lijeve strane strelice, da dobijemo listu [stanje,ulazni znak]
    sljedecaStanja = prijelaz[1].split(",") #splitanje desne strane strelice, da dobijemo listu stanja
    stanjeUlazKey = (stanjeUlaz[0],stanjeUlaz[1]) #uredeni par [stanje, ulazni znak]
    prijelazi[stanjeUlazKey] = sljedecaStanja


automat = Automat(list1[0],list1[1],list1[2],list1[4],prijelazi)
automat.obradiUlazneNizove()

