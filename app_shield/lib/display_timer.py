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


num_code = [0xC0,0xF9,0xA4,0xB0,0x99,0x92,0x82,0xF8,0x80,0x90]
num_pos  = [0xF1,0xF2,0xF4,0xF8]
num_disp = [1,2,3,4]

# chip select
pin = Pin('PB5', Pin.OUT)
spi = SPI(2, SPI.CONTROLLER, baudrate=100000, polarity=0, phase=0, crc=None)
tim = Timer(4)

tim.init(freq = 50)
pin.value(True)

# dynamicka obnova stavu displeja v preruseni casovaca
#tim.callback(update_display)
