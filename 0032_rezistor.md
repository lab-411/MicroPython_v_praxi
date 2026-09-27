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



# <font color='#4B9DA9'> Rezistor  </font>

V elektronických obvodoch je elektrický odpor reprezentovaný pasívnym prvkom - rezistorom (ľudové pomenovanie *odpor* nie je správne). Hodnota odporu rezistora je udávaná v jednotkách *Ohm*, značka $\Omega$. V zapojeniach označujeme rezistor písmenom *R*. 

```{code-cell} ipython3  
:tags: ["remove-cell"]
from src.utils import *

data = r'''
include(lib_base.ckt)
include(lib_stm32.ckt)
include(lib_user.ckt)

up_; 
R1: resistor(1.8,E); rlabel(,R,);
    line left_ 1; r_current(I, above, 0.5)
C1: circle rad 0.08; "$+$" rjust;
    line from R1.start left_ 1; 
C2: circle rad 0.08; "$-$" rjust; 
    line -> from C1.s+(0,-.1) to C2.n+(0,0.1); "$U$" at last line.center rjust;
'''

_ = cm_compile('img_0032a', data,  dpi=600)   
```

```{figure} ./src/img_0032a.png
:width: 150px
:name: img_0032a

Prúd a napätie rezistorom.
```

Pre vzťah prúdu pretekajúcim ideálnym rezistorom, jeho odporom a úbytkom napätia na rezistore platí *Ohmov zákon*

$$
U = R \cdot I 
$$

Prechodom prúdu rezistorom sa energia elektrického prúdu mení na teplo, stratový výkon ktorý vzniká na rezistore je potom 

$$
P= U \cdot I = R \cdot U^2 = \frac{U^2}{R}
$$

##  <font color='#547792'> Prevedenie </font>

Elektrický odpor vodiča je určený materiálovými vlastnosťami vodiča, je priamo úmerný dĺžke vodiča $l$ a nepriamo úmerný jeho prierezu $S$

$$
R = \rho \frac{l}{S}
$$

kde $\rho$ je merný elektrický odpor materiálu vodiča. Merný odpor materiálu ako aj odpor vodiča závisia od teploty, pri kovových materiáloch s rastúcou teplotou stúpa podľa vzťahu


$$
\rho = \rho_0 \, (1 + \alpha \Delta t) \\
\\
R= R_0 \, (1 + \alpha \Delta t) \\
$$

Typické hodnoty merného odporu a teplotnáho súčinitelu pre vybrané materiály sú uvedené v tabulke


| Materiál | Zloženie | $\rho$ | $\alpha$ | 
| :---     | :----    | :----  |   :----  | 
| Striebro |  Ag      |     17 |     3.80 |
| Meď      |  Cu      |     18 |     3.92 |


Rezistory vyrábané rôznymi postupmi v závislosti od účelu ich použitia, zvyčajne s využitím materiálov s rôznym merným odporom ako vodičov s rôznym prierezom navinutým na keramickom teliesku alebo vo forme tenkých uhlíkových alebo kovových vrstiev nanesených na vhodný elektricky nevodivý materiál.

```{figure} ./img/resistor_1.jpg
:width: 350px
:name: mp_0076a

Typy rezistorov THT (*Through Hole Technology*).
```

```{figure} ./img/resistor_4.jpg
:width: 350px
:name: mp_0076e

Typy rezistorov SMD (*Surface Mount Device*).
```

V niektorých prípadoch je vhodné v elektrickom obvode použiť rezistor, ktorého hodnotu možeme mechanicky meniť, takéto rezistory potom označujeme sa ako potenciometre, trimre alebo premenné rezistory.

```{figure} ./img/resistor_3.jpg
:width: 400px
:name: mp_0076b

Premenné rezistory.
```

V schémach zapojenia obvodov sa používajú pre rezistory nasledujúce značky ($R_1$ rezistor podľa európskeho značenia, $R_2$ rezistor podľa anglosaského značenia, $R_3$ potenciometer, $R_4$ trimer)

