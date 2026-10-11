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



# <font color='#4B9DA9'> Zbernica SPI </font>

##  <font color='#547792'> Popis </font>

**SPI** (Serial Peripheral Interface) je synchrónne sériové rozhranie používané na komunikáciu na krátke vzdialenosti medzi procesorom a periférnymi obvodmi (prevodníky, pamäte, displeje). Vyvinuté bolo na prelome 70. a 80. rokov 20. storočia spoločnosťou Motorola a umožňuje obojsmernú *full-duplex* komunikáciu na spoločnej zbernici. Podrobný popis rozhrania *SPI* je uvedený v [dokumentácii](./doc/an_1248.pdf). Výhodou zbernice SPI je možnosť použitia jednoduchých [posuvných registrov](./doc/sn74hc595.pdf) ak periférnych zariadení.

Zariadenia na zbernici:

* **Master**

  * riadi časovanie prenášaných dát generovaním hodinového signálu SCLK (System Clock)
  * určuje, s ktorým zariadením bude komunikácia prebiehať pomocou signálu SS (Slave Select) 
  * vysiela dáta pomocou signálu MOSI (Master Out Slave In)
  * prijíma dáta pomocou signálu MISO (Master In Slave Out)

* **Slave**

  * ak je aktivovaný pomocou signálu SS, potom prijíma alebo vysiela dáta synchronizované na signál SCLK

### <font color='#E37434'>  Časovanie zbernice </font>

Konfigurácii parametrov zbernice je určená parametrami CPOL (polarita sgnálov) a CPHA (fáza signálov)

* CPOL - polarita hodinového signálu
  * CPOL=0 aktívna úroveň signálu je H
  * CPOL=1 aktívna úroveň signálu je L

* CPHA - určuje okamžik zmeny hodnoty dát pri vysielaní
  * CPHA=0 signál mení hodnotu pri zostupnej hrane a číta sa pri nábežnej hrane hodinového signálu
  * CPHA=1 signál mení hodnotu pri nábežnej hrane a číta sa pri zostupnej hrane hodinového signálu
 

```{figure} ./img/spi_timing.png
:width: 650px
:name: img_0250a

Základné módy časovania zbernice SPI.
```
  
##  <font color='#547792'> Zapojenie </font>

### <font color='#E37434'> Základné zapojenie </font>


```{code-cell} ipython3  
:tags: ["remove-cell"]

import sys
sys.path.append('../')

from src.utils import *

data = r'''
include(lib_base.ckt)
include(lib_stm32.ckt)
include(lib_user.ckt)

log_init

command "\sf"

define(`SPI_Master', `[
  BX: box wid 2.5 ht 5*lg_pinsep;

      lg_pin(BX.ne - (0, 1*lg_pinsep),  SCLK, Pin8, e,,0 );
      lg_pin(BX.ne - (0, 2*lg_pinsep),  MOSI, Pin7, e,,0 );
      lg_pin(BX.ne - (0, 3*lg_pinsep),  MISO, Pin6, e,,0 );
      lg_pin(BX.ne - (0, 4*lg_pinsep),  lg_bartxt(SS), Pin5, e,,0 );
]')

