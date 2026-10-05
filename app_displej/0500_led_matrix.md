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


#  <font color='#4B9DA9'> LED modul WS2812 </font>

##  <font color='#547792'> Popis </font>

Modul obsahuje 64 farebných LED usporiadaných do matice v sériovom zapojení. Každá LED obsahuje obvod [WS2812](../doc/WS2812B.pdf),
informácia o intenzite svetla farby každej LED na module sa riadi prostredníctvom dátového paketu, v ktorom sú usporiadané trojice 8-bitových dát (GRB). Pri príjme paketu dáta prechádzajú postupne LED diódami, pričom každá LED dióda prvú trojicu prijatých dát použíje na nastavenie farebných zložiek a zbytok paketu odošle nasledujúcej LED dióde. 
Moduly je možné zapájať za sebou v sérii, modul obsahuje dva konektory, jeden pre pripojenie napájania a vstupu dát, druhý pre propojenie nasledujúceho modulu. 


```{figure} ./img/led_ws812.jpg
:width: 320px
:name: mp_0500a

LED modul WS2812-64.
```


##  <font color='#547792'> Zapojenie </font>

Pripojenie modulu k mikrokontroléru je pomocou troch vodičov, napájanie +5V, zem a dátový vodič. 

```{code-cell} ipython3  
:tags: ["remove-cell"]

import sys
sys.path.append('../')

from src.utils import *

data = r'''
log_init  

include(lib_base.ckt)
include(lib_user.ckt)
include(lib_color.ckt)
include(lib_time.ckt)

command"\sf"

define(`WS2812', `[
  rgbfill(fill_light_yellow, {BX: box wid 2 ht 5*lg_pinsep; })
      lg_pin(BX.nw - (0, 1*lg_pinsep), Din,  Pin4, w, 4, );
      lg_pin(BX.nw - (0, 4*lg_pinsep), Vss,  Pin3, w, 3, );
      lg_pin(BX.ne - (0, 1*lg_pinsep), Vcc,  Pin1, e, 1, );
      lg_pin(BX.ne - (0, 4*lg_pinsep), Dout, Pin2, e, 2, );
]')

LED1: WS2812; 


line from LED1.Pin2.end right_ 1;
line up_ to (Here, LED1.Pin4) then right_ 1;
right_ ; 
LED2: WS2812 with .Pin4.end at Here;

line from LED2.Pin2.end right_ 0.5 ;
line right_ 1.0 dashed;
line up_ to (Here, LED2.Pin4) then right_ 1 dashed;
right_ ; 
LED3: WS2812 with .Pin4.end at Here;

"LED1" at LED1.s below;
"LED2" at LED2.s below;
"LEDn" at LED3.s below;

# zemny spoj
line from LED1.Pin3.end down_ 1;
DD1: dot;
line to (LED2.Pin3.end, Here);
DD2: dot; {line to LED2.Pin3.end; }
line to (LED2.Pin2.end, Here)+(0.5,0);
line to (LED3.Pin3.end, Here) dashed;
DD3: dot;  {line to LED3.Pin3.end; }
line to ( LED3.Pin2.end, Here);
tconn(right_ 2,M); "GND" ljust;
tconn(from LED3.Pin2.end right_ 2,M); "Out" ljust;
tconn(from DD1 left_ 1.5,M);  "GND" rjust;

