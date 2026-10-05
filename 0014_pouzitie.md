---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.11.5
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

% #   <font color='#4B9DA9'> level 1 </font>
% ##  <font color='#547792'> level 2 </font>
% ### <font color='#E37434'> level 3 </font>
% {dropdown} <font color='#84B179'> Text </font>

# <font color='#4B9DA9'> Použitie  </font>


Mikrokontrolér s inštalovaným *MicroPython-om* komunikuje s nadradeným počítačom prostredníctvom sériového rozhrania USART. Pre komunikáciu je možné použiť niektorú z terminálových [aplikácií](https://github.com/cdleon/awesome-terminals).

## <font color='#547792'> picocom </font>

Pre testy a overenie funkčnosti inštalácie postačuje jednoduchý terminál [picocom](https://github.com/npat-efault/picocom), ktorý z repozitárov distribúcie Linuxu nainštalujem z konzoly príkazom

    sudo apt install picocom 

Použitie 

    picocom /dev/ttyACM0 --b 115200


```{figure} ./img/konzola.png
:width: 600px
:name: mp_0012a

Terminálový program *picocom* komunikujúci s interpreterom MicroPython v cykle *REPL*.
```

V *picocom* termináli pre skopírovanie programu do prostredia môžeme použiť skratky *CTRL+E* a *CTRL+D*. 


## <font color='#547792'> mpremote </font>

Rozsiahlejšie možnosti práce s *MicroPython-om* ponúka prostredie shell-programu [mpremote](https://docs.micropython.org/en/latest/reference/mpremote.html), ktorý nainštalujeme pomocou inštalátora *pip* 

    pip install --user mpremote

Jednou z jeho výhod je možnosť mapovania lokálneho disku do prostredia *MicroPython-u*, čím sa odstraňuje potreba opakovaného nahrávania programov do súborového systému mikrokontroléra pri testoch a ladení programov. 

    mpremote mount .

```{figure} ./img/mpremote.png
:width: 600px
:name: mp_0012b

Použitie programu *mpremote*.
```
    
*mpremote* podporuje v príkazom riadku príkazy, ktoré sa vykonajú na vzdialenom zariadení s *MicroPython-om*. Príkazy majú všeobecný formát

    mpremote <command name> [--options] [args...]
    
Podrobný popis príkazov je v dokumentácii k programu. Program spustený bez príkazov vyhladá a pripojí zariadenie s inštalovaným *MicroPython-om* a spustí shell v móde REPL. Zoznam podporovaných príkazov

    connect      - pripojenie zariadenia cez sériový port, TCP alebo mapované zariadenie
    disconnect   - odpojenie zariadenia
    soft_reset   - zmazanie histórie a reštart interpreteru
    repl         - nastavenie vlastností módu REPL 
    eval         - vykonanie prikazu a tlač výsledku
    exec         - spustenie kódu Pythonu
    run          - spustenie skriptu z lokálneho súborového systému
    fs           - spustenie príkazu pre vzdialený súborový systém (cat, ls, cp, rm, ...)
    df           - výpis volného/použitého pamäťového priestoru
    edit         - editácia súboru zo vzdialeného súborového systému
    mip          - inštalácia balíkov 
    mount        - pripojenie lokálneho súborového systému
    unmount      - odpojenie lokálneho súborového systému
    romfs        - správa obrazu inštalácie v pam§ti zariadenia
    rtc          - správa hodín reálneho času
    sleep        - pauza pre
    reset        - reset zariadenia
    bootloader   - spustenie bootloadru pre nahratie firmware

    
## <font color='#547792'> pyboard </font>


Pre prácu so zariadením s inštalovaným  *MicroPython-om* môžeme využiť aj skript [pyboard.py](./lib/pyboard.py), ktorý je súčasťou distribúcie *./tools/pyboard.py* (adresár v distribúcii z github-u). Pomocou skriptu je možné z lokálneho počítača ukladať, mazať súbory, vyvárať adresárovú štruktúru a spúšťat programy. 

    usage: pyboard.py [-h] [--device DEVICE] [-b BAUDRATE] [-u USER] [-p PASSWORD]
                      [-c COMMAND] [-w WAIT] [--follow] [-f]
                      [files [files ...]]


Doplňujúce argumenty pre *-f (--filesystem)*  

    ls
    ls ./adresar
    cp ./file ./
    rm ./file
    rmdir addr
    mkdir addr
    cat ./subor   vypis suboru na terminal resp
    cat./subor > lokalny.txt
    
Príklad použitia   
    
    python pyboard.py -f ls
    python pyboard.py -f cp ./test.py :
    
Ak sa prepíšeme resp. upravíme súbor *main.py* v koreňovom adresári tak aby obsahoval vykonateľný kód, tento sa po resete automaticky spustí. Spustenie nahratého kódu je jedmoducho možné aj priamo

     python pyboard.py test.py

     
