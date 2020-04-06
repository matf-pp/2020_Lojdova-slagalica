class Polje:

    '''
    
    (x,y)     - koordinate gornjeg levog temena polja
    vrednost  - broj koji se nalazi u tom polju trenutno
    
    '''
    def __init__(self , x,y, vrednost):
        self.x = x
        self.y = y
        self.vrednost = vrednost

    def promeni_vrednost( self , nova_vrednost):
        self.vrednost = nova_vrednost
    
    def trenutna_vrednost(self):
        return (self.vrednost, self.x, self.y)



#----------------------------------------------------


class Slagalica:

    '''

    lista_stanja - lista niski koje predstavljaju stanja kroz koja slagalica prolazi
    (x,y)        - koordinate gornjeg levog temena slagalice
    boja         - boja koju trenutno imaju svi brojevi(string)
    velicina     - velicina slagalice u smislu broj piksela(uz pp da su nam sve slagalice 4x4)

    '''

    def __init__(self , lista_stanja , x,y , boja , velicina) :
        self.lista_stanja = lista_stanja
        self.x = x
        self.y = y
        self.boja = boja
        self.velicina = velicina

        #self.niz_boja = ['plava' , 'zelena' , ...] TODO
        self.indeks_trenutnog = 0 #Indeks trenutnog stanja
        self.broj_stanja = len(lista_stanja) 

        self.polja_slagalice = self.inicijalizuj_polja()


    #Vraca listu brojeva koja predstavlja stanje u kom se slagalica trenutno nalazi
    def trenutno_stanje(self):
        tmp_stanje_string = self.lista_stanja[self.indeks_trenutnog]
        pom = tmp_stanje_string.split(":")

        tmp_stanje_lista = []
        for i in range(16):
            tmp_stanje_lista.append( int(pom[i],10) )

        return tmp_stanje_lista


    def sledece_stanje(self):
        sl_stanje_string = self.lista_stanja[self.indeks_trenutnog+1]
        pom = sl_stanje_string.split(":")

        sl_stanje_lista = []
        for i in range(16):
            sl_stanje_lista.append( int(pom[i],10) )

        return sl_stanje_lista


    #Indikator koji proverava da li je trenutno stanje i poslednje   
    def ind_poslednje_stanje(self):
        if(self.indeks_trenutnog == self.broj_stanja-1):
            return True


    #Plan je da imamo vise boja(menja se kad se promeni stanje)
    #Vraca string 
    def trenutna_boja(self):
        return self.boja

    '''
    Plan:
        Boja da bude napisana kao string, da bih mogli od toga da pravimo imena slike
        i na taj nacin da ih dodeljujemo poljima

        npr naziv slike: 1_plava.png ==> Plavo polje sa jedinicom
    '''
    def promeni_boju(self):
        #TODO tek kad vidimo koje sve boje imamo
        pass


    def dimenzija_polja(self):
        return self.velicina / 4



    #Vraca niz parova (x,y)
    #Na osnovu koordinata (x,y) koji su dati slagalici i dimenzije polja, odredjujem koordinate svakog pojedinacnog polja
    def koordinate_svih_polja(self):
        niz_koord = []

        a = self.dimenzija_polja()

        red = 1
        kolona = 0
        for i in range(16):
            
            x_polja = self.x + kolona*a 
            y_polja = self.y + red*a

            niz_koord.append((x_polja,y_polja))

            if (i+1)%4 == 0:
                red += 1
                kolona = -1

            kolona +=1

        return niz_koord


    '''
    Plan:
        Imam niz instanci klase Polje duzine 16 za slagalicu 4x4.
        Polja u nizu ce biti tako ucitana da odgovaraju sledecem rasporedu:

        [0]  [1]  [2]  [3]
        [4]  [5]  [6]  [7]
        [8]  [9]  [10] [11] 
        [12] [13] [14] [15]

       

        NAPOMENA: Ako se polje nalazi na polju [5] ne znaci da ima broj 5!
                  Polje 5    znaci 5. polje u prikazanom rasporedu.
                  Vrednost 5 znaci da je broj 5 predstavljen na tom polju.

        Vrednost 0 predstavlja polje koje je prazno i koje se ustvari krece kroz slagalicu. 
                  
    '''
    def inicijalizuj_polja(self):
        
        tmp_stanje = self.trenutno_stanje()
        niz_koordinata = self.koordinate_svih_polja()
        
        niz_polja = []
        for i in range(0, 16):
            tmp_x = niz_koordinata[i][0]
            tmp_y = niz_koordinata[i][1]
            tmp_vr = tmp_stanje[i]

            niz_polja.append(Polje(tmp_x,tmp_y,tmp_vr))

        
        return niz_polja


    '''
    
    Plan:
        Ova funkcija da vrati niz parova (Polje , ime_slike)
        Iz polja izvlacimo (x,y) za postavljanje slike. 
        ime_slike = Polje.vr(prebaceno u string) + "_" + self.trenutna_boja

    '''
    #Ovo zahteva funkciju koja ce u pygame da ucita ove podatke, na osnovu njih ucita sliku i prikaze slagalicu
    def trenutni_izgled_slagalice(self):
        niz = []
        tmp_boja = self.trenutna_boja()

        for i in range(16):
            tmp_naziv_slike =  str(self.polja_slagalice[i].vrednost) + "_" + tmp_boja + ".png"

            niz.append( (self.polja_slagalice[i] , tmp_naziv_slike) )

        return niz



    def razlike_stanja(self , trenutno , sledece):
        for i in range(16):
            if trenutno[i] != sledece[i]:
                #Prvo izmenjeno polje
                index1   = i
                nova_vr1 = sledece[i]
                
                #Drugo izmenjeno polje(trazim u ostatku liste)
                for j in range(i+1,16):
                    if trenutno[j] != sledece[j]:
                        index2   = j
                        nova_vr2 = sledece[j]
                        break
                break

        return (index2,nova_vr1,index1,nova_vr2)


    '''

    Plan:
        Funkcija menja vrednost za dva polja cija se polja razlikuju u listama:
            trenutno_stanje i sledece_stanje

    '''
    def promena_stanja(self):

        #TODO Obradi ovu gresku!!!
        if(self.ind_poslednje_stanje()):
            return None 
        else:
            (index1 , nova_vr1 , index2 , nova_vr2) = self.razlike_stanja(self.trenutno_stanje() , self.sledece_stanje())

            self.indeks_trenutnog += 1
            self.polja_slagalice[index1].promeni_vrednost(nova_vr1)
            self.polja_slagalice[index2].promeni_vrednost(nova_vr2)
            self.polja_slagalice = self.inicijalizuj_polja()



#--------------------Testiranje------------------------
if __name__ == "__main__":
    niz_stanja = [ '1:2:3:4:5:6:7:8:9:10:11:12:13:14:15:0' , '1:2:3:4:5:6:7:8:9:10:11:12:13:14:0:15' , '1:2:3:4:5:6:7:8:9:10:11:12:13:0:14:15' ]

    slg = Slagalica(niz_stanja,0,0,"plava",400)

    print(slg.indeks_trenutnog)
    print(slg.broj_stanja)

    print(slg.trenutno_stanje())
    print(slg.indeks_trenutnog)

    slg.promena_stanja()
    print(slg.trenutno_stanje())
    print(slg.indeks_trenutnog)

    slg.promena_stanja()
    print(slg.trenutno_stanje())
    print(slg.indeks_trenutnog)

    if(slg.promena_stanja() != None):
        print(slg.trenutno_stanje())
    else:
        print("Kraj")