## Licenta Neamtu Maria Ramona 2020


#### Instalare dependintelor software pe device-ul Raspberry Pi
1. updatam package-manager-ul sistemului de operare `sudo apt update`
2. ne asiguram ca `git` este instalat cu comanda `git --version`. Daca nu este instalat il instalam cu comanda `sudo apt install git`
3. ne asiguram ca `python3` accesandu-l din terminal. Daca nu este instalat il instalam cu comanda `sudo apt install python3-pip`
4. instalam libraria necesara pentru citirea senzorilor cu comanda `sudo pip3 install Adafruit_DHT`
5. cream cont pe platforma https://www.dataplicity.com si rulam comenzile pe care aceasta ni le ofera
6. se cloneaza proiectul curent cu comanda `git clone https://github.com/ramona1996/licenta-cod-python.git`


#### Pasii pentru rularea aplicatiei
1. se porneste aplicatia server cu comanda `sudo python3 main.py`
2. accesam device-ul la adresa https://www.dataplicity.com/devices/ pentru a ne asigura ca optiunea `wormhole` este enabled si pentru a verifica url-ul public la care este disponibila aplicatia
3. accesul la serverul de pe device este public. De exemplu https://doctoral-pug-9165.dataplicity.io/

#### Diagrama de flux
![gauge](https://raw.githubusercontent.com/ramona1996/licenta-cod-python/master/preview/diagrama_flux.jpg)


#### Exemple de grafice (datele sunt generate cu valori random):

*temperatura/umiditate senzori*
![gauge](https://raw.githubusercontent.com/ramona1996/licenta-cod-python/master/preview/prev1.PNG)

*grafic comparativ in timp*
![comparatie](https://raw.githubusercontent.com/ramona1996/licenta-cod-python/master/preview/prev2.PNG)

*grafic de corelatie*
![corelatie](https://raw.githubusercontent.com/ramona1996/licenta-cod-python/master/preview/prev3.PNG)