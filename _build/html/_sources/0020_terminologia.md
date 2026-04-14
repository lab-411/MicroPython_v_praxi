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


# <font color='#4B9DA9'> Terminológia</font>

##  <font color='#547792'> Použité symboly </font>

| Symbol | Význam | 
| :--- | :---- | 
| $U$, $I$    | Konštantná alebo stredná hodnota napätia a prúdu      | 
| $u$, $i$    | Okamžitá hodnota napätia a prúdu      | 
| $R_1$, $C_1$ ...    | Referencie na komponenty     | 
| $1k5$, $22nF$ ...    | Hodnoty komponentov     | 


##  <font color='#547792'> Značky elektronických prvkov </font>


```{code-cell} ipython3  
:tags: ["remove-cell"]
from src.utils import *

data = r'''
include(lib_base.ckt)
include(lib_stm32.ckt)
include(lib_user.ckt)
command"\sf"

d=-1;
x=0.5; y=1
    move to (x,y);
    resistor(right_ 1.5,E); "Rezistor" ljust;
    move to (x, y+d);
    
    capacitor(right_ 1.5,); "Kondenzátor" ljust; 
    move to (x, y+2*d);
    
    capacitor(1.5,K+,,0.55, 0.18); "Kondenzátor polarizovaný" ljust; 
    move to (x, y+3*d);
    inductor(1.5,L,4); "Cievka" ljust;
    
    move to (x, y+4*d);
    L1:[Q: inductor(1.5,L,4); linethick_(2); 
    line dimen_*0.55 at Q.c + (0,0.25);];  "Cievka s jadrom" ljust;
    
    move to (x+0.35, y+5.2*d);
TR:[Q:transformer(down_ 1.5,L,4,W,4); {"Transformátor" at Here + (0.3,0) ljust; }
     line from Q.S1 to (Q.S1,Q.P1);         
     line from Q.S2 to (Q.S2,Q.P2)]; 
     #"$\sf L_1$" at TR.w rjust; "$\sf L_2$" at TR.e ljust;


d=-1;
x=6.5; y=1
    move to (x,y);
    diode(1.5); "Dióda" ljust;
    
    move to (x,y+1*d);
    bjt_NPN(1,1,L); "NPN Tranzistor" ljust;
    
    move to (x,y+2.25*d);
    bjt_PNP(1,1,L); "PNP Tranzistor" ljust;

    move to (x,y+3.5*d);
    e_fet(up_ ,,P,);  "MOSFET Tranzistor" at Here+(0.2,0) ljust;

    move to (x,y+4.7*d);
    right_; 
A2: opamp(1.3,,,0.9,R); "Operačný zosilovač" at Here+(0.1,0) ljust;
'''

_ = cm_compile('img_0020a', data,  dpi=600)   
```


```{figure} ./src/img_0020a.png
:width: 600px
:name: img_0020a
```




%```{subfigure} AB
%:layout-sm: A|B
%:subcaptions: below
%:name: myfigure
%:gap: 16px
%:width: 600px
%
%![Pasívne prvky](/src/img_0020a.png)
%![Aktívne prvky](/src/img_0020b.png)
%
%Značky prvkov elektrických zapojení.
%```


##  <font color='#547792'> Násobky jednotiek </font>

| Skratka | Meno | Hodnota   | Názov   | 
| :--- | :----  |  :----    | :----    | 
| G    | giga   |    $10^9$ | miliarda |
| M    | mega   |   $10^6$  |   milión |
| k    | kilo   |   $10^3$  |   tisíc  |
| h    | hekto  |   $10^2$  |   sto    |
| da    | deka  |   $10^1$  |   desať  |