```{code-cell} ipython3  
:tags: ["remove-cell"]
from src.utils import *

data = r'''
include(lib_base.ckt)
include(lib_stm32.ckt)
include(lib_user.ckt)

#Grid(6,1.5)
    up_;
    
    move to (1,0);  
    R1: ebox(1.5, 0.8); "$R_1$" at R1.c+(-0.1,0) rjust;   

    move to (2.5,0); 
    R2: resistor(1.5); "$R_2$" at R2.c+(-0.1,0) rjust;  
    
    move to (4,0)
    R3: vres_v(1.5,); line from R3.S down_ 0.35; "$R_3$" at R3.c+(-0.15,0) rjust;  
    
    move to (5.5,0+1.5)
    R4: vres_v(1.5,T); line from R4.S down_ 0.35; "$R_4$" at R4.c+(-0.15,0) rjust; 
'''

_ = cm_compile('img_0076t', data,  dpi=600)   
```

```{figure} ./src/img_0076t.png
:width: 400px
:name: img_0076t

Značky rezistorov.
```


##  <font color='#547792'> Hodnoty rezistorov  </font>

Hodnoty rezistorov sa môžu pohybovať v širokom rozsahu niekoľkých rádov. Aby bolo možné vyrábať rezistory v definovanom počte hodnôt, boli určené [rady](https://en.wikipedia.org/wiki/E_series_of_preferred_numbers) hodnôt. Hodnoty sú určené tak, aby v logaritmickej mierke boli približne rovnako rozložené v rámci jedného rádu, podľa vzťahu

\begin{equation*}
X_n = round(\sqrt[\leftroot{5}\uproot{3} m]{10^n} )
\end{equation*}

kde $m$ je počet hodnôt v ráde a $n=0 \dots m-1$. 

:::{dropdown} <font color='#84B179'> Výpočet hodnôt v rade E6</font>

Hodnoty pre radu *E6* spočítame nasledujúcim programom

```{code} python  
from numpy import *
m = 6
for n in range(m):      # 0 .. m-1
    r = power(10, n)    
    x = power(r, 1/m)   
    print(round(x,1), end=', ') 
```
Reálne vyrábané hodnoty sa v niektorých hodnotách od teoretických mierne líšia, napr. v rade *E6* je miesto hodnoty 3.2 použitá hodnota 3.3, miesto 4.6 hodnota 4.7. 

:::

**Rada E3**

    1.0, 2.2, 4.7
    
**Rada E6**

    1.0, 1.5, 2.2, 3.3, 4.7, 6.8
    
**Rada E12** 

    1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2  
    
**Rada E24**

    1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0, 
    3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1


Vyrábané hodnoty sú dekadickými podielmi a násobkami týchto hodnôt, napríklad 0.1, 0.15 ... 1, 1.5 ... 10, 15, ... 2200, 3300, ... 680000, ... Pre jednotlivé rady je stanovená tolerancia hodnôt tak, aby sa susedné hodnoty v rozsahu tolerancie neprekrývali, napríklad pre radu **E3** je maximálna tolerancia 40%, pre **E24** je tolerancia 5%.   

   
### <font color='#E37434'> Farebný kód </font>

Na rezistoroch bývala hodnota vyznačená textom, čo ale pri malých rozmeroch nie je príliš praktické, preto sa pri označovaní rezistorov začal používať aj kód hodnoty v podobe farebn7ch prúžkov na rezistore. Výhodou tohoto značenie je, že na rozdiel od textu je viditeľné zo všetkých strán.


```{figure} ./img/resistor_5.jpg
:width: 450px
:name: mp_0076d

Farebné značenie hodnôt rezistorov.
```

**TODO** značenie SMD rezistorov

**TODO** program na vyhladanie seriovej a paralelnej kombinácie rezistorov.



### <font color='#E37434'>   Sériové zapojenie rezistorov   </font>


```{code-cell} ipython3  
:tags: ["remove-cell"]
from src.utils import *

data = r'''
include(lib_base.ckt)
include(lib_stm32.ckt)
include(lib_user.ckt)

right_;
circle rad 0.09; {"a" at last circle.n above;}
resistor(1.5, E); llabel(,R_1,);
resistor(1.5, E); llabel(,R_2,);
resistor(1.5, E); llabel(,R_3,);
resistor(1.5, E); llabel(,R_4,);
line 0.5 dotted;
resistor(1.5, E); llabel(,R_N,);
circle rad 0.09; "b" at last circle.n above;
'''

_ = cm_compile('img_0032s', data,  dpi=600)   
```

```{figure} ./src/img_0032s.png
:width: 400px
:name: img_0032s

Sériové zapojenie rezistorov.
```
Odpor sériového zapojenia rezistoroch

$$
R_{ab} = R_1 + R_2 + \dots + R_N = \sum_{i=1}^N R_i
$$

Výsledný odpor sériového zapojenia rezistorov je vždy väčší ako odpor naväčšieho z nich.

### <font color='#E37434'>  Paralelné zapojenie rezistorov </font>


```{code-cell} ipython3  
:tags: ["remove-cell"]
from src.utils import *

data = r'''
include(lib_base.ckt)
include(lib_stm32.ckt)
include(lib_user.ckt)

{ 
    line up 0.95;
    dot; {
            line up_ 0.95;
            dot;{
                  line up_ 0.95;
                  R4: resistor(right_ 1.75, E); 
                  llabel(,R_4,);
                }
            R3: resistor(right_ 1.75, E); 
            llabel(,R_3,);
         }
    R2: resistor(right_ 1.75, E); 
    llabel(,R_2,);
}
R1: resistor(right_ 1.75, E);
llabel(,R_1,);


line from R4.end to R3.end; dot;
line from R3.end to R2.end; dot;
line from R2.end to R1.end; 

Q1: 0.5 between R3.start and R2.start;
dot(at Q1);
line from Q1 left_ 1; circle rad 0.09; "a" at last circle.n above;

Q2: 0.5 between R3.end and R2.end;
dot(at Q2);
line from Q2 right_ 1;  circle rad 0.09; "b" at last circle.n above;
'''

_ = cm_compile('img_0032q', data,  dpi=600)   
```

```{figure} ./src/img_0032q.png
:width: 280px
:name: img_0032q

Paralelené zapojenie rezistorov.
```


##  <font color='#547792'> Použitie rezistorov  </font>


### <font color='#E37434'> Napäťový delič </font>

```{code-cell} ipython3  
:tags: ["remove-cell"]
from src.utils import *

data = r'''
include(lib_base.ckt)
include(lib_stm32.ckt)
include(lib_user.ckt)

define(`source_DC',`[
    S: source($1,); rarrow($2, ->, 0.2);
    dx = 0.2;
    dy = 0.05;
    line from S.c-(dx, -dy) to S.c+(dx, dy);
    line from S.c-(dx, dy) to S.c+(dx, -dy);
    N: S.n;
    S: S.s;
    C: S.c;
]')

