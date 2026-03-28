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


% vykreslenie obrazkov v matplotlib-e pred volanim generovania CM makier
```{code-cell} ipython3  
:tags: ["remove-cell"]

from numpy import *
import pylab as plt
plt.rcParams['figure.dpi'] = 150

T = linspace(0, 5*pi*2, 1000)     # 2*pi*t

m  = 0.5
A0 = 1
ct = A0*(1 + m*cos(T))     # modulacny signal
am = ct * cos(10*T)        # amplitudova modulacia

plt.plot(T, am)
plt.plot(T, ct, 'k--')
plt.plot(T,-ct, 'k--')
plt.title(r'Modulačný činiteľ ' + str(m))
plt.grid()
plt.xlabel('t')
plt.ylabel('AM')

plt.savefig('am_signal.png', dpi=300)
plt.close()
```



# <font color='#4B9DA9'> Vlastnosti signálov  </font>

V elektronickom obvode pokladáme za signál časovo premenlivé napätie alebo prúd, ktorý prenáša informáciu. 

##  <font color='#547792'> Binárne signály  </font> 

V ideálnych binárnych signáloch má napätie v každom okamžiku len jednu z dvoch hodnôt, označovaných ako H (High) alebo L (Low). Informácia je v signáli reprezentovaná postupnosťou impulzov o dĺžke $t$, pri ich opakovani s periódou $T$. Skupina niekoľkých impulzov môže vytvárať *burst*. 

```{code-cell} ipython3  
:tags: ["remove-cell"]
from src.utils import *

data = r'''
scale=1.5

include(lib_base.ckt)
include(lib_stm32.ckt)
include(lib_user.ckt)
include(lib_color.ckt)

right_;
move to (0,0);                              # "0" below;

linethick_(1.25);
color_red;
line from (0,0) to (1,0) then to (1,1) then to (1.5, 1) then to (1.5, 0) then to (2.5, 0) then to (2.5, 1);
line to (3,1) to (3,0) then to (4, 0); 

right_;
line from (5,0) to (5.5, 0)  then to (5.5,1) then to (6,1) then to (6,0) then to (7,0);
#then to (5.5, 1) then to (5.5, 0) then to (6.5,0);


linethick_();
color_orange;
line from (1,-0.5) to (1, 1.75) dashed; 
line from (1.5, 1) to (1.5, 1.25) dashed; 
line from (2.5,-0.5) to (2.5, 0) dashed; 
line from (7,-0.5) to (7, 1.75) dashed; 

color_black;
line <-> from (1, -0.35) to (2.5, -0.35); "T" at last line.center above; 
line <-> from (1, 1.25) to (1.5, 1.25);   "t" at last line.center above; 
line <-> from (1, 1.5) to (7, 1.5); "Burst N.T" at last line.center above;

color_black;
line  from (-0.25,0) to (4,0);     
line from (4,0) to (5,0) dashed;
line -> to (7.5,0); "t" above ;
line -> from (0,-0.25) to (0,2);

color_blue;
line  from (-0.25,1) to (2*pi+0.5,1) dotted;

'''

_ = cm_compile('img_0072c', data,  dpi=600)   
```

```{figure} ./src/img_0072c.png
:width: 600px
:name: img_0072c

Parametre binárneho signálu.
```

##  <font color='#547792'> Harmonické signály  </font> 

Harmonický signál je reprezentovaný zmenou napätia alebo prúdu podľa vzťahu

$$
y(t) = A \cdot sin(\omega \, t + \phi)
$$


Informáciu je možné prenášať v harmonickom signáli zmenou niektorého z jeho parametrov - amplitúdy, frekvencie alebo fázy,

```{code-cell} ipython3  
:tags: ["remove-cell"]
from src.utils import *

data = r'''
scale=1.2 #2.54
arrowht=0.15
arrowwid=.1

include(lib_base.ckt)
include(lib_stm32.ckt)
include(lib_user.ckt)
include(lib_color.ckt)

right_;
move to (0,0);                              # "0" below;
#Grid(10,4);

color_black;
line -> from (-0.25,0) to (2*pi+0.5,0); "t" above ;
move to (0,0); 
color_blue;
sinusoid(1.0, 1, -pi/2, 0, 2*pi);
move to (0,0);
color_red;
sinusoid(1.0, 1, -1.5*pi/2, 0, 2*pi, dashed);

color_orange;
line from (0, 1) to (2*pi,1) dotted;
line from (0, -1) to (2*pi,-1) dotted;
line from (0, .707) to (2*pi, 0.707) dotted; color_black; #"$A_{RMS}$" at last line.start rjust;

color_black;
line -> from (0, -1.25) to (0,1.25); 
"y(t)" at last line.end+(0, 0.1);# rjust;
"A" at last line.center+(0,1) rjust;
"-A" at last line.center+(0,-1) rjust;

line -> from (1.35*pi, 0) to (1.35*pi, 0.707); 
"$A_{RMS}$" at last line.center ljust ;

line from (pi/2/1.95, 0.1) to (pi/2/1.95, -0.25) dashed; "$\phi$" at last line.end below;
line from (pi, 0.1) to (pi, -0.1); "$T/2$" at last line.end below;
line from (2*pi, 0.1) to (2*pi, -0.1); "$T$" at last line.start above;;
'''

_ = cm_compile('img_0072a', data,  dpi=600)   
```

```{figure} ./src/img_0072a.png
:width: 600px
:name: img_0072a

Parametre harmonického signálu.
```

Stredná hodnota

$$
A_{mean} = \frac{1}{T} \int_0^T y(t) dt
$$

Efektívna hodnota

$$
A_{RMS} = \sqrt{ \frac{1}{T} \int_0^T y(t)^2 dt }
$$



##  <font color='#547792'> Modulované signály  </font> 

### <font color='#E37434'> Amplitúdová modulácia </font>



```{figure} am_signal.png
:width: 500px
:name: sig_01

Amplitúdovo modulovaný signál.
```

### <font color='#E37434'> Frekvenčná modulácia </font>





