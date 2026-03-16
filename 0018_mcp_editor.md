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


# Externý editor


*MicroPython* môžeme pre jednoduché skripty používať s konzolovou aplikáciou v cykle *REPL*, pri komplikovanejších a väčších programoch nám tento spôsob nemusí vždy vyhovovať. S využitím pomocného programu *mpremote* môžeme v interpreteri spustiť skript vytvorený v lokálnom textovom editore príkazom z konzoly

        mpremote run <file.py>
        
Niektoré editory pre tvorbu kódu majú možnosť konfigurácie príkazov. Príkladom môže byť univerzálny multiplatformový editor [Geany](https://www.geany.org/), v ktorom vytvorený skript na obrázku stlačením klávesy `F9` presunieme a spustíme v interpreteri. Výstup programu sa zobrazí na konzole v spodnom okne editora. 


```{figure} ./img/geany_1.png
:width: 600px
:name: mp_0018a

Skript v editore *Geany*
```

V konfigurácii editora doplníme príkaz pre spustenie editovaného skriptu podľa obrázku

```{figure} ./img/geany_2.png
:width: 600px
:name: mp_0018b

Konfigurácia editora *Geany*
```
