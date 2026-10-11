'''
MicroPython kniznica pre riadenie modulu 7-segmentového displeja
----------------------------------------------------------------

Upravené s pouzitím nasledujucich zdrojov

zdroj:   MicroPython driver for MAX7219 with 7-segment modules
link:    https://github.com/JennaSys/micropython-max7219
autor:   John Sheehan
mail:    jennasyseng@gmail.com
licencia:MIT

zdroj:   Segmented LED Display - ASCII Library
link:    https://github.com/dmadison/LED-Segment-ASCII
autor:   Dave Madison
licencia:MIT


Pripojenie modulu ku kitu NUCLEO-64:

DIN  -> PB15   
CLK  -> PB13
CS   -> PB1
+5V
GND     
'''

from pyb import Pin, SPI
import time

# konfiguracia SPI
SPI_BUS = 2  
SPI_BAUDRATE = 100000
SPI_CS =  'PB1' # D3

# konfiguracia displeja
MAX7219_DIGITS = 8

MAX7219_REG_NOOP = 0x0
MAX7219_REG_DIGIT0 = 0x1
MAX7219_REG_DIGIT1 = 0x2
MAX7219_REG_DIGIT2 = 0x3
MAX7219_REG_DIGIT3 = 0x4
MAX7219_REG_DIGIT4 = 0x5
MAX7219_REG_DIGIT5 = 0x6
MAX7219_REG_DIGIT6 = 0x7
MAX7219_REG_DIGIT7 = 0x8
MAX7219_REG_DECODEMODE = 0x9
MAX7219_REG_INTENSITY = 0xA
MAX7219_REG_SCANLIMIT = 0xB
MAX7219_REG_SHUTDOWN = 0xC
MAX7219_REG_DISPLAYTEST = 0xF

# 7 Segment bit order: DP-G-F-E-D-C-B-A
char_map = {
    ' ': 0b00000000,
    '!': 0b10000110,
    '"': 0b00100010,
    '#': 0b01111110,
    '$': 0b01101101,
    '%': 0b11010010,
    '&': 0b01000110,
    "'": 0b00100000,
    '(': 0b00101001,
    ')': 0b00001011,
    '*': 0b00100001,
    '+': 0b01110000,
    ',': 0b00010000,
    '-': 0b01000000,
    '.': 0b10000000,
    '/': 0b01010010,
    '0': 0b00111111,
    '1': 0b00000110,
    '2': 0b01011011,
    '3': 0b01001111,
    '4': 0b01100110,
    '5': 0b01101101,
    '6': 0b01111101,
    '7': 0b00000111,
    '8': 0b01111111,
    '9': 0b01101111,
    ':': 0b00001001,
    ';': 0b00001101,
    '<': 0b01100001,
    '=': 0b01001000,
    '>': 0b01000011,
    '?': 0b11010011,
    '@': 0b01011111,
    'A': 0b01110111,
    'B': 0b01111100,
    'C': 0b00111001,
    'D': 0b01011110,
    'E': 0b01111001,
    'F': 0b01110001,
    'G': 0b00111101,
    'H': 0b01110110,
    'I': 0b00110000,
    'J': 0b00011110,
    'K': 0b01110101,
    'L': 0b00111000,
    'M': 0b00010101,
    'N': 0b00110111,
    'O': 0b00111111,
    'P': 0b01110011,
    'Q': 0b01101011,
    'R': 0b00110011,
    'S': 0b01101101,
    'T': 0b01111000,
    'U': 0b00111110,
    'V': 0b00111110,
    'W': 0b00101010,
    'X': 0b01110110,
    'Y': 0b01101110,
    'Z': 0b01011011,
    '[': 0b00111001,
    '\\': 0b01100100,
    ']': 0b00001111,
    '^': 0b00100011,
    '_': 0b00001000,
    '`': 0b00000010,
    'a': 0b01011111,
    'b': 0b01111100,
    'c': 0b01011000,
    'd': 0b01011110,
    'e': 0b01111011,
    'f': 0b01110001,
    'g': 0b01101111,
    'h': 0b01110100,
    'i': 0b00010000,
    'j': 0b00001100,
    'k': 0b01110101,
    'l': 0b00110000,
    'm': 0b00010100,
    'n': 0b01010100,
    'o': 0b01011100,
    'p': 0b01110011,
    'q': 0b01100111,
    'r': 0b01010000,
    's': 0b01101101,
    't': 0b01111000,
    'u': 0b00011100,
    'v': 0b00011100,
    'w': 0b00010100,
    'x': 0b01110110,
    'y': 0b01101110,
    'z': 0b01011011,
    '{': 0b01000110,
    '|': 0b00110000,
    '}': 0b01110000,
    '~': 0b00000001
}


def get_char(char):
    return char_map.get(str(char), char_map.get('_'))


def get_char2(char):
    # 7 Segment bit order: DP-A-B-C-D-E-F-G
    bits = get_char(char)
    tmp = '{:08b}'.format(bits)
    return int(''.join(['0b', tmp[0], ''.join(reversed(tmp[1:]))]), 2)
    
    

