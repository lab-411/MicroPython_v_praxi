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


#  <font color='#4B9DA9'>  LED WS2812-64 </font>

Modul obsahuje 64 farebných LED v sériovom zapojení usporiadaných do matice. Každá LED obsahuje obvod [WS2812](./doc/WS2812B.pdf), pomocou komunikačného protokolu je možné riadiť farbu a intenzitu každej LED na module. 


```{figure} ./img/led_ws812.jpg
:width: 320px
:name: mp_0500a

LED modul WS2812.
```

##  <font color='#547792'>  Komunikácia </font>

Komunikácia s obvodmi riadiacimi LED je sériová, po jednom dátovom vodiči, s pevným časovaním logických stavov. 


```{code-cell} ipython3  
:tags: ["remove-cell"]
from src.utils import *

data = r'''
include(lib_base.ckt)
include(lib_user.ckt)
include(lib_time.ckt)
include(lib_color.ckt)

#Grid(10,3)
move to (0,0.5);
level(0.5,L,D)
pulse(1 ,0,LH);  {color_red; "$T_{0H}$" at last[].n+(0, 0.25) above; color_black; }
pulse(2,0,HL);   {color_red;"$T_{0L}$" at last[].n+(0, 0.25) above; color_black;}

level(1,L,D);
pulse(2,0,LH); {color_red;"$T_{1H}$" at last[].n+(0, 0.25) above; color_black;}
pulse(1,0,HL); {color_red;"$T_{1L}$" at last[].n+(0, 0.25) above; color_black;}
level(0.5,L,D);

color_red;
line from (0.5, 0) to (0.5,1.5) dotted; line <-> from (0.5, 1) to (1.5, 1);
line from (1.5, 0) to (1.5,1.5) dotted; line <-> from (1.5, 1) to (3.5, 1);
line from (3.5, 0) to (3.5,1.5) dotted;

line from (4.5, 0) to (4.5,1.5) dotted; line <-> from (4.5, 1) to (6.5, 1);
line from (6.5, 0) to (6.5,1.5) dotted; line <-> from (6.5, 1) to (7.5, 1);
line from (7.5, 0) to (7.5,1.5) dotted;

color_black;
move to (0,2.5);
level(0.5,H,D);
pulse(5 ,0.025, HL);
pulse(1 ,0.9, LH);
level(1.5,H,D);

color_red;
line from (0.5+0.022*6, 2) to (0.5+0.022*6, 3.5) dotted;
line from (5.5+0.9, 2) to (5.5+0.9, 3.5) dotted;
line <-> from (0.5+0.022*6, 3) to (5.5+0.9, 3); "$T_{reset}$" at last line.center above;
'''

_ = cm_compile('img_0500k', data,  dpi=600)   
```


```{figure} ./src/img_0500k.png
:width: 400px
:name: img_0500k

Časovanie logických stavov L,H a RESET.
```



Každá farba LED je určená 8-bitovou hodnotou, pre 3 farby (RGB) potrebujeme preto vyslať pre každú LED postupnosť 24 bitov.

```{code-cell} ipython3  
:tags: ["remove-cell"]
from src.utils import *

data = r'''
include(lib_base.ckt)
include(lib_user.ckt)
include(lib_time.ckt)
include(lib_color.ckt)

command"\sf"
color_dark_green;
d=0.7;
level(0.5,X)
data(d,G7);
data(d,G6);
data(d,G5);
data(d,G4);
data(d,G3);
data(d,G2);
data(d,G1);
data(d,G0);

color_red;
data(d,R7);
data(d,R6);
data(d,R5);
data(d,R4);
data(d,R3);
data(d,R2);
data(d,R1);
data(d,R0);

color_blue;
data(d,B7);
data(d,B6);
data(d,B5);
data(d,B4);
data(d,B3);
data(d,B2);
data(d,B1);
data(d,B0);
level(0.5,X)
'''

_ = cm_compile('img_0500c', data,  dpi=600)   
```


```{figure} ./src/img_0500c.png
:width: 750px
:name: img_0500c

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


##  <font color='#547792'> Zapojenie </font> 

Pripojenie modulu je pomocou troch vodičov, napájanie +5V, zem a komunikácia. Pre komunikáciu s modulom je použitá jednodušená verzia zbernice **SPI**. Nie je použitý hodinový synchronizačný signál zbernice SCLK a jednosmerná komunikácia s modulom je prostredníctvom signálou MOSI. 



```{figure} ./img/ws2812_nucleo.png
:width: 450px
:name: mp_0500f

Pripojenie modulu k Nucleo-64 cez rozhranie SPI1.
```


SPI1, MOSI, bez CLK

    MICROPY_HW_SPI1_MOSI        (pin_PB5)
    



##  <font color='#547792'> API </font> 

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
    
##  <font color='#547792'> Príklady </font> 

%--------------------------------------------------------------------
    
:::{dropdown} <font color='#84B179'> Príklad 1. Riadenie farieb LED matice </font>
    
Inicializácia rozhrania a dáta pre rozsvietenie LED matice

```Python3
from lib_ws2812 import *
matrix = WS2812(spi_bus=1, led_count=64)

data = [
    (24, 0, 24), ( 0, 24, 0),  ( 0,  0, 24), (12, 12, 0), 
    (0, 12, 12), (12,  0, 12), (24,  0,  0), (21,  3, 0),
    (18, 6,  0), (15,  9, 0),  (12, 12,  0), ( 9, 15, 0),
    (6, 18,  0), ( 3, 21, 0),  ( 0, 24,  0), ( 8, 8,  8)
]

matrix.show(data)   # rozsvieti 16 LED  

data=data*4
matrix.show(data) # rozsvieti 64 LED
```    

Opakovaná inicializácia knižnice zhasne LED.
:::

%--------------------------------------------------------------------

:::{dropdown} <font color='#84B179'> Príklad 2. Náhodné farby  </font>


```Python3
import math

from lib_ws2812 import *
matrix = WS2812(spi_bus=1, led_count=64)

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
:::

%--------------------------------------------------------------------

:::{dropdown} <font color='#84B179'> Príklad 3. Demonštračný program    </font>

Demonštrácia vlastností LED matice je v súbore [demo_ws2812.py](./lib/demo_ws2812.py).

```Python3
import math
from lib_ws2812 import *
from demo_ws2812 import *
matrix = WS2812(spi_bus=1, led_count=64, intensity=0.05)

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

:::

%Nahrati knižnice a demo programu do MicroPython
%
%    python ./py/pyboard.py -d /dev/ttyACM0 -f cp lib_ws2812.py :./lib_ws2812.py
%    python ./py/pyboard.py -d /dev/ttyACM0 -f cp demo_ws2812.py :./demo_ws2812.py
        
        
