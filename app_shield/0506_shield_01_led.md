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

# <font color='#4B9DA9'> LED, Tlačitka a Bzučiak  </font>

##  <font color='#547792'> LED diódy </font>

Na module sú zapojené 3 LED diódy, ich anódy sú pripojené cez rezistor 1k k napájaciemu napätiu +5V. Katódy sú pripojené k pinom mikrokontroléra, dióda sa rozsvieti pri stave piny LOW. 

```{code-cell} ipython3  
:tags: ["remove-cell"]
import sys
sys.path.append('../')
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
line down_ 0.25 then right_ 1; T1: tbox(\sf D13,1,);

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

_ = cm_compile('img_0505w', data,  dpi=600, path='../src')   
```

```{figure} ../src/img_0505w.png
:width: 350px
:name: img_0505w

Zapojenie LED diód.
```


| LED   | Arduino  | Nucleo-64 |
| :---: | :----:   | :----:    |
| D1    | D13      | PA5       |
| D2    | D12      | PA6       |
| D3    | D11      | PA7       |
| D4    | D10      | PB5       |


```{admonition} Poznámka
K pinu PA5 je doske Nucleo-64 pripojená zelená LED, ktorá ovlyvňuje stav LED D1. Na module Nucleo-64 je možné ju odpojiť zrušením prepojky [SB21](../dev_utils/doc/nucleo_64.pdf). 
```
### <font color='#E37434'> Programovanie </font>
    
```{dropdown} <font color='#84B179'> Príklad riadenia LED </font>

Program rozsvietenia a postupného zhasnutia LED
    
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

##  <font color='#547792'> Tlačítka </font>

Na module sa nachádzajú tri tlačítka A1..A3 pre všeobecné použitie a resetovacie tlačitko mikrokontroléra.

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

_ = cm_compile('img_0505z', data,  dpi=600, path='../src')   
```

```{figure} ../src/img_0505z.png
:width: 300px
:name: img_0505z

Zapojenie tlačítok.
```

| Tlačítko | Arduino  | Nucleo-64
| :---     | :--      | :--        
| S1       | A1       | PA1          
| S2       | A2       | PA4          
| S3       | A3       | PB0       

### <font color='#E37434'> Programovanie </font>

````{dropdown} <font color='#84B179'> Príklad vyvolania prerušenia tlačitkami </font>

```{code-block} ipython3  
from pyb import Pin
s1 = Pin('A1', Pin.IN)
s2 = Pin('A2', Pin.IN)
s3 = Pin('A3', Pin.IN)

s1.irq(lambda p:print('S1', s1.value()))
s2.irq(lambda p:print('S2', s2.value()))
s3.irq(lambda p:print('S3', s3.value()))
```
````


##  <font color='#547792'> Bzučiak </font>

Bzučiaka je pripojené k pinu D3 pomocou spínacieho tranzistora.

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

_ = cm_compile('img_0505v', data,  dpi=600, path='../src')   
```

```{figure} ../src/img_0505v.png
:width: 250px
:name: img_0505v

Zapojenie bzuciaka.
```



| Bzučiak | Arduino | NUCLEO-64 |
| :---: | :----: | :----: |
| LS1-3   | D3      | PB3     |


### <font color='#E37434'> Programovanie </font>

````{dropdown} <font color='#84B179'> Príklad spustenia a zastavenia bzučiaka </font>

```{code-block} ipython3  
import pyb
from time import sleep

b=Pin('D3', Pin.OUT_OD)

# spistenie bzuciaka
b.on()
sleep(0.5)

# zastavenie bzuciaka
b.off()
```

````
