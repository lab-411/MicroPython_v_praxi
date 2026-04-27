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

# <font color='#4B9DA9'> LCD Display PCF8547T </font>

Štandardný LCD display s doplneným 8-bitovým paralelným prevodníkom pre I2C rozhranie s obvodom PCF8547T. Display je riadený v paralelnom 4-bitovom móde. 

```{figure} ./img/lcd_i2c_modul.jpg
:width: 400px
:name: mp_0207a

LCD Display s adaptérom PCF8547T 
```

##  <font color='#547792'> Komunikácia  </font> 

##  <font color='#547792'> Zapojenie  </font> 

```{figure} ./img/stm32_i2c.png
:width: 600px
:name: mp_0207b

Zapojenie displeja
```


##  <font color='#547792'> API </font> 

Základné funkcií pre obsluhu displeja.

    lcd_init(i2c)
    lcd_clear()
    lcd_set_cursor(i2c, row, column)
    lcd_write_string(i2c, text)
    

::: {dropdown} <font color='#84B179'> Implementácia knižnice </font>

```Python
I2C_ADDR = 0x27     # I2C address of the PCF8574
RS_BIT = 0          # Register select bit
EN_BIT = 2          # Enable bit
BL_BIT = 3          # Backlight bit
D4_BIT = 4          # Data 4 bit
D5_BIT = 5          # Data 5 bit
D6_BIT = 6          # Data 6 bit
D7_BIT = 7          # Data 7 bit

LCD_ROWS = 2        # Number of rows on the LCD
LCD_COLS = 16       # Number of columns on the LCD

BACKLIGHT = 1

def lcd_write_nibble(i2c, nibble, rs):
    data = nibble << D4_BIT
    data = data & 0xFF
    data |= rs    << RS_BIT
    data |= BACKLIGHT << BL_BIT   # Include backlight state in data
    data |= 1     << EN_BIT
    i2c.send(bytes([data]), I2C_ADDR)
    
    data &= ~(1 << EN_BIT)
    i2c.send(bytes([data]), I2C_ADDR)


def lcd_send_cmd(i2c, cmd):
    upper_nibble = cmd >> 4
    lower_nibble = cmd & 0x0F
    lcd_write_nibble(i2c, upper_nibble, 0)
    lcd_write_nibble(i2c, lower_nibble, 0)


def lcd_init(i2c):
    lcd_write_nibble(i2c, 0x03, 0)
    lcd_write_nibble(i2c, 0x03, 0)
    lcd_write_nibble(i2c, 0x03, 0)
    lcd_write_nibble(i2c, 0x02, 0)
    lcd_send_cmd(i2c, 0x28)
    lcd_send_cmd(i2c, 0x0C)
    lcd_send_cmd(i2c, 0x06)
    lcd_send_cmd(i2c, 0x01)


def lcd_send_data(i2c, data):
    '''
    Vyslanie 1 byte na displej
    '''
    data = data & 0xFF
    upper_nibble = data >> 4
    lower_nibble = data & 0x0F
    lcd_write_nibble(i2c, upper_nibble, 1)
    lcd_write_nibble(i2c, lower_nibble, 1)


def lcd_write_string(i2c, text):
    for i in text:
        lcd_send_data(i2c, ord(i))


def lcd_set_cursor(i2c, row, column):
    addr = 0
    if row == 0:
        addr = 0x00
    if row >= 1:
        addr = 0x40
    addr = addr + column
    lcd_send_cmd(i2c, 0x80 | addr)


def lcd_clear():
    lcd_send_cmd(i2c, 0x01)
```
:::



##  <font color='#547792'> Príklady </font> 


::: {dropdown} <font color='#84B179'> Príklad 1. Výpis textu </font>

```Python
from pyb import I2C
import time 
from lib.lib_lcd_pcf8547 import *

i2c = I2C(1, I2C.CONTROLLER, baudrate=100000)

# vypis pripojenych zariadeni pripojenych na zbernici
print(i2c.scan())
```

Zobrazenie textu

```Python
lcd_init(i2c)
time.sleep_ms(10)

lcd_set_cursor(i2c, 0,0)
lcd_write_string(i2c, 'Hello')
lcd_set_cursor(i2c, 1,0)
lcd_write_string(i2c, 'Clobrde')
```
:::
