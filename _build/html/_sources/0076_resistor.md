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



# <font color='#4B9DA9'>  Rezistor  </font>

V elektronických obvodoch je odpor reprezentovaný vlastným odporom prepojovacích vodičov medzi komponentami a špeciálnym elektronickým komponentom - rezistorom (ľudové pomenovanie odpor nie je správne). Technologicky sú rezistory vyrábané roznymi postupmi v závislosti od účelu ich použitia, zvyčajne s využitím materiálov s rôznym merným odporom ako vodičov s rôznym prierezom alebo vo forme tenkých vrstiev nanesených na nevodivý materiál (keramika).   

```{figure} ./img/resistor_1.jpg
:width: 400px
:name: mp_0076a

Typy rezistorov.
```

TODO SMD

V niektorých prípadoch je vhodné použiť rezistor, ktorého hodnotu možeme mechanicky meniť, označujú sa ako potenciometre, trimre, premenné rezistory

```{figure} ./img/resistor_3.jpg
:width: 400px
:name: mp_0076b

Premenné rezistory.
```

V schémach zapojenia sa používajú pre rezistory nasledujúce značky

TODO Značky

##  <font color='#547792'> Hodnoty štandardných rezistorov  </font>

Hodnoty rezistorov sa môžu pohybovať v širokom rozsahu niekoľkých rádov. Aby bolo možné vyrábať rezistory v definovanom počte hodnôt, boli určené rady hodnôt. Hodnoty sú určené tak, aby v logaritmickej mierke boli približne rovnako rozložené v rámci jedného rádu,  podľa vzťahu

\begin{equation*}
X_n = round(\sqrt[\leftroot{5}\uproot{3} m]{10^n} )
\end{equation*}

kde $m$ je počet hodnôt v ráde a $n=0 \dots m-1$. Napríklad hodnoty všetkých rezitorov pre radu *E6* spočítame nasledujúcim programom

```{code-cell} ipython3  
from numpy import *
m = 6
for n in range(m):      # 0 .. m-1
    r = power(10, n)    
    x = power(r, 1/m)   
    print(round(x,1), end=', ')   
```

Reálne dodávané hodnoty sa v niektorých hodnotách mierne líšia, napr. v rade E6 je miesto hodnoty 3.2 použitá hodnota 3.3, miesto 4.6 hodnota 4.7. Vyrábané hodnoty sú dekadickými podielmi a násobkami týchto hodnôt, napríklad 0.1, 0.15 ... 1,1.5 ... 10, 15, ... 2200, 3300, ... 680000, ...

Pre radu E24 sú vyrábané hodnoty: 

    1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 
    2.0, 2.2, 2.4, 2.7, 
    3.0, 3.3, 3.6, 3.9, 4.3, 4.7, 
    5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1

Okrem počtu hodnôt v rade sa jednotlivé rady líšia aj toleranciou hodnôt, čím vyššia rada, tým je tolerancia hodnôt menšia.  
    
Na rezistoroch bývala niekedy hodnota vyznačená textom, čo ale pri malých rozmeroch nebolo je príliš praktické, preto sa pri označovaní rezistorov začal používať aj farebný kód v podobe prúžkov na rezistore. Výhodou tohoto značenie je, že na rozdiel od textu je viditeľné zo všetkých strán.


```{figure} ./img/resistor_4.png
:width: 500px
:name: mp_0076d

Farebné značenie hodnôt rezistorov.
```

##  <font color='#547792'> Základné zapojenia rezistorov  </font>

### <font color='#E37434'> Sériové zapojenie rezistorov </font>

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


Ekvivalentný odpor séeriovho zapojenia rezistorov

\begin{equation*}
u = u_{1} + u_{2} \\
u = R_1 i + R_2 i \\
\frac{u}{i} = R = R_1  + R_2 
\end{equation*}

Napäťový delič

\begin{equation*}
\frac{u}{R_1 + R_2} = \frac{u_2}{R_2}  
\end{equation*}

\begin{equation*}
u_2 = \frac{R_2}{R_1 + R_2} u  
\end{equation*}

```{dropdown}  <font color='#84B179'> Príklad </font>
Delič napätia pre prevodník

```

### <font color='#E37434'> Paralelné zapojenie rezistorov </font>

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

_ = cm_compile('img_0076s', data,  dpi=600)   
```

```{figure} ./src/img_0076s.png
:width: 260px
:name: img_0076s

Paralelné zapojenie rezistorov.
```



Ekvivalentý odpor paraleleného zapojenia rezistorov

\begin{equation*}
i = i_1 + i_2\\
\frac{1}{R} = \frac{1}{R_1} + \frac{1}{R_2}\\
R = \frac{R_1 R_2}{R_1 + R_2}
\end{equation*}

Prúdový delič

\begin{equation*}
R i = R_1 i_1 \\
\frac{R_1 R_2}{R_1 + R_2} i = R_1 i_1 \\
i_1 = \frac{R_2}{R_1 + R_2} i
\end{equation*}


```{dropdown}  <font color='#84B179'> Príklad </font>
```
