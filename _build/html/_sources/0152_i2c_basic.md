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


#  <font color='#4B9DA9'> Vlastnosti </font>

I2C (Inter-Integrated Circuit) rozhranie je dvojvodičové obojsmerné synchrónne sériové periférne rozhranie (zbernica), primárne využívané v rámci vstavaných systémov pre komunikáciu na krátke vzdialenosti medzi riadiacimi mikrokontrolérmi a ostatnými integrovanými obvodmi resp. modulmi (EEPROM, A/D prevodníky, pamäťové karty, displeje, a pod.). Rozhranie bolo patentované firmou Philips v roku 1981 a prvá verzia špecifikácie bola vydaná v roku 1982.

Zbernica umožňuje, v závislosti od pripojených zariadení, komunikáciu prenosovými rýchlosťami od 100 kbps (standard mode) až po 5 Mbps (ultra-fast mode) a zariadenia sú adresované 7-bitovými (27 = 128 adries) prípadne 10-bitovými (210 = 1 024 adries) adresami.

```{figure} ./img/i2c_01.png
:width: 550px
:name: img_0201a

Zapojenie zariadení na zbernici *I2C*.
```

##  <font color='#547792'> Časovanie zbernice  </font>

```{figure} ./img/i2c_02.png
:width: 550px
:name: img_0201b

Časovani zebernice *I2C*.
```