# napajanie
line from LED1.Pin1.end right_ 0.25; 
DD5: dot; { capacitor(down_ to (Here, DD1)+(0, 0.85)); llabel(,\sf C1,);  line to ((Here, DD1)); dot; }
line up_ 0.75;
DD6: dot;
line right_ to (LED2.Pin1.end, Here)+(0.25, 0);
DD7: dot;
line to (Here, LED2.Pin1.end); 
dot; { capacitor(down_ to (Here, DD1)+(0, 0.85)); llabel(,\sf C2,);line to ((Here, DD1)); dot; }
line to LED2.Pin1.end;
line from DD7 right_ 0.35
line to (LED3.Pin4.end, Here) dashed;
line to (LED3.Pin1.end, Here) + (0.25,0);
DD8: dot;
line to (Here, LED3.Pin1.end);
dot; { capacitor(down_ to (Here, DD1)+(0, 0.85));  llabel(,\sf Cn,); line to ((Here, DD1)); dot; }
line to LED3.Pin1.end;
tconn(from DD8 right_ 1.75,M); "+5V" ljust;
tconn(from DD6 left_ 4.75,M); "+5V" rjust;
tconn(from LED1.Pin4.end left_ 1.5,M); "In" rjust;
'''

_ = cm_compile('img_0500f', data,  dpi=600, path='../src')   
```

```{figure} ../src/img_0500f.png
:width: 800px
:name: mp_0500d

Sériové zapojenie v LED module.
```

Komunikácia s obvodmi WS2812 je sériová, po jednovodičovej zbernici, s pevným časovaním stavov L a H, tieto sa odlišujú dĺžkou impulzu na zbernici. Jednotlivé pakety sú oddelené časovým intervalom reprezentujúcim reset zbernice.


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

_ = cm_compile('img_0500k', data,  dpi=600, path='../src')  
```


```{figure} ../src/img_0500k.png
:width: 400px
:name: img_0500k

Časovanie logických stavov L,H a RESET.
```

| Interval    | Min            | Max     | 
| :---        | :----          |  :---- | 
| $T_{reset}$ | $300 \mu s$    | $\infty$       | 
| $T_{0H}$    | $220 ns$       | $380 n s$     |
| $T_{0L}$    | $750 ns$       | $1.6 \mu s$   |
| $T_{1H}$    | $750 ns$       | $1.6 \mu s$     |
| $T_{1L}$    | $220 ns$       | $420 n s$   |


Pre komunikáciu mikrokontroléra s modulom môžeme použiť niekoľko metód, najjednoduchšou je priame generovanie dát časovaním pinu mikrokontroléra. Elegantnejšou metódou je je použitie rozhranie  [SPI](../0250_spi.md), pre prenos dát do modulu je použitý len signál MOSI, správne časovanie zbernice dosiahneme nastavením frekvencie hodín rozhrania. 

```{figure} ./img/ws2812_nucleo.png
:width: 450px
:name: mp_0500f

Pripojenie modulu k Nucleo-64 cez rozhranie SPI1.
```

##  <font color='#547792'>  Programovanie </font>

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

_ = cm_compile('img_0500c', data,  dpi=600, path='../src')   
```


```{figure} ../src/img_0500c.png
:width: 750px
:name: img_0500c

Kódovanie farebnej informácie.
```

LED sú zpojené v sérii, každý riadiaci obvod si z dátového reťazca ponechá 24 bite o stave LED a zbytok reťazca prepošle k nasledujúcej LED. Informácie o stave LED sú za sebou bez medzier, po ukončení vysielania je medzi jednotlivými reťazcami časový interval dlhší ako $300 \mu s$, ktorý je interpretovaný ako reset komunikácie.

```{code-cell} ipython3  
:tags: ["remove-cell"]
from src.utils import *

data = r'''
include(lib_base.ckt)
include(lib_user.ckt)
include(lib_time.ckt)
include(lib_color.ckt)

command"\sf"
move to (1,3.5); "LED1" rjust;
level(1,X,D)
data(2, 24 bit)
data(2, 24 bit)
data(2, 24 bit)

level(1,X,D); 
 
{   color_red;
    L1: last [].w; line from L1+(0,1) down_ 4.5;
    L2: last [].e; line from L2+(0,1) down_ 4.5;
    line <- from L1+(0, 0.75) left_ 1;
    line <- from L2+(0, 0.75) right_ 1;
    line from L1+(0, 0.75) to L2+(0, 0.75) dashed;
   "Reset" at last [].c+(0,1.25); 
   color_black;
}

data(2, 24 bit)
data(2, 24 bit)
data(2, 24 bit)
level(1,X,D)

move to (1,2.5); "LED2" rjust;
level(3,X,D)
#data(2, 24 bit)
data(2, 24 bit)
data(2, 24 bit)
level(3,X,D)
#data(2, 24 bit)
data(2, 24 bit)
data(2, 24 bit)
level(1,X,D)

