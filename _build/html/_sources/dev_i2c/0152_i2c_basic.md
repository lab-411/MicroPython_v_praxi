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


# <font color='#4B9DA9'> Zbernica I2C </font>

##  <font color='#547792'> Popis </font>

I2C (Inter-Integrated Circuit) rozhranie je dvojvodičové obojsmerné synchrónne sériové periférne rozhranie (zbernica), primárne využívané v rámci vstavaných systémov pre komunikáciu na krátke vzdialenosti medzi riadiacimi mikrokontrolérmi a ostatnými integrovanými obvodmi resp. modulmi (EEPROM, A/D prevodníky, pamäťové karty, displeje, a pod.). Rozhranie bolo patentované firmou Philips v roku 1981 a prvá verzia špecifikácie bola vydaná v roku 1982.

##  <font color='#547792'> Zapojenie </font>

Zbernica umožňuje, v závislosti od pripojených zariadení, komunikáciu prenosovými rýchlosťami od 100 kbps (standard mode) až po 5 Mbps (ultra-fast mode) a zariadenia sú adresované 7-bitovými (27 = 128 adries) prípadne 10-bitovými (210 = 1 024 adries) adresami.



```{code-cell} ipython3  
:tags: ["remove-cell"]

import sys
sys.path.append('../')

from src.utils import *

data = r'''
include(lib_base.ckt)
include(lib_stm32.ckt)
include(lib_user.ckt)
include(lib_color.ckt)

command "\sf";

command "\sf";

    move to (0,2);
    tbox(SDA, 1.5); line 0.5; dot;
    line right_ 1.5; 
    dot; {up_; R1:resistor(2,E); llabel(,4k7,); right_;}
    line 2;
D1: dot; 
    line 3;
D4: dot; 
LD: line 3;

    move to (0,1.5);
    tbox(SCL, 1.5); line 0.5; dot;
    line right_ 2.5; 
    dot; {up_; line 0.5; R2:resistor(2,E); rlabel(,4k7,); right_;}
    line 2;
D2: dot; line 3;
D3: dot; 
LC: line 2;

L1: line from R1.end to R2.end;
    move to L1.c; dot; {up_; tconn(0.75,O); "$\sf Vdd$" at Here above;}

    move to D1; line down_ 1.5;
    move to D2; line down_ 1;
    move to (D1+D2)/2 + (0,-1.25);
    box wid 2 ht 1.5; "SLAVE" at last box.c above; "$\sf \#1$" at last box.c below;

    move to D4; line down_ 1.5;
    move to D3; line down_ 1;
    move to (D3+D4)/2 + (0,-1.25);
    box wid 2 ht 1.5; "SLAVE" at last box.c above; "$\sf \#2$" at last box.c below;

    color_blue();
    line from (0,4) right 2 then down 4.5 then left 2 dashed;
    "STM32" at (1,4) below;
    "MASTER" at (1,4) above;

    color_black();
    line from LD.end right 1 dashed; LX: line 1.5 then down_ 1.5;
    line from LC.end right 1 dashed; LY: line 0.5 then down_ 1;
    move to (LX.end + LY.end)/2 + (0,0);
    box wid 2 ht 1.5; "SLAVE" at last box.c above; "$\sf \#N$" at last box.c below;
'''

_ = cm_compile('img_0152a', data,  dpi=600, path='../src')   
```

```{figure} ../src/img_0152a.png
:width: 600px
:name: img_0152a

Zapojenie zariadení na zbernici *I2C*.
```



### <font color='#E37434'> Časovanie zbernice </font>

```{figure} ./img/i2c_02.png
:width: 550px
:name: img_0201b

Časovanie zbernice *I2C*.
```

##  <font color='#547792'> Programovanie </font>

Knižnica *pyb* obsahuje pre obsluhu sériového rozhrania triedu *I2C*. 

| Periféria         | Nucleo-64 | Arduino-UNO 
| :---              | :--       | :--         
| I2C1 SCL          | PB8       | D18         
| I2C1 SDA          | PB9       | D19         
| I2C2 SCL          | PB10      |            
| I2C2 SDA          | PB11      |            
| I2C3 SCL          | PC0       |             
| I2C3 SDA          | PC1       |            


### <font color='#E37434'> API </font>

**Konštruktor / deštruktor**


    I2C(mode, addr=0x12, baudrate=400000, gencall=False, dma=False)
    I2C.deinit()
    
    mode
      I2C.CONTROLLER 
      I2C.PERIPHERAL
      
    addr      - 7 bitová adresa v móde I2C.PERIPHERAL 
    baudrate  - prenosová rýchlosť
    gencall
    dma       - povolenie DMA prenosu dát
    
**Metódy**

    I2C.is_ready(addr)    - kontrola pripojenia zariadenia s addr
    I2C.scan()            - výpis všetkých zariadení na zbernici
    I2C.send(send, addr=0x00, *, timeout=5000)
    I2C.recv(recv, addr=0x00, *, timeout=5000)
    I2C.mem_read(data, addr, memaddr, *, timeout=5000, addr_size=8)
    I2C.mem_write(data, addr, memaddr, *, timeout=5000, addr_size=8)
    
    
    
    
    


