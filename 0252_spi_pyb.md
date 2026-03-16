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


# Knižnica pyb.SPI 

Knižnica *pyb* obsahuje pre obsluhu sériového rozhrania triedu [SPI](https://docs.micropython.org/en/latest/library/pyb.SPI.html). Signál NSS pre výber **nie** je v knižnici *pyb* štandardne aktivovaný, je potrebné ho ovládať samostatne prostredníctvom triedy *pyb.Pin*.

```{admonition} Poznámka

Rozhranie SPI1 na doske NUCLE-64 nie je štabdardne pripojené ku pinom konektora Arduino-UNO.   
Pomocou funkcie alternatívnych pinov možeme pripojenie rozhrania rekonfigurovať.

    >>> p=Pin('PA7')
    >>> p.af_list()
    [Pin.AF1_TIM1, Pin.AF2_TIM3, Pin.AF3_TIM8, Pin.AF5_SPI1, Pin.AF14_TIM17]
    pp = Pin('PA7', mode=Pin.ALT, alt=Pin.AF5_SPI1)
```


## Inicializácia

    SPI.init(mode, baudrate=328125, *, prescaler=-1, 
                   polarity=1, phase=0, bits=8, firstbit=SPI.MSB, 
                   ti=False, crc=None)
    SPI.deinit()

    mode
        SPI.CONTROLLER
        SPI.PERIPHERAL

    firstbit
        SPI.LSB
        SPI.MSB

## Funkcie

    SPI.recv(recv, *, timeout=5000)
    SPI.send(send, *, timeout=5000)
    SPI.send_recv(send, recv=None, *, timeout=5000)


## Príklad použitia

```Python
from pyb import SPI

# inicializacia
pin = Pin('PB1', Pin.OUT)
spi = SPI(2, SPI.CONTROLLER, baudrate=100000, polarity=0, phase=0, crc=None)

# vyslanie jedneho byte
pin.value(False)
spi.send(0x12)
pin.value(True)
            
```
TODO - prepojenie MCU v móde MASTER-SLAVE
