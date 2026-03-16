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


# Inštalácia Firmware 

V základnej verzii je možné **MicroPython** pre zvolenú platformu inštalovať **v štandardnej konfigurácii** priamo z predpripravených skompilovaných prostredí

* zo stránky https://micropython.org/download/ vybrať cielovú platformu
* stiahnúť príslušný **.hex** súbor
* štandardným postupom pomocou STM32CubeProgrammer naprogramovať mikrokontrolér
* po resete mikrokontroléra **MicroPython** komunikuje cez terminálový program

    picocom -b 115200 /dev/ttyACM0
    
    

##  Kompilácia zdrojového kódu 

V prípade kompilácie zo zdrojových kódov z github-u je potrebné mať nainštalované vývojové prostredie pre kompiláciu aplikácii STM32.
Z github-u stiahneme zdrojové kódy **MicroPython**-u

    git clone https://github.com/micropython/micropython
    
Skompilujeme vlastný kompilátor Pythonu do bytecode

    cd mpy-cross
    make

Prejdeme do adresára 

    cd ../ports/stm32
    
a spustíme

    make submodules
    
Na konci skompilujte firmware pre vašu cieľovú dosku, pre každú cieľovú dosku je vytvorený konfiguračný adresár v *./ports/stm32/boards* a meno adresára je zároveň príznakom pre kompilátor. Pre dosku napr. NUCLEO_L476RG je príkaz na kompiláciu potom

    make BOARD=NUCLEO_L476RG
    
Po kompilácii vznikol adresár *build-NUCLEO_L476RG*, v ktorom sa o.i. nachádzajú súbory firmware.bin, firmware.elf ...

    cd ./build-NUCLEO_L476RG

Pomocou programátora STM32Cube nahráme firmware do mikrokontroléra, resetujeme ho a spustíme terminálový program 

    picocom -b 115200 /dev/ttyACM0
    
V prípade, že to s budúcim experimentovaním v MicroPython-e nejako preženiete, môžete kedykoľvek zápisom firmware systém vrátiť do pôvodného stavu. 



## Test inštalácie 

Po resete by sa MicroPython mal ozvať v interaktívnom móde známym promptom

    >>>

Pre jednoduchšiu obsluhu hardware dosku sú pripravené hotové moduly Pythonu, príkazom

    >>> help()
 
dostaneme výpis vlastností modulu *pyb* . Povinná jazda - bliknutie s LED na doske potom vyzerá takto

    >>> import pyb
    >>> d = pyb.LED(1)
    >>> d.on()
    >>> d.off()
    
Podrobná dokumentácia k modulom, súborovému systému, hardware a pod. je v adresári ./docs, pomocou parametru v *make* si ju môžete vygenerovať do vhodného formátu.
