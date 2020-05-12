# Lojdova slagalica

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/ef68343b3be3489ca58dea50fe2eb14a)](https://app.codacy.com/gh/matf-pp/2020_Lojdova-slagalica?utm_source=github.com&utm_medium=referral&utm_content=matf-pp/2020_Lojdova-slagalica&utm_campaign=Badge_Grade_Dashboard)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/ef68343b3be3489ca58dea50fe2eb14a)](https://app.codacy.com/gh/matf-pp/2020_Lojdova-slagalica?utm_source=github.com&utm_medium=referral&utm_content=matf-pp/2020_Lojdova-slagalica&utm_campaign=Badge_Grade_Dashboard)

:clipboard: ## Opis:
Aplikacija _Lojdova slagalica_, bavi se rešavanjem poznatog problema čiji je cilj da se od početnog(neuređnog) stanja slaglice(kvadratnog oblika veličine 16 ili 9 polja) dođe do uređenog redosleda polja. Rešavanje slagalice omogućeno je pomoću četiri algoritma(u osnovi svih algoritama koji su korišćeni nalazi se algoritam A*), koji slagalicu rešavaju nejednakim brzinama, te stoga aplikacija omogućava poređenje datih algoritama uz grafičku podršku. Na samom početku korisniku se daje mogućnost da odabere 2 od 4 algoritma koja želi da poredi, kao i dimenziju slagalice(koja može biti dimenzije _3x3_ ili _4x4_). Nakon odabira parametara, generiše se slagalica zadatih dimenzija koja nužno ne mora imati rešenje. Ukoliko slagalica ne može biti rešena, biće ispisana odgovarajuća poruka. U suprotnom ukoliko slagalica ima rešenje, u novootorenom prozoru se čeka dok jedan od algoritama ne reši slagalicu. Čim jedan algoritam(od dva koja je korisnik odabrao) završi rešavanje, pristupa se grafičkoj simulaciji rešavanja slagalice(ukoliko i drugi algoritam u međuvremenu reši slagalicu, grafička simulacija se izvršava paralelno za oba algoritma).

:hammer: ## Instalacija i pokretanje:
Aplikaciju je moguće jednostavno instalirati pomoću sledećih komandi terimnala:
```sh
git clone https://github.com/matf-pp/2020_Lojdova-slagalica.git
cd 2020_Lojdova-slagalica
pip install -r requirements.txt
```
Nakon preduzetih koraka, aplikacija će se klonirati sa gitHub-a, a sve neophodne biblioteke koje se nalaze u **requirements.txt** biće preuzete i instalirane. Kako bi se aplikacija pokrenula, neophodno je, u terminalu, zadati komandu
```sh
$ run main.py
```

:heavy_exclamation_mark: Alternativno, po preuzimanju(kloniranju), aplikacija se može instalirati i pokrenuti na sledeći način(neophodno je posedovati instaliran program **anaconda**):
```sh
conda env create -f enviroment.yml
conda activate loydpuzzle
run main.py
```

:open_file_folder: **Aplikacija je pisana u programskom jeziku python, uz korišćenje biblioteka pygame i tkinter**