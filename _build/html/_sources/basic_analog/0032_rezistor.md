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

`````{admonition} Výpočet hodnôt v rade E6
:class: dropdown, tip

Hodnoty pre radu *E6* spočítame nasledujúcim programom

```{code-block} ipython3
:class: dropdown, note
from numpy import *
m = 6                   # rada E6
for n in range(m):      # 0 .. m-1
    r = power(10, n)    
    x = power(r, 1/m)   
    print(round(x,1), end=', ') 
```

    1.0, 1.5, 2.2, 3.2, 4.6, 6.8, 

Reálne vyrábané hodnoty sa v niektorých hodnotách od teoretických mierne líšia, napr. v rade *E6* je miesto hodnoty 3.2 použitá hodnota 3.3, miesto 4.6 hodnota 4.7. 
`````

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

   
### <font color='#E37434'> Farebný kód hodnôt THT rezistorov</font>

Na rezistoroch bývala hodnota vyznačená textom, čo ale pri malých rozmeroch nie je príliš praktické, preto sa pri označovaní rezistorov začal používať aj kód hodnoty v podobe farebných prúžkov na rezistore. Výhodou tohoto značenie je, že na rozdiel od textu je viditeľné zo všetkých strán.


```{figure} ./img/resistor_5.jpg
:width: 450px
:name: mp_0076d

Farebné značenie hodnôt THT rezistorov.
```

### <font color='#E37434'> Značenie hodnôt SMD rezistorov </font>

Hodnoty bezvývodových rezistorov pre povrchovú montáž sú značené číselným 3 alebo 4 ciferným kódom. Hodnoty malých rezistotov začínajú písmenom **R**. 

```{figure} ./img/smd_code.png
:width: 400px
:name: mp_0032e

Značenie hodnôt SMD rezistorov.
```


### <font color='#E37434'>   Sériové zapojenie rezistorov   </font>


```{code-cell} ipython3  
:tags: ["remove-cell"]
from src.utils import *

data = r'''
include(lib_base.ckt)
include(lib_user.ckt)

Origin: Here 

right_;
circle rad 0.09; {"\it a" at last circle.n above;}
line 0.65; r_current(I, above, 0.85 );
right_; 
resistor(1.75, E); rlabel(,R_1,); larrow(U_{1}, ->, 0.25)
resistor(1.75, E); rlabel(,R_2,); larrow(U_{2}, ->, 0.25)
resistor(1.75, E); rlabel(,R_3,); larrow(U_{3}, ->, 0.25)
line 0.5 dotted;
resistor(1.75, E); rlabel(,R_N,); larrow(U_{N}, ->, 0.25)
line 0.65;
circle rad 0.09; "\it b" at last circle.n above;
'''

_ = cm_compile('img_0032s', data,  dpi=600)   
```

```{figure} ./src/img_0032s.png
:width: 460px
:name: img_0032s

Sériové zapojenie rezistorov.
```

V sériovom zapojení rezistorov preteká všetkými rezistormi rovnaký prúd, napätie na sériovo zapojených rezistoroch je súčtom napätí na jednotlivých rezistoroch. Pre odpor $R_{ab}$ sériového zapojenia rezistorov medzi svorkami *ab* potom platí  

\begin{align*}
U =& U_{1} + U_{2} + \dots + U_N \\
U =& R_1 \, I + R_2 \, I + \dots + R_N \, I\\
R_{ab} = \frac{U_{ab}}{I} =&  R_1  + R_2 + \dots + R_N = \sum_{i=1}^N R_i 
\end{align*}

Celkový odpor sériovo zapojených rezistorov je vždy väčší ako odpor najväčšieho z nich. 

### <font color='#E37434'>  Paralelné zapojenie rezistorov </font>


```{code-cell} ipython3  
:tags: ["remove-cell"]
from src.utils import *

data = r'''
include(lib_base.ckt)
include(lib_user.ckt)

    {    
    line up 0.95;
    dot; {
            line up_ 0.95;
            dot;{
                  line up_ 1.25 dashed;
                  R4: resistor(right_ 2.5, E); 
                  llabel(,R_N,); b_current(I_{N} ); 
                }
            R3: resistor(right_ 2.5, E); 
            llabel(,R_3,); b_current(I_{3} );
         }
    R2: resistor(right_ 2.5, E); 
    llabel(,R_2,); b_current(I_{2} );
    }
R1: resistor(right_ 2.5, E);
    llabel(,R_1,); b_current(I_{1} );

    line from R4.end to R3.end dashed; dot;
    line from R3.end to R2.end; dot;
    line from R2.end to R1.end; 

Q1: 0.5 between R3.start and R2.start;
    dot(at Q1);
    line from Q1 left_ 1.5; r_current(I, above, 0.55 ); 
    circle rad 0.09; "a" at last circle.n above;

Q2: 0.5 between R3.end and R2.end;
    dot(at Q2);
    line from Q2 right_ 1.5; 
    circle rad 0.09; "b" at last circle.n above;
'''

_ = cm_compile('img_0032q', data,  dpi=600)   
```

```{figure} ./src/img_0032q.png
:width: 300px
:name: img_0032q

Paralelné zapojenie rezistorov.
```

Pri paralelnom zapojení rezistorov je na všetkých rezistoroch rovnaké napätie $U$, prúd pretekajúci obvodom je súčtom prúdov pretekajúcich rezistormi. Pre odpor $R_{ab}$ paralelného zapojenia rezistorov medzi svorkami *ab* potom platí  

\begin{align*}
I =& I_{1} + I_{2} + \dots + I_N \\
I = \frac{U}{R_{ab} } =& \frac{U}{R_1}  + \frac{U}{R_2}  + \dots + \frac{U}{R_N} \\
\frac{1}{R_{ab}} = & \frac{1}{R_1}  + \frac{1}{R_2} + \dots + \frac{1}{R_N} = \sum_{i=1}^N \frac{1}{R_i} 
\end{align*}

Celkový odpor paralelne zapojených rezistorov je vždy menší ako odpor najmenšieho z nich. 

**TODO** program na vyhladanie seriovej a paralelnej kombinácie rezistorov.
