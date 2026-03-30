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


## <font color='#547792'> Základné zapojenia rezistorov  </font>

## <font color='#E37434'> Sériové zapojenie rezistorov </font>

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


