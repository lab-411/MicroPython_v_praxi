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



# <font color='#4B9DA9'> Kondenzátor  </font>

```{code-cell} ipython3  
:tags: ["remove-cell"]
from src.utils import *

data = r'''
include(lib_base.ckt)
include(lib_stm32.ckt)
include(lib_user.ckt)

up_; 
Q1: capacitor(1.8,); llabel(,C,)
line right_ 1; 
C1:circle rad 0.08; "$+$" ljust; 
line <- from last line.end+(0.6,0) right_ 0.8; "$i(t)$" ljust;
line from Q1.start right_ 1; 
C2:circle rad 0.08; "$-$" ljust; 
line -> from C1.s+(0,-.1) to C2.n+(0,0.1); "$v(t)$" at last line.center ljust;
'''

_ = cm_compile('img_0034a', data,  dpi=600)   
```

```{figure} ./src/img_0034a.png
:width: 220px
:name: img_0034a

Prúd a napätie kondenzátorom.
```

Pre vzťah prúdu pretekajúcim kondenzátorom  a napätím na konzenzátore 

\begin{align*}
q =& C \cdot v \\
i =& \frac{dq}{dt} = C \frac{dv}{dt}
\end{align*}
