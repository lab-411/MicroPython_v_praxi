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



# <font color='#4B9DA9'> Vlastnosti </font>


**SPI** (Serial Peripheral Interface) je synchrónne sériové rozhranie používané na komunikáciu na krátke vzdialenosti medzi procesorom a periférnymi obvodmi (prevodníky, pamäte, displeje). Vyvinuté bolo na prelome 70. a 80. rokov 20. storočia spoločnosťou Motorola a umožňuje obojsmernú *full-duplex* komunikáciu na spoločnej zbernici. Podrobný popis rozhrania *SPI* je uvedený v [dokumentácii](./doc/an_1248.pdf)

Zariadenia na zbernici:

* **Master**

  * riadi časovanie prenášaných dát generovaním hodinového signálu SCLK (System Clock)
  * určuje, s ktorým zariadením bude komunikácia prebiehať pomocou signálu SS (Slave Select) 
  * vysiela dáta pomocou signálu MOSI (Master Out Slave In)
  * prijíma dáta pomocou signálu MISO (Master In Slave Out)

* **Slave**

  * ak je aktivovaný pomocou signálu SS, potom prijíma alebo vysiela dáta synchronizované na signál SCLK
  
  
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

_ = cm_compile('img_0250b', data,  dpi=600)   
```

```{figure} ./src/img_0250b.png
:width: 400px
:name: img_0255b

Základné zapojenie zariadení na zbernici *SPI* (Multi-subnode).
```

V niektorých prípadoch môžu byť zariadenia zapojené v konfigurácii reťazového zapojenia (*daisy chain*), kde je výstup predchádzajúceho *Slave* zariadenia pripojený na vstup nasledujúceho *Slave* zariadenia. Výstup posledného *Slave* zariadenia je pripojený nazad k *Master* zariadeniu. Posuvné registre jednotlivých zariadení takto tvoria jeden veľký posuvný register, v ktorom sa dáta posúvajú medzi jednotlivými zariadeniami. Táto konfigurácia vyžaduje len jeden signál SS a nie samostatné signály pre každé *Slave* zariadenie.

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

_ = cm_compile('img_0250c', data,  dpi=600)   
```

```{figure} ./src/img_0250c.png
:width: 400px
:name: img_0255c

Reťazenie zariadení na zbernici *SPI* (Daisy-Chain).
```

Komunikácia a spracovanie dát pomocou posuvných registrov pre riadenie LED displeja je popísaná v kapitole [Modul Funduino](0505_funduino_01).
  
## <font color='#547792'>  Časovanie zbernice </font>

Konfigurácii parametrov zbernice je určená parametrami

* CPOL - polarita hodinového signálu
  * CPOL=0 aktívna úroveň signálu je H
  * CPOL=1 aktívna úroveň signálu je L

* CPHA - určuje okamžik zmeny hodnoty dát pri vysielaní
  * CPHA=0 signál mení hodnotu pri zostupnej hrane a číta sa pri nábežnej hrane hodinového signálu
  * CPHA=1 signál mení hodnotu pri nábežnej hrane a číta sa pri zostupnej hrane hodinového signálu
 

```{figure} ./img/SPI_timing.png
:width: 650px
:name: img_0250a

Základné módy časovania zbernice SPI.
```


```{figure} ./img/spi_daisy.png
:width: 350px
:name: img_0250d

Časovanie SPI zbernice v móde daisy-chain.
```