move to (1,1.5); "LED3" rjust;
level(5,X,D)
#data(2, 24 bit)
#data(2, 24 bit)
data(2, 24 bit)
level(5,X,D)
#data(2, 24 bit)
#data(2, 24 bit)
data(2, 24 bit)
level(1,X,D)

move to (1,0.5);  "LED4" rjust;
level(15,X,D)
'''

_ = cm_compile('img_0500e', data,  dpi=600, path='../src')    
```

```{figure}  ../src/img_0500e.png
:width: 650px
:name: mp_0500e

Princíp komunikácie na sériovej zbernici.
```


### <font color='#E37434'> Knižnica </font>

Pre riadenie matice LED je určená knižnica [lib_ws2812.py](./lib/lib_ws2812.py). Hodnoty farieb su kódované do bitovej postupnosti, ktorá je pomocou SPI rozhrania vyslaná do matice.

Kódovanie hodnôt bitová postupnosti je pomocou dátového registra SPI rozhrania pri bitovej rýchlosti 4Mbit/sec, ktorá zabezpečuje správne časovanie na dátovej zbernici:

    hodnota 0  - postupnosť bitov 1000,  doba trvania stavu H - 250 nsec, L - 750 nsec 
    hodnota 1  - postupnosť bitov 1110,  doba trvania stavu H - 750 nsec, L - 250 nsec 

Na vyslanie 8 bitov pre jednu farbu LED potom potrebujeme vyslať 4 Byte v SPI rozhraní, pre nastavenie stavu jednej LED potrebujeme 12 Byte ktoré obsahujú časovanie binárnych hodnôt: 

    g7g6 g5g4 g3g2 g1g0  r7r6 r5r4 r3r2 r1r0  b7b6 b5b4 b3b2 b1b0
    
Prevod medzi hodnotou byte a jeho časovaním uskutočníme pomocou jednoduchého algoritmu

```{code-block} Python3    
# green     - hodnota farebnej zlozky v RGB
# intensity - celkova intenzita svetla LED diody

buf_bytes = (0x88, 0x8e, 0xe8, 0xee) # dvojice stavov 00,01,10,11
mask = 0x03                          # maska 00000011
green = int(green * intensity)       # hodnota pre LED, 8bit       

# priradenie dvojic do pola data[] (4 Byte) pre vyslanie v SPI 
data[index  ] = buf_bytes[green >> 6 & mask]
data[index+1] = buf_bytes[green >> 4 & mask]
data[index+2] = buf_bytes[green >> 2 & mask]
data[index+3] = buf_bytes[green & mask     ]
```

Doba prenosu dát pre jednu LED je (4 Byte po 8 bitov a 3 farby)

```{math}
\begin{align}
t_1 &= \dfrac{1}{4000000} \cdot 8 \cdot 4 \cdot 3 = 0.000024 s = 24 \mu s \\
\end{align}
```
a pre celú maticu 64 LED diód je potom doba trvania celého paketu

```{math}
\begin{align}
t_{64} &= 64 \cdot t_1 = 64 \cdot 24 = 1536 \mu s = 1.536 ms\\
\end{align}
```

### <font color='#E37434'> API </font>

Knižnica pre riadenie LED matice je implementovaná v triede WS2812:

    Konštruktor:
    
    WS2812(spi_bus, led_count, intensity)
    
        spi_bus         - SPI rozhranie 
        led_count       - počet LED modulu
        intensity       - jas modulu 0..1
    
    Metódy:
    
    show(data)
    
        data            - pole hodnôt GRB pre LED v tvare 
                          [(g1,r1,b1), (g2,r2,b2), ... ]


%--------------------------------------------------------------------
                          
### <font color='#E37434'> Príklady </font> 

    
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
        
##  <font color='#547792'> Literatúra a odkazy </font>
        
* [MicroPython WS2812 driver](https://github.com/JanBednarik/micropython-ws2812)
* [WS2815 Datasheet](https://www.ledyilighting.com/wp-content/uploads/2025/02/WS2812B-datasheet.pdf)
* [WS2812 Pattern Editor](https://yomotherboard.com/ws2812-pattern-editor/)
* [Awesome ws2812](https://github.com/PabloCastellano/awesome-ws2812)
