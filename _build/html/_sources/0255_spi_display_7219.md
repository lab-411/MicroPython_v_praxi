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



# <font color='#4B9DA9'>  LED Display 7219  </font>

Modul 7-segmentového displeja je riadený obvodom [MAX7219/MAX7221](./doc/max7219.pdf). Komunikácia s displejom je pomocou zbernice SPI, radič displeja podporuje sériové reťazenie obvodov na zbernici SPI (*Daisy-Chain*). 

```{figure} ./img/display_led_max7219.png
:width: 500px
:name: mp_0255c

Modul displeja.
```

## <font color='#547792'> Popis </font>

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
:name: mp_0255g

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

## <font color='#547792'> Zapojenie displeja </font>


Štandardné zapojenie modulu podľa doporučenia výrobcu ja na obrázku.

```{figure} ./img/ic_max7219_2.png
:width: 450px
:name: mp_0255e

Zapojenie displeja.
```
Príklad pripojenie modulu displeja ku kitu NUCLEO-64. 

    DIN  -> PB15   
    CLK  -> PB13
    CS   -> PB1
    +5V
    GND 

```{figure} ./img/spi2_led_max7219.png
:width: 300px
:name: mp_0255a

Pripojenie modulu displeja.
```


## <font color='#547792'> Programovanie </font>

Pre obsluhu modulu 7-segmentového displaje je vytvorená knižnica [lib_max7219](./lib/lib_max7219.py)

:::{dropdown} <font color='#84B179'>  Zdrojový kód knižnice </font>
```{literalinclude} ./lib/lib_max7219.py
:lineno-start: 1
```
:::


```{dropdown} <font color='#84B179'> Aplikačné rozhranie </font>

Konštruktor:
    
    SevenSegment(digits=8, 
                 scan_digits=MAX7219_DIGITS, 
                 baudrate=SPI_BAUDRATE, 
                 cs=SPI_CS, 
                 spi_bus=SPI_BUS, 
                 reverse=False)

Metódy:
    
    clear()
    brightness(intensity)
    command(register, data)
    text(text)
    number(val)
    scroll(rotate, reverse, flush)
    message(text, delay)
```


```{dropdown} <font color='#84B179'> Inicializácia  </font>

Uložte knižnicu [lib_max7219](./lib/lib_max7219.py) do lokálneho pracovného adresáru a spustite nasledujúci skript, ktorý knižnicu nahrá do prostredia MicroPythonu.

      mpremote fs mkdir lib
      mpremote fs cp lib_max7219.py :./lib/lib_max7219.py
```

## <font color='#547792'> Príklady </font>

### <font color='#FF4400'> Komunikácia s displejom </font>

Základná komunikácia s displejom pomocou API funkcií.

```Python
from pyb import Pin
from time import sleep
from lib.lib_max7219 import *

display = SevenSegment(digits=8, scan_digits=8, cs='PB1', spi_bus=2, reverse=True)
display.clear()

sleep(0.5)
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

### <font color='#FF4400'> Sériové zapojenie displejov </font>

Príklad komunikácie s displejmi zapojenými v sérii pomocou priameho zápisu do registrov. V programe nie je použité dekódovanie znakov pomocou dekóderu radiča, funkcia *get_char2()* prevádza kód znaku do kódu aktívnych segmentov pre zobrazenie na displeji. 

```Python
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

