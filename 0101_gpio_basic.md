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

# Vlastnosti  

Najjednoduchším spôsobom komunikácie procesora mikrokontroléra s okolím je prostredníctvom zápisu alebo čítania binárnej hodnoty na fyzickom vývode púzdra, pine. Skupina pinov je združená do portov, organizácia pinov v portoch závisí od architektúry MCU. Pre procesor sú stavy pinov v portoch mapované do vyhradených pamäťových buniek, registrov, ktoré sú umiestnené na definovaných miestach v pamäti. Širka registrov V STM32 je 16 bitov, každé bit mapuje stav príslušného pinu portu. Podľa veľkost púzdra môže mať mikrokontrolér vyvedených niekoľko portov, pričom na púzdro nemusia byť vyvedené celé porty. 
   
   
Piny portov môžu mať niekoľko funkcií, môžu byť nastavené ako výstupné pre ovládanie pripojených zariadení alebo môžu byť nastavené ako vstupné pre načítanie binárnych stavov pripojených zariadení. Pre konfiguráciu a obsluhu portov je v mikrokontroléri použitá interný blok onačovaný ako GPIO (General Purpose Input Output). 

Základná štruktúra interného zapojenia pinu GPIO pri procesoroch STM32 je na obrázku, podrobný popis je v dokumentácii  [AN4899](./doc/AN4899.pdf). 


```{code-cell} ipython3  
:tags: ["remove-cell"]
from src.utils import *

data = r'''
Origin: Here 
include(lib_base.ckt)
include(lib_stm32.ckt)
include(lib_user.ckt)

Origin: Here 
command"\sf"
d = 2;

move to (0.5, 4);
# vstupne diody
GP: gpio_port(5*d/8,L); {"\sf I/O Pin" at GP.n +(-.3, -.10) above}
dot;
{down_; diode(3*d/4,,R); gnd;}
{up_;   diode(3*d/4,,); power(0.5, $\sf V_{dd}$); }

line right_ 3*d/4; dot;
{  down_; 
   RUP: resistor(3*d/4,E); rlabel(,\sf R_{PD},); 
   {
	LUP: line from RUP.e + (.25, -0.4) to RUP.s  + (0.25, 0.4);
	line from LUP.c right_ d/4; {"\sf on" above ljust;}; {"\sf off" below ljust;}
   } 
   gnd;
}

{  up_;   
   RD: resistor(3*d/4,E);  llabel(,\sf R_{PU},);
   {
	LPD: line from RD.end + (0.25, -0.4)to RD.start  + (0.25, 0.4);
	line from LPD.c right_ d/4; {"\sf on" above ljust;}; {"\sf off" below ljust;}
   }
   power(0.5,$\sf V_{dd}$);
}

line right_ d; DT1: dot;

#============================
# digitalna cast

line down_ d+d/4 
line right_ d/2
DT5: dot

line from DT5 up_ d/8
#move to Here + (d/8, 0)
T1: fet_P(d/2,R)

line from DT5 down_ d/8
#move to Here + (d/8, 0)
T2: fet_N(d/2,R)
move to T2.S
gnd

move to T1.D
up_
VD2: tconn(d/4,O); "$\sf V_{dd}$" at VD2.n above; 

La: line from T1.G  right_ d/4
Lb: line from T2.G  right_ d/4
move to (La.end + Lb.end)/2
boxrad=0.1 
OC: box ht d wid 2*d/3
"\sf Output" at OC.c above;
"\sf Control" at OC.c below;

DIN: line <- from OC.e right_ d/2

# digit. komparator

log_init
line from DT1 right_ d;
DOUT: opamp(d/2," ", " ",0.9,)
DOUT: line -> from DOUT.Out to (DIN.end, DOUT.Out)

#------------------------------

# analogova cast
move to DT1 #+ (d,d)
line up_ d
right_; line 1;
single_switch_h(d, OFF); {"\sf Analog Option" at last [].n above; }
line -> right_ to (DOUT.end, Here); {"\sf Analog" at last line.end ljust; }


#OP: opamp(d/2,,,1,R)
#line from DT1 to (DT1, OP.In1)
#line from OP.In2 left_ d/4 
#line down_ d/2-d/8
#ACIN: line -> from Here to (DIN.end, Here)
#ACOUT:line -> from OP.Out to (DIN.end, OP.Out)

"\sf Digital In" at DOUT.end ljust; 
"\sf Digital Out" at DIN.end ljust; 
#"$\sf V_{comp}$" at ACIN.end ljust; 
#"\sf CMP" at ACOUT.end ljust

# ramik okolo analogoveho komparatora
#move to DT1 + (d, d/4+d/8)
#up_
#ABOX: box dashed ht d wid 1.6*d
#"\sf Analog Option" at ABOX.n above

'''

_ = cm_compile('img_0100b', data,  dpi=600)   
```

