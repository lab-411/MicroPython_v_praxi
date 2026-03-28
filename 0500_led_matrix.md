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


#  Modul LED WS2812-64 

Modul obsahuje 64 farebných LED v sériovom zapojení usporiadaných do matice. Každá LED je riadené obvodom [WS2812](./doc/WS2812B.pdf). 


```{figure} ./img/led_ws812.jpg
:width: 350px
:name: mp_0500a

LED matica
```

##  Komunikačný protokol 

Pre komunikáciu využíva modul zjednodušenú konfiguráciu zbernice **SPI**. Nie je využitý hodinový synchronizačný signál zbernice SCLK, jednosmerná komunikácia na signále MOSI je časovaná nastavenými hodnotami intervalov.

```{figure} ./img/ws2512_kod.png
:width: 250px
:name: mp_0500b

Časovanie logických stavov L,H a RESET.
```



    
Každá farba LED je určená 8-bitovou hoddnotou, pre 3 farby (RGB) potrebujeme preto vyslať pre každú LED 24 bitov.

```{figure} ./img/ws2512_rgb.png
:width: 750px
:name: mp_0500c

Kódovanie farebnej informácie.
```

LED sú zpojené v sérii, každý riadiaci obvod si z dátového reťazca ponechá prvú informáciu o stave LED a zbytok dátového paketu pošle ďalej. Medzi jednotlivými paketmi je časový interval, ktorý je interpretovaný ako reset.


```{figure} ./img/ws2512_zapojenie.png
:width: 750px
:name: mp_0500d

Sériové zapojenie LED
```


```{figure} ./img/ws2512_sekvencia.png
:width: 550px
:name: mp_0500e

Princíp komunikácie na sériovej zbernici.
```

## Pripojenie  

SPI1, MOSI, bez CLK

    MICROPY_HW_SPI1_MOSI        (pin_PB5)
    
```{figure} ./img/ws2812_nucleo.png
:width: 550px
:name: mp_0500f

Pripojenie matice
```


## Knižnica

Pre riadenie matice LED je určená knižnica [lib_ws2812.py](./lib/lib_ws2812.py). Hodnoty farieb su kódované do bitovej postupnosti, ktorá je pomocou SPI rozhrania vyslaná do matice.

Kódovanie hodnôt v bitová postupnosti v registri SPI rozhrania pri bitovej rýchlosti 4Mbit/sec zabezpečuje správne časovanie prenosu:

    hodnota 0  - postupnosť 1000,  doba trvania stavu H - 250 usec
    hodnota 1  - postupnosť 1110,  doba trvania stavu H - 750 usec 

Na vyslanie 8 bitov pre LED potom potrebujeme vyslať 4 Byte v SPI, celkový počet pre jednu LED v matici je 12 Byte. 

    b7b6 b5b4 b3b2 b1b0

Doba prenosu dát pre jednu LED a celú maticu je potom

```{math}
\begin{align}
t_1 &= \dfrac{1}{4000000} \cdot 8 \cdot 4 \cdot 3 = 0.000024 s = 24 \mu s \\
\\
t_{64} &= 64 \cdot t_1 = 64 \cdot 24 = 1536 \mu s = 1.536 ms\\
\end{align}
```

Metódy knižnice

    WS2812(spi_bus=1, led_count=1, intensity=1)
    WS2812.show(data)
    
## Použitie
    
Inicializácia rozhrania

```Python3
from lib_ws2812 import *
matrix = WS2812(spi_bus=1, led_count=64)
```
    
### Príklad 1. Riadenie LED matice
    
Dáta pre rozsvietenie matice


```Python3
data = [
    (24, 0, 24), ( 0, 24, 0),  ( 0,  0, 24), (12, 12, 0), 
    (0, 12, 12), (12,  0, 12), (24,  0,  0), (21,  3, 0),
    (18, 6,  0), (15,  9, 0),  (12, 12,  0), ( 9, 15, 0),
    (6, 18,  0), ( 3, 21, 0),  ( 0, 24,  0), ( 8, 8,  8)
]

# rozsvieti 16 LED
matrix.show(data)     

# rozsvieti 64 LED
data=data*4
matrix.show(data)
```    

Opakovaná inicializácia knižnice zhasne LED.

### Príklad 2. Náhodné farby 

```Python3
import math

def data_generator(led_count):
    data = [(0, 0, 0) for i in range(led_count)]
    step = 0
    while True:
        red = int((1 + math.sin(step * 0.1324)) * 127)
        green = int((1 + math.sin(step * 0.1654)) * 127)
        blue = int((1 + math.sin(step * 0.1)) * 127)
        data[step % led_count] = (red, green, blue)
        yield data
        step += 1


for data in data_generator(matrix.led_count):
    matrix.show(data)
    pyb.delay(10)
```

### Príklad 3.Demonštračný program  

Demonštrácia vlastností LED matice je v súbore [demo_ws2812.py](./lib/demo_ws2812.py).

```Python3
import math
from lib_ws2812 import *
from demo_ws2812 import *
matrix = WS2812(spi_bus=1, led_count=64, intensity=0.05)
```

Spustenie príkladu

```Python3
while(True):
  anim_1 = animation_1(matrix.led_count)
  for i in range(240):
    matrix.show(next(anim_1))
      
  anim_2 = animation_2(matrix.led_count)
  for i in range(240):
    matrix.show(next(anim_2))
      
  anim_3 = animation_3(matrix.led_count)
  for i in range(240):
    matrix.show(next(anim_3))
```

Nahrati knižnice a demo programu do MicroPython

    python ./py/pyboard.py -d /dev/ttyACM0 -f cp lib_ws2812.py :./lib_ws2812.py
    python ./py/pyboard.py -d /dev/ttyACM0 -f cp demo_ws2812.py :./demo_ws2812.py
        
        
