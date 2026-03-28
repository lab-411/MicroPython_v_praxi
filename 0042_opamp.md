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



# <font color='#4B9DA9'> Operačný zosilovač </font>

Operačný zosilovač je univerzálne elektronické zariadenie, v súčasnej dobe v podobe integrovaného obvodu, ktoré je určené na elektronickú realizáciu matematických operácií (preto názov *operačný*) ako je sčítanie, odčítanie, integráciu, deriváciu, logaritmovanie, zosilnenie. V minulosti bola jeho hlavná oblasť použitia riešenie diferenciálnych rovníc, v súčasnosti sa používa aj na spracovanie a úpravu signálov zo senzorov alebo ako súčasť regulačných obvodov. Je to najuniverzálnejší obvod elektroniky, ktorý sa vyrába v množstve typov a modifikácií pre rôzne oblasti použitia.

```{code-cell} ipython3  
:tags: ["remove-cell"]
from src.utils import *

data = r'''
include(lib_base.ckt)
include(lib_stm32.ckt)
include(lib_user.ckt)
include(lib_color.ckt)

A1: opamp(); 
    line from A1.In1 left_ 0.5; 
    line from A1.In2 left_ 0.5;
    "a)" at A1.s below;

    move to A1 +(3.5,0);
    right_;
A2: opamp(,,,,P); 
    line from A2.In1 left_ 0.5;  
    color_blue; line <- left_ 0.8 up_ 0.8; "Invertujúci vstup" above; color_black; 

    line from A2.In2 left_ 0.5;
    color_blue; line <- left_ 0.8 down_ 0.8; "Neinvertujúci vstup" below; color_black; 
    color_blue; 
    line <- from A2.Out right_ 0.8 up_ 0.8; "Výstup" above; color_black; 
    line from A2.V1 up_ 0.25; color_red; line <- right_ 0.8 up_ 0.8; "Napájanie +" above; color_black; 
    line from A2.V2 down_ 0.25; color_red; line <- right_ 0.8 down_ 0.8; "Napájanie -" below;
    color_black; 
    "b)" at A2.se below;
'''

_ = cm_compile('img_0080a', data,  dpi=600)   
```

```{figure} ./src/img_0080a.png
:width: 400px
:name: img_0076s

Značka operačného zosilovača, a) ideálny, b) s označenými vývodmi.
```

##  <font color='#547792'> Vlastnosti </font>


Ideálny operačný zosilovač má dva vstupy, invertujúci (-) a neinvertujúci (+) a jeden výstup. K operačnému zosilovaču sú pripojené ďašie elektronické komponenty, ktoré určujú vlastnosti obvodu. Vlastnosti samotného ideálneho operačného zosilovača môžeme popísať v niekoľkých bodoch:

1. Zosilovač na výstupe zosilňuje rozdiel medzi napätiami na vstupoch $U_+ - U_-$, ak je rozdiel kladný, výstup bude mať kladnú hodnotu a naopak.
2. Zosilnenie $A$ operačného zosilovača je veľmi veľké, teoreticky nekonečné.
3. Do vstupov operačného zosilovača netečie žiaden prúd, vstupný odpor je nekonečný.
4. Výstup operačného zosilovača môžeme zaťažiť ľubovolne malou záťažou, jeho výstupný odpor je nulový.

Pre operačný zosilovač zapojený do obvodu zároveň platí:

5. Operačný zosilovač v lineárnom režime nastavuje napätie na výstupe tak, aby rozdiel napätí medzi vstupmi bol **nulový**.


### <font color='#E37434'> Sledovač </font>


```{code-cell} ipython3  
:tags: ["remove-cell"]
from src.utils import *

data = r'''
include(lib_base.ckt)
include(lib_stm32.ckt)
include(lib_user.ckt)
include(lib_color.ckt)

A1: opamp(); 
LN: line from A1.In1 left_ 0.5; 
LP: line from A1.In2 left_ 0.5;

line from LN.end up_ 0.8 
line right_ to (A1.Out, Here) then to A1.Out; dot; 
line right_ 1; 
C1: circle rad 0.075; "\textit{Out}" at C1.n above;

line from LP.end left_ 0.75;
C2: circle rad 0.075; "\textit{In}" at C2.n above;
'''

_ = cm_compile('img_0080b', data,  dpi=600)   
```

```{figure} ./src/img_0080b.png
:width: 250px
:name: img_0080b

Sledovač
```

### <font color='#E37434'> Invertujúci zosilovač </font>


```{code-cell} ipython3  
:tags: ["remove-cell"]
from src.utils import *

data = r'''
include(lib_base.ckt)
include(lib_stm32.ckt)
include(lib_user.ckt)
include(lib_color.ckt)

OP: opamp()
    line from OP.In1 left 0.5;
DN: dot;
    resistor(2,,E); llabel(,R_1,);
    circle rad 0.1; "\textit{In}" at last circle.n above;

    line from DN up_ 1;
    resistor(right_ 2.5,,E); llabel(,R_2,);
    line down_ (Here.y - OP.Out.y);
DO: dot;
    { line to OP.Out; }
    line right_ 1;
    circle rad 0.1; "\textit{Out}" at last circle.n above;

    line from OP.In2 left_ 0.5 then down_ 0.5; gnd; 
'''

_ = cm_compile('img_0080c', data,  dpi=600)   
```

```{figure} ./src/img_0080c.png
:width: 300px
:name: img_0080c

Invertujúci zosilovač
```

$$
K = -\dfrac{R_2}{R_1}
$$

### <font color='#E37434'> Neinvertujúci zosilovač </font>


```{code-cell} ipython3  
:tags: ["remove-cell"]
from src.utils import *

data = r'''
include(lib_base.ckt)
include(lib_stm32.ckt)
include(lib_user.ckt)
include(lib_color.ckt)

right_;
PP: opamp(,,,,R)
    line from PP.In1 left_ 1.5;
    circle rad 0.1; "\textit{In}" at last circle.n above;
    line from PP.In2 left_ 0.5 then down_ 0.75;
    dot;
    {resistor(down_ 1.5,,E); rlabel(,R_1,); gnd;}
    resistor(right_ 2.5,,E); llabel(,R_2,);
    line up_ -(Here.y - PP.Out.y);
    dot;
    { line to PP.Out; }
    line right_ 1;
    circle rad 0.1; "\textit{Out}" at last circle.n above;
'''

_ = cm_compile('img_0080d', data,  dpi=600)   
```

```{figure} ./src/img_0080d.png
:width: 300px
:name: img_0080d

Neinvertujúci zosilovač
```

$$
K =1 + \dfrac{R_2}{R_1}
$$

