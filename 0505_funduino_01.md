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

# <font color='#4B9DA9'>  Modul Funduino 1.0  </font>

Funduino je populárny výukový modul pre Arduino UNO, ktorý je osadený základnými perifériami a konektormi pre pripojenie ďaľších zariadení. 

```{figure} ./img/multi_shield_10.png
:width: 350px
:name: mp_0505a

Modul Funduino, verzia 1.0.
```
## <font color='#547792'> Popis a zapojenie </font>

Zapojenie modulu je na obrázku

```{figure} ./img/fun01_zapojenie.gif
:width: 750px
:name: mp_0505b

Zapojenie modulu Funduino, verzia 1.0.
```

### <font color='#E37434'> LED diódy </font>

Na module sú zapojené 3 LED diódy, ich anódy sú pripojené cez rezistor 1k k napájaciemu napätiu +5V. Katódy sú pripojené k pinom mikrokontroléra, dióda sa rozsvieti pri stave piny LOW. Pripojenie LED je uvedené na nasledujúcom obrázku a v tabulke.

```{code-cell} ipython3  
:tags: ["remove-cell"]
from src.utils import *

data = r'''
include(lib_base.ckt)
include(lib_stm32.ckt)
include(lib_user.ckt)

command"\sf"

DT1: dot; {up_; power(1, +5V);}

down_; 
D1: diode(1); rlabel(,\sf D_1,); {em_arrows(N,315,0.45) with .Tail at last [].se; }
resistor(1,E); llabel(,\sf 1k,);
line down_ 0.25 then right_ 1; T1: tbox(\sf D13,1,)

line from DT1 left_ 1.5; DT2: dot;
down_; 
D2: diode(1); rlabel(,\sf D_2,); {em_arrows(N,315,0.45) with .Tail at last [].se; }
resistor(1,E);llabel(,\sf 1k,);
line down_ to (Here, T1)+(0,-0.5);
line right_ to (T1.w, Here); T2: tbox(\sf D12,1,)

line from DT2 left_ 1.5; DT3: dot;
down_; 
D3: diode(1); rlabel(,\sf D_3,); {em_arrows(N,315,0.45) with .Tail at last [].se; }
resistor(1,E);  llabel(,\sf 1k,);
line down_ to (Here, T2)+(0,-0.5);
line right_ to (T2.w, Here); T3: tbox(\sf D11,1,)

line from DT3 left_ 1.5; #DT3: dot;
down_; 
D4: diode(1); rlabel(,\sf D_4,); {em_arrows(N,315,0.45) with .Tail at last [].se; }
resistor(1,E);  llabel(,\sf 1k,);
line down_ to (Here, T3)+(0,-0.5);
line right_ to (T3.w, Here); T4: tbox(\sf D10,1,)
'''

_ = cm_compile('img_0505w', data,  dpi=600)   
```

```{figure} ./src/img_0505w.png
:width: 350px
:name: img_0505w

Zapojenie LED diód na module Funduino.
```

| Funduino | Arduino | NUCLEO-64 |
| :---: | :----: | :----: |
| D1    | D13      | PA5     |
| D2    | D12      | PA6     |
| D3    | D11      | PA7     |
| D4    | D10      | PB5     |


:::{admonition} Poznámka
K pinu PA5 je doske NUCLEO-64 štandardne pripojená zelená LED, ktorá ovlyvňuje stav LED D1.  
:::

    
```{dropdown} <font color='#84B179'> Príklad riadenia LED </font>

Program rozsvietenia a postupn0 zhasnutia LED
    
    from pyb import Pin
    from time import sleep

    d1 = Pin('PA5', Pin.OUT)
    d2 = Pin('PA6', Pin.OUT)
    d3 = Pin('PA7', Pin.OUT)
    d4 = Pin('PB6', Pin.OUT)

    d1.off(); d2.off(); d3.off(),  d4.off()

    sleep(0.5)
    d1.on()

    sleep(0.5)
    d2.on()

    sleep(0.5)
    d3.on()

    sleep(0.5)
    d4.on()

```

### <font color='#E37434'> Tlačítka </font>

Na module sa nachádzajú tri tlačítka pre všeobecné použitie a resetovacie tlačitko mikrokontroléra.

```{code-cell} ipython3  
:tags: ["remove-cell"]
from src.utils import *

data = r'''
cct_init
log_init

l=elen_

include(lib_base.ckt)
include(lib_stm32.ckt)
include(lib_user.ckt)

#-----------------------------------------------------------------------
# single_button_h(d, ON | OFF) - horizontalne tlacitko
#-----------------------------------------------------------------------
define(`single_button_h',`[

    B: box ht 1 wid $1 invis;            # neviditelny  box
    rr = 0.15;
    p = 1.5; 

    C1: circle diameter rr at  B.c + (rr/2 - p/4, 0); #  fill 0;
    C2: circle diameter rr at  B.c + (-rr/2 + p/4, 0); # fill 0;
    line from C1.w to B.w
    line from C2.e to B.e
    ifinstr($2,OFF,
        {
            line from C1.c + (-0.05, p/8) to C2.c + (0.05, p/8);
            Q: 0.5 between C1.c+(0, p/8) and C2.c+(0, p/8);
            box wid 0.2 ht 0.08 at  Q+(0, 0.08/2) fill 0;
        },
        {
            line from C1.c + (-0.05, rr/2) to C2.c + (0.05, rr/2);
            Q: 0.5 between C1.c+(0, rr/2) and C2.c+(0, rr/2);
            box wid 0.2 ht 0.08 at  Q+(0, 0.08/2) fill 0; 
        }
    );
]')

