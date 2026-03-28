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


# <font color='#4B9DA9'> Základné veličiny  </font>

##  <font color='#547792'> Prúd  </font>

Elektrický prúd je usmernený tok elementárnych elektrických častíc, elektrónov. Elektrón reprezentuje elementárny elektrický náboj, ktorého hodnota je $e = -1.602 \times 10^{-19} \,\,\, \text{Coulomb}$. V analógii s prúdením kvapaliny, kde môžeme prúd kvapaliny pokladať za množstvo kvapaliny, ktoré pretečie otvorom za  stanovený čas v jednotkách litrov za sekundu, môžeme rovnako aj elektrický prúd $I$ pokladať za množstvo náboja $Q$, ktoré pretečie vodičom za čas $t$. Jednotkou prúdu je *Ampér* [A].

$$
\text{Prúd} = \frac{\text{Náboj}}{\text{Čas}} \,\,\,\, \text{alebo} \,\,\,\, I=\frac{Q}{t} \,\,[A]
$$

Prúdu $1$ *Ampér* zodpovedá náboji $1$ *Coulumb*, ktorý pretiekol vodičom za jednu sekundu, čo zodpovedá počtu $6.25 \times 10^{18}$ elementárnych nábojov.
Elektrický prúd $I$ v uvedenom vzťahu reprezentuje priemernú hodnotu prúdu za čas $t$, v elektronike nás ale častejšie zaujíma okamžitá hodnota prúdu $i$, ktorý tečie obvodom v čase $t$

$$
i(t) =\frac{d Q}{d t} 
$$

Na základe konvencie v elektronických obvodoch znázorňujeme smer prúdu ako pohyb kladných nábojov, aj keď samotný prúd je spôsobený tokom elektrónov so zápornym nábojom.  


```{code-cell} ipython3  
:tags: ["remove-cell"]
from src.utils import *

data = r'''
include(lib_base.ckt)
include(lib_stm32.ckt)
include(lib_user.ckt)

command"\sf"

up_; 
BB: battery(,1);  rlabel(,,+);
    line from BB.end right_ 2; l_current(I, above_, 0.55 ); 
    down_;
    lamp();
    line to BB.start
'''

_ = cm_compile('img_0251a', data,  dpi=600)   
```

```{figure} ./src/img_0251a.png
:width: 200px
:name: img_0251a

Znázornenie prúdu elektrickým obvodom.
```

Ak elektrický prúd preteká uzlom, v ktorom sa delí do niekoľkých vetiev, súčet prúdov vytekajúcich z uzla musí byť rovný súčtu prúdov do uzla vtekajúcich.

```{code-cell} ipython3  
:tags: ["remove-cell"]
from src.utils import *

data = r'''
include(lib_base.ckt)
include(lib_stm32.ckt)
include(lib_user.ckt)

up_; 
BB: battery(2.5,1);  rlabel(,,+); 
    line right_ 1.5; l_current(I_0,above,0.5); 
    dot; "$Q$" below rjust;       
    { 
        line right_ 0.75 up_ 0.75; l_current(I_1,above rjust, 0.75)
        line right_ 2;
        down_; lamp(2);
        LA: line to (Here, BB.start)
    };      
    line right_ 0.75 down_ 0.75; l_current(I_2,above ljust, 0.75); 
    line right_ 1;
    down_; lamp(1.5);
    LB: line to (Here, BB.start);
    line from LA.end to LB.end; dot;
    line to BB.start;
'''

_ = cm_compile('img_0251d', data,  dpi=600)   
```

```{figure} ./src/img_0251d.png
:width: 300px
:name: img_0251d

Elektrický prúd pretekajúci uzlom.
```

Podľa konvencie je prúd do uzla vtekajúci záporný, vytekajúci kladný. Pre uzol *Q* na obrázku {numref}`img_0251d` potom platí *prvý Kirchhoffov zákon* (zákon zachovania elektrického náboja)

