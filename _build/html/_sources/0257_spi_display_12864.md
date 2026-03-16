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



# <font color='#4B9DA9'>  LCD Display 12864  </font>

Grafický LCD display [QC12864](./doc/QC12864B.pdf) s rozlíšením 128x64 pixlov je možné riadiť pomocou paralelného alebo sériového SPI rozhrania.

```{figure} ./img/lcd_st7520_1.png
:width: 400px
:name: mp_0257c

Displej QC12864.
```

## <font color='#547792'> Popis </font>

### <font color='#E37434'> Označenie vývodov </font>

    GND     Ground
    VCC     Module power supply – 5 V
    VO      LCD Contrast
    RS      Register Select Pin
    R/W     Write/ Read selection
    E       Enable Signal
    D0...D7 Data Bus
    PSB     Interface selection 
                0 for serial communication
                1 for 8-bit parallel communication
    NC      Not Connected
    RST     Reset
    Vout    LCD Voltage Output (Vout < 7V)
    BLA     Power Supply for Backlight+
    BLK     Power Supply for Backlight-

##  <font color='#547792'> Programovanie </font>

:::{dropdown} <font color='#84B179'>  Zdrojový kód knižnice </font>
```{literalinclude} ./lib/lib_lcd12864_spi.py
:lineno-start: 1
```
:::

API Funkcie

    clear( self ): - Clear display
    set_font(self, font): - Set font for text
    set_text_wrap(self, on = True): - Set text wrapping
    draw_text(self, text, x, y, color = 1): - Draw text on display
    draw_bitmap(self, bitmap, x, y, color = 1): - Draw a bitmap on display
    show( self ): - Send frameBuffer to lcd
    other framebuffer functions - 
    see more on https://docs.micropython.org/en/latest/library/framebuf.html#module-framebuf


Demo program  

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

