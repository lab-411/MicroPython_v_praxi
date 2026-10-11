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

%#   <font color='#4B9DA9'>  Nazov </font>
%##  <font color='#547792'> Popis </font>
%##  <font color='#547792'> Zapojenie </font>
%##  <font color='#547792'> Programovanie </font>
%### <font color='#E37434'> Knižnica </font>
%### <font color='#E37434'> API </font>
%### <font color='#E37434'> Príklady </font>

# <font color='#4B9DA9'>  LED Display 7219  </font>

##  <font color='#547792'> Popis </font>

Moduly 7-segmentových displejov s radičmi [MAX7219/MAX7221](./doc/max7219.pdf) sú dostupné v rôznych verziách. Moduly umožňujú zobrazenie čísel ako aj niektorých znakov. Komunikácia s displejom je pomocou zbernice SPI, radič displeja podporuje sériové radenie modulov na zbernici SPI (*Daisy-Chain*). 

```{figure} ./img/display_led_max7219.png
:width: 500px
:name: mp_0255c

Modul 7-segmentového displeja.
```

##  <font color='#547792'> Zapojenie </font>

Štandardné zapojenie modulu podľa doporučenia výrobcu je na obrázku.

```{figure} ./img/ic_max7219_2.png
:width: 450px
:name: mp_0255e

Zapojenie displeja.
```
Príklad pripojenie modulu displeja ku kitu NUCLEO-64 pre rozhranie SPI2 

    VCC  -> +5V
    GND  -> GND
    DIN  -> PB15  
    CS   -> PB1
    CLK  -> PB13
    

```{figure} ./img/spi2_led_max7219.png
:width: 300px
:name: mp_0255g

Pripojenie modulu displeja.
```


##  <font color='#547792'>  Programovanie </font>

Radič displeja MAX7219 umožňuje pripojenie 8-znakového 7-segmentového displeja so spoločnou katódou, sĺpcového LED displeja alebo 64 samostatných LED. Obvod obsahuje BCD dekóder pre 7-segmentové znaky, obvody pre multiplexovanie znakov displeja, riadenie jasu a statickú pamäť RAM 8x8 pre každý znak displeja. Riadnie displeja umožňuje adresovať každý znak displeja individuálne, bez potreby prepísania obsahu celého displeja. Obvod je k mikroprocesoru pripojený pomocou rozhrania SPI s maximálnou frekvenciou hodím 10MHz. 

```{figure} ./img/ic_max7219_1.png
:width: 650px
:name: mp_0255d

Vnútorné zapojenie obvodu [MAX7219](./doc/max7219.pdf).
```

Obvod obsahuje 16-bitový posuvný register, ktorého obsah je po naplnení z rozhrania SPI dekódovaný podľa nasledujúceho formátu

```{figure} ./img/ic_max7219_3.png
:width: 750px
:name: mp_0255f

Sériový formát dát v posuvnom registri.
```
Popis polí vo formáte dát 

* **D15 ... D12** - nepoužité bity
* **D11 ... D08** - adresa registru alebo znaku 
* **D07 ... D00** - dáta pre register alebo adresovaný znak

Adresné bity (D11 ... D08) majú nasledujúci význam

```{figure} ./img/ic_max7219_4.png
:width: 400px
:name: mp_0255x

Dekódovanie adresných bitov.
```

Popis registrov

* **No-Op** - používa sa pri sériovom radení registrov, kedy v sekvencii dát chceme osloviť niektorý z radičov a požadujeme, aby ostatné nereagovali
* **Digit 0 ... Digit 7** - adresa znaku
* **Decode Mode** - nastavenie dekódovania dát pre zobrazenie znaku na displeji v BCD kóde alebo priamym riadením LED 
* **Intensity** - nastavenie jasu displeja
* **Scan Limit** - počet zobrazovaných znakov
* **Shutdown** - zhasnutie displeja a prechod do módu s malou spotrebou

Dáta pre register **Decode Mode** určujú formát dekódovania znakov. Hodnota **0xFF** nastavuje dekódovanie znakov v BCD kóde, hodnote **0x00** priame zobrazenie LED.

```{figure} ./img/ic_max7219_6.png
:width: 750px
:name: mp_0255h

Nastavenie typu dekódovania dát pre znaky displeja.
```


### <font color='#E37434'> Knižnica </font>

Pre obsluhu modulu 7-segmentového displeja je vytvorená knižnica [lib_max7219](./lib/lib_max7219.py). Pre riadenie displeja je potrebné inicializovať SPI rozhranie a definovať pin CS (chip select).

### <font color='#E37434'> API </font>

%```{dropdown} <font color='#84B179'> Aplikačné rozhranie </font>

**Konštruktor**
    
    SevenSegment(spi, cs, digits=8, scan_digits=8, reverse=False)
    
        spi         - objekt SPI rozhrania
        cs          - meno pinu pre chip-select
        digits      - počet znakov displeja
        scan_digits - počet zobrazovaných znakov
        reverset    - smer zobrazenia

**Metódy**
    
    clear()                 - zhasnutie a zmazanie displeja
    brightness(intensity)   - nastavenie jasu
    command(register, data) - priamy zápis do registrov radiča 
    text(text)              - zobrazenie textu
    number(val)             - zobrazenie čísla a desatinnej bodky
    scroll(rotate, reverse, flush) 
                            - rotacia zobrazenia o jednu poziciu
    message(text, delay)    - zobrazenie textu s posúvaním
%```


Pre riadenie displeja je potrebné inicializovať objekt SPI rozhrania z modulu *pyb* a definovať meno pinu CS (chip select).

    from pyb import SPI
    from lib_max7219 import *
    spi = SPI(2, SPI.CONTROLLER, baudrate=100000, polarity=0, phase=0, crc=None)
    display = SevenSegment(spi, 'PB1')


### <font color='#E37434'> Príklady </font> 

````{dropdown} <font color='#84B179'> Riadenie 8-znakového displeja </font>

Základná komunikácia s displejom pomocou API funkcií.

```{code-block} Python
from pyb import SPI
from time import sleep
from lib_max7219 import *
spi = SPI(2, SPI.CONTROLLER, baudrate=100000, polarity=0, phase=0, crc=None)
display = SevenSegment(spi, 'PB1')

display.text("HELLO")

sleep(1)
display.number(3.14159)

sleep(1)
display.message("--- HELLO ---        ")

sleep(1)
display.clear()
for i in range(32):
    s = f'{i:2d}--{i:04x}'
    display.text(s)
    sleep(0.5)
    
```
````


````{dropdown} <font color='#84B179'> Sériové zapojenie displejov </font>


Príklad komunikácie s displejmi zapojenými v sérii pomocou priameho zápisu do registrov. V programe nie je použité dekódovanie znakov pomocou dekóderu radiča, funkcia *get_char2()* prevádza kód znaku do kódu aktívnych segmentov pre zobrazenie na displeji. 

```{code-block} Python
from pyb import Pin
from time import sleep
from lib.lib_max7219 import *

display = SevenSegment(digits=16, scan_digits=8, cs='PB1', spi_bus=2, reverse=True)
display.clear()
display.brightness(5) 
  
display.command(0x09,0x00)     # mod bez dekodovania
s1 = '    1234'
s2 = '--AHOJ--'
for x in range(8):
    display._write([8-x, get_char2(s2[x]), 
                    8-x, get_char2(s1[x])] )
    sleep(0.25)
```
````
