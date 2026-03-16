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


# LED / Tlačítko 

Na module Nucleo-64 sa nachádzajú dve periférie, LED dióda a tlačitko. Obe sú pripojené priamo k pinom mikrokontroléra podľa zapojenia na {numref}`img_0105a`.

```{code-cell} ipython3  
:tags: ["remove-cell"]
from src.utils import *

data = r'''
include(lib_base.ckt)
include(lib_stm32.ckt)
include(lib_user.ckt)

Origin: Here 
up_
    move to (2,0)
    gnd;
SW: single_switch(2, OFF, V, L);
    dot; {line -> right 2; "\sf PC13" at last line .end ljust}
    resistor(1.5, ,E);
    power(0.5,$\sf V_{dd}$)
    "\sf Blue Button" at SW.e ljust
    
move to (6,0);
gnd;
DD: diode(2,,R); { em_arrows(,-45, .35) at DD.center +(.3,-.3); }
    resistor(right_ 1.5, ,E); llabel(,\sf 510,);
    line -> right 0.5; "\sf PA5 (D13)" at last line .end ljust
    
    #power(0.5,$\sf V_{dd}$)
    "\sf Green LED" at DD.center + (.5,0) ljust 
'''

_ = cm_compile('img_0100a', data,  dpi=600)   
```

```{figure} ./src/img_0100a.png
:width: 400px
:name: img_0105a

Zapojenie tlačítka a LED diódy na module *Nucleo-64*
```

## LED

```Python
from pyb import Pin
p = Pin('D13', Pin.OUT)
p.value(True)
p.value(False) 
```

## Tlačítko

Nestlačené tlačítko vráti hodnotu 1, stlačené 0.

```Python
from pyb import Pin
p = Pin('PC13', Pin.IN)

# tlac hodnoty tlacitka 0/1
print(p.value())  

# definovanie prerusenia a callback funkcie
p.irq(lambda p:print(p.value()))
```