command"\sf"
    right_;
S1: single_button_h(1.5, OFF); 
    {"S1" at S1.s above;} 
    line right_ 0.5; D1: dot; {line right_ 3; T1: tbox(\sf A1, 1.5); }
R1: resistor(up_ 1.5, E); rlabel(,\sf 10k,);  

S2: single_button_h(1.5, OFF) at S1+(0, -1.2);  "S2" at S2.s above; 
    line from S2.e to  (R1.start, S2.e) + (1,0); dot; {line right_ to (T1.w, Here); T2: tbox(\sf A2, 1.5); }
    line to (Here, R1.start);
R2: resistor(up_ 1.5, E); rlabel(,\sf 10k,);
DT: dot;

S3: single_button_h(1.5, OFF) at S2+(0, -1.2); {"S3" at S3.s above; }
    line from S3.e to  (R2.start, S3.e) + (1,0); dot; {line right_ to (T1.w, Here); T3: tbox(\sf A3, 1.5); }
    line to (Here, R1.start); 
    R3: resistor(up_ 1.5, E); rlabel(,\sf 10k,);
    
    line from DT to R1.end;
    line from DT to R3.end;
    H1: Header(2,1,,,) with .P1 at DT;{ "J2" at H1.e ljust;}
    power(0.5, +5V)

    right_;
RR: single_button_h(1.5, OFF) at S3+(0, -1.2); {"RESET" at RR.s above; }
    {line right_ to (T1.w, Here); T4: tbox(\sf RESET,1.5); }

    line from S1.w left_ 0.25;
    line to (Here, S2.w); dot; {line to S2.w; }
    line to (Here, S3.w); dot; {line to S3.w; }
    line to (Here, RR.w); dot; {line to RR.w; }
    line down_ 0.5;
    gnd();
'''

_ = cm_compile('img_0505z', data,  dpi=600)   
```

```{figure} ./src/img_0505z.png
:width: 300px
:name: img_0505z

Zapojenie tlačítok na module Funduino.
```




### <font color='#E37434'> Bzučiak </font>

Obvody pasívneho bzučiaka sú pripojené k pinu D3. Pre spustenie potrebuje bzučiak signál 1kHz, ktorý je generovaný časovačom TIM2 na kanáli CH2 v móde PWM.

```{code-cell} ipython3  
:tags: ["remove-cell"]
from src.utils import *

data = r'''
include(lib_base.ckt)
include(lib_stm32.ckt)
include(lib_user.ckt)

command"\sf"

#DT1: dot; {up_; power(1, +5V);}