class SevenSegment:
    def __init__(self, digits=8, scan_digits=MAX7219_DIGITS, baudrate=SPI_BAUDRATE, cs=SPI_CS, spi_bus=SPI_BUS, reverse=False):
        """
        Constructor:
        `digits` should be the total number of individual digits being displayed
        `scan_digits` is the number of digits each individual max7219 displays
        `baudrate` defaults to 100KHz, note that excessive rates may result in instability (and is probably unnecessary)
        `cs` is the GPIO port to use for the chip select line of the SPI bus - defaults to GPIO 0 / D3
        `spi_bus` is the SPI bus on the controller to utilize - defaults to SPI bus 1
        `reverse` changes the write-order of characters for displays where digits are wired R-to-L instead of L-to-R
        """

        self.digits = digits
        self.devices = -(-digits // scan_digits)  # ceiling integer division
        self.scan_digits = scan_digits
        self.reverse = reverse
        self._buffer = [0] * digits
        #self._spi = SPI(spi_bus, baudrate=baudrate, polarity=0, phase=0)
        self._spi = SPI(spi_bus, SPI.CONTROLLER, baudrate=baudrate, polarity=0, phase=0, crc=None)
        self._cs = Pin(cs, Pin.OUT, value=1)

        self.command(MAX7219_REG_SCANLIMIT, scan_digits - 1)  # digits to display on each device  0-7
        self.command(MAX7219_REG_DECODEMODE, 0)   # use segments (not digits)
        self.command(MAX7219_REG_DISPLAYTEST, 0)  # no display test
        self.command(MAX7219_REG_SHUTDOWN, 1)     # not blanking mode
        self.brightness(7)                        # intensity: range: 0..15
        self.clear()

    def command(self, register, data):
        """Sets a specific register some data, replicated for all cascaded devices."""
        self._write([register, data] * self.devices)

    def _write(self, data):
        """Send the bytes (which should be comprised of alternating command, data values) over the SPI device."""
        self._cs.off()
        self._spi.write(bytes(data))
        self._cs.on()

    def clear(self, flush=True):
        """Clears the buffer and if specified, flushes the display."""
        self._buffer = [0] * self.digits
        if flush:
            self.flush()

    def flush(self):
        """For each digit, cascade out the contents of the buffer cells to the SPI device."""
        buffer = self._buffer.copy()
        if self.reverse:
            buffer.reverse()

        for dev in range(self.devices):
            if self.reverse:
                current_dev = self.devices - dev - 1
            else:
                current_dev = dev

            for pos in range(self.scan_digits):
                self._write([pos + MAX7219_REG_DIGIT0, buffer[pos + (current_dev * self.scan_digits)]] + ([MAX7219_REG_NOOP, 0] * dev))

    def brightness(self, intensity):
        """Sets the brightness level of all cascaded devices to the same intensity level, ranging from 0..15."""
        self.command(MAX7219_REG_INTENSITY, intensity)

    def letter(self, position, char, dot=False, flush=True):
        """Looks up the appropriate character representation for char and updates the buffer, flushes by default."""
        value = get_char2(char) | (dot << 7)
        self._buffer[position] = value

        if flush:
            self.flush()

    def text(self, text):
        """Outputs the text (as near as possible) on the specific device."""
        self.clear(False)
        text = text[:self.digits]  # make sure we don't overrun the buffer
        for pos, char in enumerate(text):
            self.letter(pos, char, flush=False)

        self.flush()

    def number(self, val):
        """Formats the value according to the parameters supplied, and displays it."""
        self.clear(False)
        strval = ''
        if isinstance(val, (int, float)):
            strval = str(val)
        elif isinstance(val, str):
            if val.replace('.', '', 1).strip().isdigit():
                strval = val

        if '.' in strval:
            strval = strval[:self.digits + 1]
        else:
            strval = strval[:self.digits]

        pos = 0
        for char in strval:
            dot = False
            if char == '.':
                continue
            else:
                if pos < len(strval) - 1:
                    if strval[pos + 1] == '.':
                        dot = True
                self.letter(pos, char, dot, False)
                pos += 1

        self.flush()

    def scroll(self, rotate=True, reverse=False, flush=True):
        """Shifts buffer contents left or right (reverse), with option to wrap around (rotate)."""
        if reverse:
            tmp = self._buffer.pop()
            if rotate:
                self._buffer.insert(0, tmp)
            else:
                self._buffer.insert(0, 0x00)
        else:
            tmp = self._buffer.pop(0)
            if rotate:
                self._buffer.append(tmp)
            else:
                self._buffer.append(0x00)

        if flush:
            self.flush()

    def message(self, text, delay=0.4):
        """Transitions the text message across the devices from left-to-right."""
        self.clear(False)
        for char in text:
            time.sleep(delay)
            self.scroll(rotate=False, flush=False)
            self.letter(self.digits - 1, char)
