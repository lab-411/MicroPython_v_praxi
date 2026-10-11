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

%#   <font color='#4B9DA9'>  Nazov </font>
%##  <font color='#547792'> Popis </font>
%##  <font color='#547792'> Zapojenie </font>
%##  <font color='#547792'> Programovanie </font>
%### <font color='#E37434'> Knižnica </font>
%### <font color='#E37434'> API </font>
%### <font color='#E37434'> Príklady </font>



# <font color='#4B9DA9'>  LCD Display 12864  </font>

##  <font color='#547792'> Popis </font>

LCD 12684 je univerzálny grafický displej s rozlíšením 128x64 pixlov a je široko využívaný v rôznych priemyselných aplikáciách. Napájanie modulu je 5V a obsahuje integrovaný radič ST7920. Modul je možné k mikrokontroléru pripojiť prostredníctvom paralelného 8/4 rozhrania alebo pomocou sériového SPI rozhrania. Každý pixel je možné ovládať samostatne, modul obsahuje vlastné znakové sady. 


```{figure} ./img/lcd_st7520_1.png
:width: 400px
:name: mp_0257c

Displej QC12864.
```

##  <font color='#547792'> Zapojenie </font>

**Vývody displeja**

    GND     - Ground
    VCC     - Module power supply +5V
    VO      - LCD Contrast
    RS      - Register Select Pin    / SPI  CS   serial select 
    R/W     - Write/ Read selection  / SPI MOSI  serial data
    E       - Enable Signal          / SPI SCK   serial clock
    D0...D7 - Data Bus
    PSB     - Interface selection 
                0 for serial communication
                1 for 8/4-bit parallel communication
    NC      - Not Connected
    RST     - Reset
    Vout    - LCD Voltage Output (Vout < 7V)
    BLA     - Power Supply for Backlight+  +5V
    BLK     - Power Supply for Backlight-  GND

##  <font color='#547792'> Programovanie </font>

### <font color='#E37434'> Knižnica </font>

Pre obsluhu displeja je vytvorená knižnica [lib_lcd12864_spi](./lib/lib_lcd12864_spi.py). Pre vykreslenie na displeji je použitý modul [framebuf]( https://docs.micropython.org/en/latest/library/framebuf.html#module-framebuf). 

### <font color='#E37434'> API </font>

**Konštruktor**

    LCD12864_SPI(spi, cs_pin, rst_pin, rotation)

**Metódy**

    clear()                           - Clear display
    set_font(font)                    - Set font for text
    set_text_wrap(on)                 - Set text wrapping
    draw_text(text, x, y, color)      - Draw text on display
    draw_bitmap(bitmap, x, y, color)  - Draw a bitmap on display
    show()                            - Send frameBuffer to lcd
    

Pre riadenie displeja je potrebné inicializovať SPI rozhranie a definovať pin CS (chip select). 
    
    from pyb import SPI
    from lib.lcd12864_spi import *
    spi = SPI(2, SPI.CONTROLLER, baudrate=100000, polarity=1, phase=1, crc=None)
    lcd = LCD12864_SPI( spi = spi, cs_pin = 'D6', rst_pin = 'D2', rotation = 1 )

### <font color='#E37434'> Príklady </font>

````{dropdown} <font color='#84B179'>  Použitie príkazov z modulu framebuf </font>


```{code-block} Python
from pyb import SPI
from lib.lcd12864_spi import *
spi = SPI(2, SPI.CONTROLLER, baudrate=100000, polarity=1, phase=1, crc=None)
lcd = LCD12864_SPI( spi = spi, cs_pin = 'D6', rst_pin = 'D2', rotation = 1 )

lcd.text( "123.456", 50, 25, 1 )
lcd.rect( 0, 0, 128, 64, 1 )
lcd.rect( 3, 3, 128-6, 64-6, 1 )
lcd.line(0,0,20,30,1)
lcd.ellipse(30,30,15,15,1)
lcd.show()
```

````
    

##  <font color='#547792'> Odkazy a literatúra </font>
    
* [Knižnica](https://github.com/mchobby/esp8266-upy/blob/master/lcdspi-lcd12864/readme_ENG.md)
    
    
  
