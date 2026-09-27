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

# <font color='#4B9DA9'> Ako na to  </font>

MicroPython je vo svojej podstate zjednodušený interpreter programovacieho jazyka Python upravený pre použitie v mikrokontroléri. Interpreter je doplnený knižnicami, ktoré umožňujú prácu s perifériami implementovanými v mikrokontroléri. Pre zadávanie príkazov interpreteru využijeme štandardná počítač, pomocou ktorého odošleme príkaz mikrokontroléru, tento príkaz spracuje a odozvu pošle nazad, tento postup je vo všeobecnosti označovaný ako cyklus **REPL** (Read–Eval–Print-Loop). 

Pre prácu s MicroPython interpreterom preto potrebujeme  

* naprogramovaný mikrokontrolér zvyčajne umiestnený na niektorom z výukových kitov, [Ako na to ?]
* vhodný komunikačný program, [Ako na to ?]


##  <font color='#547792'> Inštalácia </font>

**TODO** popis inštalácie

* Kit, kód, programovanie
* komunikačný program

##  <font color='#547792'> Test inštalácie </font>

**TODO** popis príkazov terminálu

```{figure} ./img/konzola.png
:width: 600px
:name: mp_0012a

Terminálový program *picocom* komunikujúci s interpreterom MicroPython v cykle *REPL*.
```

Pre pokročilejšiu prácu s interpreterom a zadávanie dlhších skriptov a programov môžeme využiť externé programátorské editory ktorých použitie a konfigurácia je popísaná v kapitole [Externý editor](0716_editor.md). 