$$
I_0 = I_1 + I_2
$$

alebo vo všeobecnom tvare

$$
\sum_{k=1}^n I_k = 0
$$



##  <font color='#547792'> Napätie  </font>

Ak v hydraulickom systéme je prúdenie kvapaliny podmienené pritomnosťou zariadenia, ktoré pôsobením tlaku uvádza kvapalinu do pohybu, podobne aj v elektrickom obvode je pohyb elektrónov a následne elektrický prúd spôsobený zdrojom elektrického napätia, Takýmto napäťovým zdrojom je napríklad batéria a jej napätie označuje ako *elektromotorické napätie*. Ak tlak kvapaliny v hydraulickom systéme meriame v jednotkách tlaku, v elektrickom obvode meriame napätie v jednotkách *Volt*. Napätie v obvode označujeme písmenom *V* alebo *U*. 


```{code-cell} ipython3  
:tags: ["remove-cell"]
from src.utils import *

data = r'''
include(lib_base.ckt)
include(lib_base.ckt)
include(lib_stm32.ckt)
include(lib_user.ckt)

up_; 
BB: battery(,1);  rlabel(,,+);
    line from BB.end right_ 1.5; C1: circle rad 0.1; "\it a" ljust;
    line from BB.start right_ 1.5; C2: circle rad 0.1;  "\it b" ljust;
    L1: line -> from C1.s + (0, -0.1) to C2.n + (0, 0.1); "$V_{ab}$" at last line.center ljust; 
'''

_ = cm_compile('img_0251b', data,  dpi=600)   
```

```{figure} ./src/img_0251b.png
:width: 210px
:name: img_0251b

Napätie zdroja medzi svorkami *a*,*b*. 
```

Podobne ako v hydraulickom systéme prietok kvapaliny zúženým miestom spôsobí úbytok tlaku, podobne aj v elektrickom obvode spôsobí prechod prúdu prvkom reprezentujúcim odpor, napríklad rezistorom,  úbytok napätia na takomto prvku.

```{code-cell} ipython3  
:tags: ["remove-cell"]
from src.utils import *

data = r'''
include(lib_base.ckt)
include(lib_base.ckt)
include(lib_stm32.ckt)
include(lib_user.ckt)

up_; 
BB: battery(3,1);  rlabel(,,+); larrow(V_{0}, <-);
    line from BB.end right_ 1.5; l_current(i, above_, 0.55 );
    resistor(down_ 1.5, E); larrow(V_{2}, ->); rlabel(,R_2,)
    resistor(down_ 1.5, E); larrow(V_{1}, ->); rlabel(,R_1,);
    line to BB.start
    
    #line from BB.start right_ 1.5; C2: circle rad 0.1;  "b" ljust;
    #L1: line -> from C1.s + (0, -0.1) to C2.n + (0, 0.1); "$V_{ab}$" at last line.center ljust; 
'''

_ = cm_compile('img_0251c', data,  dpi=600)   
```

```{figure} ./src/img_0251c.png
:width: 230px
:name: img_0251c
Úbytok napätia na rezistívnych prvkoch obvodu.
```

Pre úbytok napätia na rezistore platí *Ohmov zákon*


$$
V = R \cdot I
$$

Súčet úbytkov napätí v uzatvorenej slučke elektrického obvodu musí byť rovný súčtu elektromotorických napätí, ktoré vytvárajú prúd obvodom. Tento princíp definuje  *druhy Kirchhoffov zákon* (zákon o slučkových napätiach), pre obvod na {numref}`img_0251c` platí

$$
V_0 = V_1 + V_2
$$

alebo vo všeobecnom tvare

$$
\sum_{k=1}^n V_k = 0
$$


##  <font color='#547792'> Výkon  </font>

Súčin jednosmerného napätia a jednosmerného prúdu je výkon, jednotkou výkomu je *Watt*

$$
P = U \cdot I \,\,\, [W]
$$

