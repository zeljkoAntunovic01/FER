import pprint
import sys

class Automat():
    def __init__(self,ulazniNizovi,stanja,abeceda,abecedaStoga,prihvatljivaStanja,pocetnoStanje,pocetniZnakStoga,prijelazi):
        self.ulazniNizovi = ulazniNizovi
        self.stanja = stanja
        self.abeceda = abeceda
        self.abecedaStoga = abecedaStoga
        self.prihvatljivaStanja = prihvatljivaStanja
        self.pocetnoStanje = pocetnoStanje
        self.pocetniZnakStoga = pocetniZnakStoga
        self.prijelazi = prijelazi
    def obradiUlazneNizove(self):
        for niz in self.ulazniNizovi:
            stog = self.pocetniZnakStoga
            trenutnoStanje = self.pocetnoStanje
            print(trenutnoStanje + "#" + stog + "|", end = "")
            prekid = 0
            for znak in niz:
                
                ulaz = (trenutnoStanje, znak, stog[len(stog)-1]) 
                if ulaz in prijelazi.keys():
                    trenutnoStanje = prijelazi[ulaz][0]
                    if len(stog)>1:  
                        stog = stog[0:len(stog)-1]
                    else:
                        stog = ""
                    if prijelazi[ulaz][1]!="$":
                        stog = stog + prijelazi[ulaz][1][::-1]
                    if stog=="":
                        print(trenutnoStanje + "#" + "$" + "|", end = "")
                    
                    print(trenutnoStanje + "#" + stog[::-1] + "|", end = "")
                else:
                    
                    while(1):
                        if stog=="":
                            break
                        ulaz = (trenutnoStanje, "$", stog[len(stog)-1])
                        if  ulaz in prijelazi.keys():
                            trenutnoStanje = prijelazi[ulaz][0]
                            if len(stog)>1:  
                                stog = stog[0:len(stog)-1]
                            else:
                                stog = ""
                            if prijelazi[ulaz][1]!="$":
                                stog = stog + prijelazi[ulaz][1][::-1]
                                print(trenutnoStanje + "#" + stog[::-1] + "|", end = "")
                            if stog=="":
                                print(trenutnoStanje + "#" + "$" + "|", end = "")
                            
                            
                        else:
                            break
                    if stog=="":
                        print("fail|",end = "")
                        prekid = 1
                        break
                    ulaz = (trenutnoStanje, znak, stog[len(stog)-1]) 
                    if ulaz in prijelazi.keys():
                        trenutnoStanje = prijelazi[ulaz][0]
                        if len(stog)>1:  
                            stog = stog[0:len(stog)-1]
                        else:
                            stog = ""
                        if prijelazi[ulaz][1]!="$":
                            stog = stog + prijelazi[ulaz][1][::-1]
                        if stog=="":
                            print(trenutnoStanje + "#" + "$" + "|", end = "")
                        
                        print(trenutnoStanje + "#" + stog[::-1] + "|", end = "")
                    else:
                        print("fail|",end = "")
                        prekid = 1
                        break
            
            
            while(prekid==0 and (trenutnoStanje not in self.prihvatljivaStanja)):
                ulaz = (trenutnoStanje,"$",stog[len(stog)-1])
                if ulaz in prijelazi.keys():
                    trenutnoStanje = prijelazi[ulaz][0]
                    stog = stog[0:len(stog)-1]
                    if prijelazi[ulaz][1]!="$":
                        stog = stog + prijelazi[ulaz][1][::-1]
                        print(trenutnoStanje + "#" + stog[::-1] + "|", end = "")
                    if stog=="":
                        print(trenutnoStanje + "#" + "$" + "|", end = "")
                        break
                    
                else:
                    break 
            if prekid==1:
                print(0)
            else:
                if trenutnoStanje in self.prihvatljivaStanja:
                    print(1)
                else:
                    print(0)
            
list1=[]     
list2=[]
for i in range(7):
    list1.append(str(input()))
list2 = sys.stdin.read().splitlines()
for i in range (len(list2)):
    list2[i] = list2[i].split("->") 

prijelazi = {} #dictionary, key = n-torka (stanje,ulazni znak, vrh stoga), value = sljedece stanje, vrh stoga
for prijelaz in list2:
    
    stanjeUlaz = prijelaz[0].split(",") 
    sljedecaStanja = prijelaz[1].split(",")
    stanjeUlazKey = (stanjeUlaz[0],stanjeUlaz[1],stanjeUlaz[2])
    prijelazi[stanjeUlazKey] = sljedecaStanja

uNizovi = list1[0]
uNizovi = uNizovi.split('|')
for i in range(len(uNizovi)):
    pomocna = uNizovi[i].split(',')
    pomocna = ''.join(pomocna)
    uNizovi[i] = pomocna
    
automat = Automat(uNizovi,list1[1],list1[2],list1[3],list1[4],list1[5],list1[6],prijelazi)
automat.obradiUlazneNizove()