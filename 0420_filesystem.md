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


#  Súborový systém

Pri MCU s väčšou pamäťou sa ako súborový systém využíva pamäť FLASH. Súbory uložené sa po resete procesora nemažú.

##  Lokálna správa filesystému 

Použitie knižnice **os** v interaktívnom móde MicroPython-u.

```Python
import os

dir(os)                   # vypis funkcii kniznice os
os.getcwd()               # vypis aktualneho adesaru
os.listdir()              # vypis adresarov
os.mkdir('path')          # vytvorenie adresaru
os.chdir('path')          # zmena adresaru
os.unlink('filename')     # zmazanie suboru alebo symbolickeho linku
os.rmdir('path')          # zmazanie prazdneho adresaru
```

Zmazanie všetkých súborov v adresári

```Python
os.chdir('path') 
w=os.listdir()
for i in w: os.unlink(i)
```

##   Diaľková správa filesystému 

Z konzoly počítača môžeme cez CLI pristupovať k súborovému systému MicroPython-u pomocou programu [pyboard.py](./lib/pyboard.py). 

    python pyboard.py -h
    usage: pyboard.py [-h] [-d DEVICE] [-b BAUDRATE] [-u USER] [-p PASSWORD] [-c COMMAND] [-w WAIT]
                      [--soft-reset | --no-soft-reset] [--follow | --no-follow] [--exclusive |
                      --no-exclusive] [-f]
                      [files ...]

    Run scripts on the pyboard.

    positional arguments:
      files                 input files

    options:
      -h, --help            show this help message and exit
      -d, --device DEVICE   the serial device or the IP address of the pyboard
      -b, --baudrate BAUDRATE
                            the baud rate of the serial device
      -u, --user USER       the telnet login username
      -p, --password PASSWORD
                            the telnet login password
      -c, --command COMMAND
                            program passed in as string
      -w, --wait WAIT       seconds to wait for USB connected board to become available
      --soft-reset          Whether to perform a soft reset when connecting to the board [default]
      --no-soft-reset
      --follow              follow the output after running the scripts [default if no scripts given]
      --no-follow
      --exclusive           Open the serial device for exclusive access [default]
      --no-exclusive
      -f, --filesystem      perform a filesystem action: cp local :device | cp :device local | cat path | ls
                            [path] | rm path | mkdir path | rmdir path

Vytvorenie adresáru

    python ./py/pyboard.py -d PORT -f mkdir PATH

Nahratie súboru

    python ./py/pyboard.py -d PORT LOKALNY_SUBOR :REMOTE_SUBOR




##  Jupyteru Notebook

Nahratie súboru do pamäte FLASH z prostredia Jupyteru. Pri použití kernelu MicroPython-u je potrebné vytvoriť bunku, ktorú interpretuje lokálny kernel *ipython*. 

```Python
# prepinac pre bunku v lokalnom mode - interpretuje lokalny ipython 
%local

import os
port = '/dev/ttyACM0'

# vytvorenie remote adresaru
_ = os.system('python ./py/pyboard.py -d '+port+' -f mkdir lib')

# nahravany subor je mozne ulozit do vopred vytvoreneho remote adresaru
# _ = os.system('python ./py/pyboard.py -d PORT LOKALNY_SUBOR :REMOTE_SUBOR')
_ = os.system('python ./py/pyboard.py -d '+port+' -f cp ./subor.py :./lib/subor.py')

```