Origin: Here 


d = 1.5;

#-----------------------------------------------------------------------
move to (2.5, 3);
down_;

R1: resistor(d,,E); rlabel(,R_1,); larrow(u_{1}, ->, 0.2)
dot;
R2: resistor(d,,E); rlabel(,R_2,); larrow(u_{2}, ->, 0.2)
 
move to (R1.end -(d, -d/2 )  )


S: source_DC(down_ d, u ); 
line from S.N to (S.N.x, R1.start.y); 
line -> right d/2; {"\textit{i}" at last line.e above}
line to R1.start;
line from S.S to (S.S.x, R2.end.y) to R2.end;
'''

_ = cm_compile('img_0076r', data,  dpi=600)   
```

```{figure} ./src/img_0076r.png
:width: 210px
:name: img_0076r

Sériové zapojenie rezistorov.
```


Ekvivalentný odpor sériovho zapojenia dvoch rezistorov

\begin{align*}
u =& u_{1} + u_{2} \\
u =& R_1 \, i + R_2 \, i \\
R = \frac{u}{i} =&  R_1  + R_2 
\end{align*}

Celkový odpor sériovo zapojených rezistorov je vždy väčší ako odpor najväčšieho z nich. Pre $N$ sériovo zapojených rezistorov platí

\begin{equation*}
R = \sum_{i=1}^N R_i 
\end{equation*}


```{dropdown}  <font color='#84B179'> Napäťový delič </font>

Senzor, ktorého výstupné napätie $u$ sa pohybuje v rozsahu od 0 do 10V, máme pripojiť k analogovo-digitálnemu prevodníku so vstupným rozsahom napätí $u_2$ od 0 do 3.3V. Senzor môžeme zaťažiť celkovým odporom 10k. Určíme hodnoty sériového zapojenia rezistorov $R_1$ a $R_2$, ktoré tvoria napäťový delič.

Pre napäťový delič platí

\begin{align*}
\frac{u_{2}}{R_2} =& \frac{u}{R_1 + R_2}  \\
\\
u =& 10 \text{V} \\
u_2 =& 3.3 \text{V} \\
R_1 + R_2 =& 10 \text{k}  \\
\end{align*}

Po dosadení dostaneme hodnoty  $R_2 = 3k3$ a $R_1 = 6k7$.

```

### <font color='#E37434'> Prúdový delič </font>

```{code-cell} ipython3  
:tags: ["remove-cell"]
from src.utils import *

data = r'''
include(lib_base.ckt)
include(lib_stm32.ckt)
include(lib_user.ckt)