```{figure} ./src/img_0100b.png
:width: 500px
:name: img_0100b

Zjednodušené interné zapojenie pinu mikrokontroléru STM32.
```

Zapojenie každého pinu portu GPIO obsahuje 

* ochranné diódy voči krátkodobému prepätiu a ESD
* rezistory pre prevádzku portu v režime pull-up, pull-down
* digitálne výstupné obvody s výkonovým budičom 
* digitálne vstupné obvody s komparátorom s hysterézou
* pre vybrané piny portov multiplexer pre pripojenie analogových periférií

GPIO umožňuje nastaviť piny portov do základných výstupných konfigurácií

```{code-cell} ipython3  
:tags: ["remove-cell"]
from src.utils import *

data = r'''
Origin: Here 
include(lib_base.ckt)
include(lib_stm32.ckt)
include(lib_user.ckt)

Origin: Here 
command"\sf"

up_
move to (3.5,5)

    gnd();
Q1: fet_N(1.5,L);
    dot; {line right_ 1; tbox("Port Pin",1.5); }
Q2: fet_P(1.5,L);
    power(0.5, $\sf V_{cc}$)

    line from Q2.G left_ 0.5;
    line to (Here, Q1.G);
    dot; {line left_ 0.5; tbox("Digital Out",2,,<); }
    line to Q1.G
    circle at Q2.c - (2.5,0) rad 0.25 "A"


move to (11.5,5)
    up_;
    gnd();
Q3: fet_N(1.5,L);
    dot; {line right_ 1; tbox("Port Pin",1.5); }
Q4: fet_P(1.5,L);
    power(0.5, $\sf V_{cc}$)
R1: resistor(left_ 1 from Q3.G,E)
R2: resistor(left_ 1 from Q4.G,E)
    line 0.5 from R2.end;
    line to (Here, R1.end);
    dot; {line left_ 0.5; tbox("Digital Out",2,,<); }
    line to R1.end;
    circle at Q4.c - (3,0) rad 0.25 "B"


move to (3.5, 0)

    up_;
    gnd;
    resistor(1.5, E); rlabel(,\sf R_{PD},)
    dot; 
    {
        {line left_ 1.5; tbox("Digital In",2,, >);}
        line right_ 1;
        tbox("Port Pin",1.5); 
    }
Q5: fet_P(1.5,L);
    power(0.5, $\sf V_{cc}$);
    {line from Q5.G left_ 1; tbox("Digital Out",2,,<); }
    circle at Q5.c - (2.5,-1) rad 0.25 "C";


move to (11.5, 0)
    up_;
    gnd;
Q6: fet_N(1.5,L);
    dot; 
    {
        {line left_ 1.5; tbox("Digital In",2,, >);}
        line right_ 1;
        tbox("Port Pin",1.5); 
    }
    resistor(up_ 1.5, E); rlabel(,\sf R_{PU},)
    power(0.5, $\sf V_{cc}$);
    {line from Q6.G left_ 1; tbox("Digital Out",2,,<); }
    circle at Q6.c - (2.5,-2) rad 0.25 "D";
'''

_ = cm_compile('img_0100c', data,  dpi=600)   
```

```{figure} ./src/img_0100c.png
:width: 600px

Konfigurácie výstupného pinu.
```


Okrem štandardnej funkcie pinu ako GPIO portu majú piny púzdra aj možnosť *alternatívnych funkcií*, kedy sú pripojené na interné periférie mikrokontroléra, napr. časovače, sériové rozhrania a pod. Pri návrhu komplikovanejších zariadení s mikrokontrolérom vyžaduje pridelenie pinov portom a perifériam dobré premyslenie návrhu.  

Časť pinov GPIO je výrobcom označená ako FT, umožňuje ich použitie pre periférie napájané napätím 5V, aj keď mikrokontrolér je napájaný zo zdroja s napätím 3.3V . Toto značne zjednodušuje pripájanie digitálnych periférii pracujúcich s napätím 5V bez inak potrebného prevodníka úrovní.