Q1:bjt_PNP(1,1,R);  #{right_ ; move to Q1.E; power(1, +5V) at Q1.E ;}
# line from Q1.E up_ 1; 
move to Q1.E; line up_ 0.25; power(0.5, +5V)
resistor(left_ 1.5 from Q1.B, E);  {rlabel(,\sf 10k,);}; tbox(\sf D3,1,,<)
line from Q1.C down 0.5 then right_ 0.25;
BB: buzzer(,,C) with .In1 at last line.end; "LS1"  at BB.ne above;
line from BB.In3 left 0.25 then down_ 0.25;
gnd();
'''

_ = cm_compile('img_0505v', data,  dpi=600)   
```

```{figure} ./src/img_0505v.png
:width: 250px
:name: img_0505v

Zapojenie bzuciaka na module Funduino.
```



| Funduino  | Arduino | NUCLEO-64 |
| :---: | :----: | :----: |
| LS1-3   | D3      | PB3     |


```{dropdown} <font color='#84B179'> Príklad spustenia a zastavenia bzučiaka </font>
    import pyb
    from time import sleep

    t1 = pyb.Timer(2, freq=1000)
    
    # spistenie bzuciaka
    ch2 = t1.channel(2, pyb.Timer.PWM, pin=pyb.Pin.board.PB3, pulse_width_percent=25)
    sleep(0.5)
    
    # zastavenie bzuciaka
    t1.deinit()
```

### <font color='#E37434'> LED Display </font>
    
4-znakový LED display je riadený dvoma 8-bitovými posuvnými registrami [74HC595](./doc/sn74hc595.pdf) pripojenými k SPI rozhraniu. Obvod obsahuje 8-bitový posuvný register typu *serial-in / paralell-out* a 8-bitový pamätový redister tvorený D-klopnými obvodmi. Vnútorná štruktúra obvodu je zobrazená na obrázku

```{figure} ./img/ic_74hc595.png
:width: 450px
:name: mp_0505c

Vnútorná štruktúra obvodu [74HC595](./doc/sn74hc595.pdf).
```

Výstupy prvého posuvného registra sú pripojené k anódam znakov, výstupy druhého ku katódam segmentov. Pre rozsvietenie jedného znaku potrebujeme do posuvných registrov vyslať postupnosť 2x 8bitov, ktoré sa zapíšu do posuvných registrov.


    pin = Pin('PB1', Pin.OUT)
    spi = SPI(2, SPI.CONTROLLER, baudrate=100000, polarity=0, phase=0, crc=None)

    pin.value(False)         # povolenie zapisu do registrov
    spi.send(0xC0)           # kod znaku, vyber segmentov duspleja  
    spi.send(oxF1)           # vyber segmentovky
    pin.value(True)          # ukoncenie zapisu a preun hodnoy do pamete registra

:::{admonition} Poznámka
Sériové rozhranie SPI(2) nie je na module NUCLEO-64 mapované na piny, ktoré vyžaduje modul Funduino, je preto potrebné prepojiť piny na vonkajšom konektore modulu NUCLEO-64 podľa nasledujúceho obrázku:

```{figure} ./img/fund_spi2.png
:width: 250px
:name: mp_0505e

Prepojenie pinov (26-21, 30-23, 24-29) pre rozhranie SPI.
```
:::
    


:::{dropdown} <font color='#84B179'> Príklad rozsvietenie jedneho znaku displeja </font>

```{code-block} python
from pyb import SPI, Pin, Timer
import time

# kodova tabulka segmentov pre zobrazenie cislic
#              0    1    2    3    4    5    6    7    8    9
num_code = [0xC0,0xF9,0xA4,0xB0,0x99,0x92,0x82,0xF8,0x80,0x90]

# kodova tabulka pozicie znakov 
#              0    1    2    3
num_pos  = [0xF1,0xF2,0xF4,0xF8]

pin = Pin('PB1', Pin.OUT)
spi = SPI(2, SPI.CONTROLLER, baudrate=100000, polarity=0, phase=0, crc=None)

pin.value(False)
spi.send(num_code[3])    # kod znaku  
spi.send(num_pos[2])     # poloha na displeji
pin.value(True)
```

:::


:::{dropdown} <font color='#84B179'> Príklad zobrazenia dát na displeja v programovej slučke</font>

Pomocou cyklu *for ...* rozsvietime postupne všetky segmenty displeja, programová slučka je ale blokujúca pre iné aktivity.

```{code-block} python
from pyb import SPI, Pin, Timer
import time

# kodova tabulka segmentov
num_code = [0xC0,0xF9,0xA4,0xB0,0x99,0x92,0x82,0xF8,0x80,0x90]

# kodova tabulka znakov 
num_pos  = [0xF1,0xF2,0xF4,0xF8]

# obsah displeja
num_disp = [4,3,7,9]

# chip select
pin = Pin('PB1', Pin.OUT)
spi = SPI(2, SPI.CONTROLLER, baudrate=100000, polarity=0, phase=0, crc=None)

for j in range(4000):
    for i in range(4):
        pin.value(False)
        spi.send(num_code[num_disp[i]])    # kod znaku  
        spi.send(num_pos[i])     # poloha na displeji
        pin.value(True)
```
:::


:::{dropdown} <font color='#84B179'> Príklad zobrazenia dát na displeja pomocou prerušenia časovača </font>

Cyklus obnovenia stavu displeja je riadený prerušením od časovača. Pri vyvolaní prerušenia je volaná funkcia *update_display()*, ktorá zobrazí znaky z poľa *num_disp[]*, hodnoty v tomto poli je možné počas behu programu meniť.

```{code-block} python
from pyb import SPI, Pin, Timer
import time

def update_display(timer):
    for j in range(16):
        for i in range(4):
            c = num_disp[i]
            pin.value(False)
            spi.send(num_code[c])
            spi.send(num_pos[i])
            pin.value(True)
            
        # zhasnutie poslednej cislice v pauze, aby vsetky svietli rovnako
        pin.value(False) 
        spi.send(0xFF)
        spi.send(0xF8)
        pin.value(True)


def display_int(x):
    # zobrazenie cisla 0...9999
    if x in range(0, 10000):
        global num_disp
        a = int(x/1000)
        b = int( (x-a*1000) / 100 )
        c = int( (x-a*1000-b*100)/10)
        d = int( (x-a*1000-b*100 - c*10))
        num_disp=[a,b,c,d]


num_code = [0xC0,0xF9,0xA4,0xB0,0x99,0x92,0x82,0xF8,0x80,0x90]
num_pos  = [0xF1,0xF2,0xF4,0xF8]
num_disp = [1,2,3,4]

# chip select
pin = Pin('PB1', Pin.OUT)
spi = SPI(2, SPI.CONTROLLER, baudrate=100000, polarity=0, phase=0, crc=None)
tim = Timer(4) 

tim.init(freq = 50)
pin.value(True)

# dynamicka obnova stavu displeja v preruseni casovaca 
tim.callback(update_display)

```
:::





    