define(`SPI_Slave', `[
  BX: box wid 2 ht 5*lg_pinsep;

      lg_pin(BX.nw - (0, 1*lg_pinsep),  SCLK, Pin1, w,,0);
      lg_pin(BX.nw - (0, 2*lg_pinsep),  MOSI, Pin2, w,, 0);
      lg_pin(BX.nw - (0, 3*lg_pinsep),  MISO, Pin3, w,, 0);
      lg_pin(BX.nw - (0, 4*lg_pinsep),  lg_bartxt(SS), Pin4, w,,0 );
]')

M: SPI_Master(); "SPI" at M.c +(-0.3,0) above; "Master" at M.c +(-0.3,0) below;
   line from M.Pin8 right 2.5;  #DT1: dot invis; 

S1: SPI_Slave() with .Pin1 at last line .end; 
    "SPI" at S1.c +(0.3,0) above; "Slave" at S1.c +(0.3,0) below;
    
    line -> from M.Pin7 to S1.Pin2;
    line <-from M.Pin6 to S1.Pin3;
    line -> from M.Pin5 to S1.Pin4
'''

_ = cm_compile('img_0250e', data,  dpi=600, path='../src')   
```

```{figure} ../src/img_0250e.png
:width: 400px
:name: img_0255x

Základné zapojenie zariadení na zbernici *SPI* (Master-Slave).
```



### <font color='#E37434'> Paralelné zapojenie </font>


```{code-cell} ipython3  
:tags: ["remove-cell"]

from src.utils import *

data = r'''
include(lib_base.ckt)
include(lib_stm32.ckt)
include(lib_user.ckt)

log_init

command "\sf"

define(`SPI_Master', `[
  BX: box wid 2.5 ht 7*lg_pinsep;

      lg_pin(BX.ne - (0, 1*lg_pinsep),  SCLK, Pin8, e,,0 );
      lg_pin(BX.ne - (0, 2*lg_pinsep),  MOSI, Pin7, e,,0 );
      lg_pin(BX.ne - (0, 3*lg_pinsep),  MISO, Pin6, e,,0 );
      lg_pin(BX.ne - (0, 4*lg_pinsep),  lg_bartxt(SS1), Pin5, e,,0 );
      lg_pin(BX.ne - (0, 5*lg_pinsep),  lg_bartxt(SS2), Pin4, e,,0 );
      lg_pin(BX.ne - (0, 6*lg_pinsep),  lg_bartxt(SS3), Pin3, e,,0 );

]')

define(`SPI_Slave', `[
  BX: box wid 2 ht 5*lg_pinsep;

      lg_pin(BX.nw - (0, 1*lg_pinsep),  SCLK, Pin1, w,,0);
      lg_pin(BX.nw - (0, 2*lg_pinsep),  MOSI, Pin2, w,, 0);
      lg_pin(BX.nw - (0, 3*lg_pinsep),  MISO, Pin3, w,, 0);
      lg_pin(BX.nw - (0, 4*lg_pinsep),  lg_bartxt(SS), Pin4, w,,0 );
]')

M: SPI_Master(); "SPI" at M.c +(-0.3,0) above; "Master" at M.c +(-0.3,0) below;
   line from M.Pin8 right 1.5;  DT1: dot; 
   line from M.Pin7 right 1.25; DT2: dot; 
   line <-from M.Pin6 right 1.;   DT3: dot;

   line from DT1-> right 1;
S1: SPI_Slave() with .Pin1 at last line .end; 
    "SPI" at S1.c +(0.3,0) above; "Slave" at S1.c +(0.3,0) below;
    line -> from DT2 to S1.Pin2
    line from DT3 to S1.Pin3
    line -> from M.Pin5 to S1.Pin4

    line from DT1 down_ 2.5; DT5: dot;line -> to (S1.Pin1, Here)
    right_
S2: SPI_Slave() with .Pin1 at last line .end
    "SPI" at S2.c +(0.3,0) above; "Slave" at S2.c +(0.3,0) below;
    line from DT2 to (DT2, S2.Pin2); DT6: dot;line -> to S2.Pin2
    line from DT3 to (DT3, S2.Pin3); DT7: dot;line  to S2.Pin3

    line from DT5 down_ 2.5; ;line -> to (S1.Pin1, Here)
    right_
S3: SPI_Slave() with .Pin1 at last line .end
    "SPI" at S3.c +(0.3,0) above; "Slave" at S3.c +(0.3,0) below;
    line from DT6 to (DT6, S3.Pin2); line -> to S3.Pin2
    line from DT7 to (DT7, S3.Pin3); line  to S3.Pin3

X:  0.3 between M.Pin4 and S2.Pin4;
    line -> from M.Pin4 to (X, M.Pin4) then to (X, S2.Pin4) then to S2.Pin4

Y:  0.2 between M.Pin3 and S3.Pin4;
    line -> from M.Pin3 to (Y, M.Pin3) then to (Y, S3.Pin4) then to S3.Pin4 
'''

_ = cm_compile('img_0250b', data,  dpi=600, path='../src')   
```

```{figure} ../src/img_0250b.png
:width: 400px
:name: img_0255b

Základné zapojenie zariadení na zbernici *SPI* (Multi-subnode).
```

### <font color='#E37434'> Reťazové zapojenie </font>

V niektorých prípadoch môžu byť zariadenia zapojené v konfigurácii reťazového zapojenia (*daisy chain*), kde je výstup predchádzajúceho *Slave* zariadenia pripojený na vstup nasledujúceho *Slave* zariadenia. Výstup posledného *Slave* zariadenia je pripojený nazad k *Master* zariadeniu. Posuvné registre jednotlivých zariadení takto tvoria jeden veľký posuvný register, v ktorom sa dáta posúvajú medzi jednotlivými zariadeniami. Táto konfigurácia vyžaduje len jeden signál SS.

```{code-cell} ipython3  
:tags: ["remove-cell"]
from src.utils import *

data = r'''
include(lib_base.ckt)
include(lib_stm32.ckt)
include(lib_user.ckt)
include(lib_color.ckt)

log_init

command "\sf"

define(`SPI_Master', `[
  BX: box wid 2.5 ht 5*lg_pinsep;

      lg_pin(BX.ne - (0, 1*lg_pinsep),  SCLK, PinCLK, e,,0 );
      lg_pin(BX.ne - (0, 2*lg_pinsep),  MOSI, PinMOSI, e,,0 );
      lg_pin(BX.ne - (0, 3*lg_pinsep),  MISO, PinMISO, e,,0 );
      lg_pin(BX.ne - (0, 4*lg_pinsep),  lg_bartxt(SS), PinSS, e,,0 );
]')

define(`SPI_Slave', `[
  BX: box wid 2 ht 5*lg_pinsep;

      lg_pin(BX.nw - (0, 1*lg_pinsep),  SCLK, PinCLK, w,,0);
      lg_pin(BX.nw - (0, 2*lg_pinsep),  MOSI, PinMOSI, w,, 0);
      lg_pin(BX.nw - (0, 3*lg_pinsep),  MISO, PinMISO, w,, 0);
      lg_pin(BX.nw - (0, 4*lg_pinsep),  lg_bartxt(SS), PinSS, w,,0 );
]')

M:  SPI_Master(); "SPI" at M.c +(-0.3,0) above; "Master" at M.c +(-0.3,0) below;
    line from M.PinCLK right 0.8;  DT1: dot; 

    line from DT1-> right 1.5;
S1:SPI_Slave() with .PinCLK at last line .end; 
    "SPI" at S1.c +(0.3,0) above; "Slave" at S1.c +(0.3,0) below;
    
    
    
    line from DT1 down_ 2.5; DT5: dot; line -> to (S1.PinCLK, Here)
    right_
S2: SPI_Slave() with .PinCLK at last line .end
    "SPI" at S2.c +(0.3,0) above; "Slave" at S2.c +(0.3,0) below;

    line from DT5 down_ 2.5; ;line -> to (S1.PinCLK, Here)
    right_
S3: SPI_Slave() with .PinCLK at last line .end
    "SPI" at S3.c +(0.3,0) above; "Slave" at S3.c +(0.3,0) below;

    # select
    color_blue;
    line from M.PinSS right_ 0.45; DS: dot; line -> to S1.PinSS
    line from DS down_ to (DS, S2.PinSS); dot; {line -> to S2.PinSS; }
    line -> down_ to (DS, S3.PinSS) then to S3.PinSS
    
    # chain
    color_red;
    line -> from M.PinMOSI to S1.PinMOSI
    line from S1.PinMISO left_ 0.75; line -> to (Here, S2.PinMOSI) then to S2.PinMOSI;
    line from S2.PinMISO left_ 0.75; line -> to (Here, S3.PinMOSI) then to S3.PinMOSI;
    line from S3.PinMISO left_ 1; line -> to (Here, M.PinMISO) then to M.PinMISO;
'''

_ = cm_compile('img_0250c', data,  dpi=600, path='../src')   
```

```{figure} ../src/img_0250c.png
:width: 400px
:name: img_0255c

Reťazenie zariadení na zbernici *SPI* (Daisy-Chain).
```

##  <font color='#547792'> Programovanie </font>

Knižnica *pyb* obsahuje pre obsluhu sériového rozhrania triedu [SPI](https://docs.micropython.org/en/latest/library/pyb.SPI.html). Signál NSS pre výber periférie **nie** je v knižnici *pyb.SPI* použitý, je potrebné ho ovládať samostatne prostredníctvom triedy *pyb.Pin*. Pripojenie rozhraní SPI k pinom mikrokontroléra je tabuľke:

| Periféria         | Nucleo-64 | Arduino-UNO | Alternatíva
| :---              | :--       | :--         | :--  
| SPI1 NSS          | PA4 - NC  | A2          | PA15 - NC
| SPI1 SCK          | PB3       | D3          | PA5
| SPI1 MISO         | PB4       | D5          | PA6
| SPI1 MOSI         | PB5       | D4          | PA7
| SPI2 NSS          | PB12 - NC |             | PB9 - NC
| SPI2 SCK          | PB13      |             | PB10
| SPI2 MISO         | PB14      |             | PC2
| SPI2 MOSI         | PB15      |             | PC3

```{admonition} Rekonfigurácia pre Arduino

Rozhranie SPI1 na doske NUCLEO-64 nie je štandardne pripojené ku pinom konektora Arduino-UNO.   
Pomocou funkcie alternatívnych pinov možeme pripojenie rozhrania rekonfigurovať.

    p=Pin('PA7')
    p.af_list()
    [Pin.AF1_TIM1, Pin.AF2_TIM3, Pin.AF3_TIM8, Pin.AF5_SPI1, Pin.AF14_TIM17]
    
    # Konfiguracia pre kompatibilitu SPI1 s Arduinom
    p_mosi = Pin('PA7', mode=Pin.ALT, alt=Pin.AF5_SPI1)
    p_miso = Pin('PA6', mode=Pin.ALT, alt=Pin.AF5_SPI1)
    p_sck  = Pin('PA5', mode=Pin.ALT, alt=Pin.AF5_SPI1)
```

### <font color='#E37434'> API </font>

**Konštruktor / deštruktor**

    SPI.init(mode, baudrate=328125, *, prescaler=-1, 
                   polarity=1, phase=0, bits=8, firstbit=SPI.MSB, 
                   ti=False, crc=None)
    SPI.deinit() 

    mode      - typ zariadenia, SPI.CONTROLLER / SPI.PERIPHERAL
    baudrate  - prenosová rýchlosť, hodnoty podporované procesorom
    prescaler - delič hodnoty prenosovej rýchlosti, 1/2/4/8/16/32/64/128/256
    firstbit  - poradie bitov, SPI.LSB / SPI.MSB
    polarity  - hodnota CPOL, 0/1
    phase     - hodnota CPHA, 0/1
    ti        - konvencia TI / Motorola, True / False
    crc       - kontrolná suma


**Metódy**

    SPI.recv(recv, *, timeout=5000)
    SPI.send(send, *, timeout=5000)
    SPI.send_recv(send, recv=None, *, timeout=5000)

    
```{dropdown} <font color='#84B179'> Príklad inicializácie a vyslania 1 Byte </font>

    from pyb import SPI

    # inicializacia
    pin = Pin('PB1', Pin.OUT)
    spi = SPI(2, SPI.CONTROLLER, baudrate=100000, polarity=0, phase=0, crc=None)

    # vyslanie jedneho byte
    pin.value(False)
    spi.send(0x12)
    pin.value(True)
```





