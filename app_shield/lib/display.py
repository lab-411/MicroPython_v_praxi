from pyb import SPI, Pin, Timer
import time

def update_display(timer):
    for j in range(16):
        for i in range(4):
            c = num_disp[i]
            pin.value(False)
            spi.send(num_code[c])
            spi.send(num_pos[i])
            pin.value(True)

        # zhasnutie poslednej cislice v pauze, aby vsetky svietli rovnako
        pin.value(False)
        spi.send(0xFF)
        spi.send(0xF8)
        pin.value(True)


def display_int(x):
    # zobrazenie cisla 0...9999
    if x in range(0, 10000):
        global num_disp
        a = int(x/1000)
        b = int( (x-a*1000) / 100 )
        c = int( (x-a*1000-b*100)/10)
        d = int( (x-a*1000-b*100 - c*10))
        num_disp=[a,b,c,d]


