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



# <font color='#4B9DA9'> Vlastnosti signálov   </font>

##  <font color='#547792'> Harmonické signály  </font> 

##  <font color='#547792'> Modulované signály  </font> 

### <font color='#E37434'> Parametre </font>

```{code-cell} ipython3  
:tags: ["remove-cell"]
from numpy import *
import pylab as plt
plt.rcParams['figure.dpi'] = 80

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
plt.savefig('./img/amsignal.png', dpi=600)
```

```{figure} ./img/amsignal.png
:width: 500px
:name: sig_01

Amplitúdovo modulovaný signál.
```


##  <font color='#547792'> Diskrétne signály  </font> 


