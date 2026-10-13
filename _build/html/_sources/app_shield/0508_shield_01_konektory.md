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

# <font color='#4B9DA9'> Konektory </font>

##  <font color='#547792'> Popis </font>

Na module sa nachádzajú konektory pre pripojenie periférií

* U4 - konektory pre pripojenie senzorov 
* U5 - konektory pre pripojenie senzorov 
* A6 - konektory s vyvedeným napájaním
* J6 - konektor pri pripojenie rozširujúcich modulov

```{figure} ./img/multi_shield_10_konektor.png
:width: 390px
:name: mp_0508a

Konektory na module.
```

##  <font color='#547792'> Zapojenie </font>


```{code-cell} ipython3  
:tags: ["remove-cell"]
import sys
sys.path.append('../')
from src.utils import *

data = r'''
include(lib_base.ckt)
include(lib_stm32.ckt)
include(lib_user.ckt)

cct_init
log_init
command "\sf"

move to (4.25,2.5);

down_;
T1: tstrip(R,3,DU); {"1" at T1.w rjust;}; 
T2: tstrip(R,3,DU); 
T3: tstrip(R,3,DU); 
T4: tstrip(R,3,DU); {"1" at T4.w rjust;}; 

line from T4.T1 up_ 2.75; circle rad 0.1; "+5V" above;
line from T4.T2 up_ 2.75 then right_ 0.5; down_; gnd; 
line from T1.T3 right_ 1;  tbox(\sf D5); 
line from T2.T3 right_ 1;  tbox(\sf D6); 
line from T3.T3 right_ 1;  tbox(\sf D9); 
line from T4.T3 right_ 1;  tbox(\sf A5); 
    "A6" at (T2.w + T3.w)/2 rjust; 
   
   
move to (4.25,5.25);
U4: tstrip(R,3,DU); {"1" at U4.w rjust;};
    line from U4.T1 down 0.75 then left 0.5;  tbox(\sf D5,,, <);
    line from U4.T2 down_ 0.75; gnd();
    line from U4.T3 down 0.75 then right_ 0.5; circle rad 0.1; "+5V" ljust;
    "U4" at U4.n above;
    
move to (7.5,5.25);
U5: tstrip(R,3,DU); {"1" at U5.w rjust;};
    line from U5.T1 down_ 0.75; gnd();
    line from U5.T2 down_ 1.5; dot(); {line down_ 0.5 then left_ 0.5; tbox(\sf A4,,, >); } 
    right_; resistor(,E); rlabel(,\sf 10k,);
    H1: Header(2,1,,,);{ "J1" at H1.n above;}; circle rad 0.1; "+5V" ljust;

    
    line from U5.T3 down 0.75 then right_ 0.5; circle rad 0.1; "+5V" ljust;
    "U5" at U5.n above;
 
       
    move to (0.5, 2.5);   
B1: tstrip(U,7,DU);
    line from B1.T1 right 1 then down 0.5; gnd();
    line from B1.T2 right 1; circle rad 0.1; "+5V" ljust;
    line from B1.T3 right 0.5;
    line from B1.T4 right 1; tbox(\sf D1,,0.38, >); 
    line from B1.T5 right 1; tbox(\sf D0,,0.38, >); 
    line from B1.T6 right 0.5;
    line from B1.T7 right 0.5;
    "J6" at B1.n above;
'''

_ = cm_compile('img_0508a', data,  dpi=600, path='../src')   
```

```{figure} ../src/img_0508a.png
:width: 600px
:name: img_0508a

Zapojenie konektorov modulu.
```


| U4    | Arduino  | Nucleo-64 |
| :---: | :----:   | :----:    |
| 1     | D5       | PB4       |
| 2     | GND      | GND       |
| 3     | +5V      | +5V       |


| U5    | Arduino  | Nucleo-64 |
| :---: | :----:   | :----:    |
| 1     | GND      | GND       |
| 2     | A4       | PC1       |
| 3     | +5V      | +5V       |


| A6    | Arduino  | Nucleo-64 |
| :---: | :----:   | :----:    |
| 1     | GND      | GND       |
| 2     | +5V      | +5V       |
| 3     | D5       | PB4       |
| 3     | D6       | PB10      |
| 3     | D9       | PC7       |
| 3     | A5       | PC0       |


| J6    | Arduino  | Nucleo-64 |
| :---: | :----:   | :----:    |
| 1     | GND      | GND       |
| 2     | +5V      | +5V       |
| 3     | NC       | NC        |
| 4     | D1       | PA2       |
| 5     | D0       | PA3       |
| 6     | NC       | NC        |
| 7     | NC       | NC        |

    