define(`source_DC',`[
    S: source($1,); rarrow($2, ->, 0.2);
    dx = 0.2;
    dy = 0.05;
    line from S.c-(dx, -dy) to S.c+(dx, dy);
    line from S.c-(dx, dy) to S.c+(dx, -dy);
    N: S.n;
    S: S.s;
    C: S.c;
]')


Origin: Here 

d = 1.5;
move to (3.5, 2.5);

D1: dot
line -> from D1 left d/2; {"\textit{$i_1$}" at last line.end above}
line left d/4; 
R1: resistor(down_ d,,E); llabel(,R_1,);

line -> from D1 right d/2; {"\textit{$i_2$}" at last line.end above}
line right d/4; 
R2: resistor(down_ d,,E); rlabel(,R_2,);

line from R1.end right (d/2+d/4); 
D2: dot;
line to R2.end;

move to R1.centre - (d, -d/2);
S: source(down_ d, I);
line from S.start up_ d/2; 
line -> right d; {"\textit{$i$}" at last line.end above}
line to (D1.x, Here.y) to D1

line from S.end down_ d/2; 
line right d;
line to (D2.x, Here.y) to D2

line -> from D1 -(0, 0.2) to D2 + (0, 0.2); {"\textit{$u$}" at last line.c ljust}
'''

_ = cm_compile('img_0076k', data,  dpi=600)   
```

```{figure} ./src/img_0076k.png
:width: 260px
:name: img_0076k

Paralelné zapojenie rezistorov.
```

Ekvivalentý odpor paralelného zapojenia dvoch rezistorov

\begin{align*}
i =& i_1 + i_2 \\
\frac{1}{R} =& \frac{1}{R_1} + \frac{1}{R_2} \\
R =& \frac{R_1 R_2}{R_1 + R_2}
\end{align*}

Celkový odpor paralelne zapojených rezistorov je vždy menší ako odpor najmenšieho z nich. Pre N paralelne zapojených rezistorov platí

$$
\frac{1}{R} = \sum_{i=1}^N \frac{1}{R_i} 
$$






