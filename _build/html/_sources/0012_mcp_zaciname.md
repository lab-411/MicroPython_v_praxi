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

# Ako na to 

MicroPython je vo svojej podstate zjednodušený interpreter programovacieho jazyka Python upravený pre použitie v mikrokontroléri. Interpreter je doplnený knižnicami, ktoré umožňujú prácu s perifériami implementovanými v mikrokontroléri. Pre zadávanie príkazov interpreteru využijeme štandardná počítač, pomocou ktorého odošleme príkaz mikrokontroléru, tento príkaz spracuje a odozvu pošle nazad, tento postup je vo všeobecnosti označovaný ako cyklus **REPL** (Read–eval–print loop). 

Pre prácu s MicroPython interpreterom preto potrebujeme  

* naprogramovaný mikrokontrolér zvyčajne umiestnený na niektorom z výukových kitov, [Ako na to ?](0900_instalacia.md)
* vhodný komunikačný program, [Ako na to ?](0900_instalacia.md)



```{figure} ./img/konzola.png
:width: 600px
:name: mp_0010a

Terminálový program *picocom* komunikujúci s interpreterom MicroPython v cykle *REPL*.
```

Pre pokročilejšiu prácu s interpreterom a zadávanie dlhších skriptov a programov môžeme využiť externé programátorské editory ktorých použitie a konfigurácia je popísaná v kapitole [Externý editor](0017_mcp_editor.md). 





