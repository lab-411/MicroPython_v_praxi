
# python pyboard.py -f cp lib_lsm6ds3.py :lib_lsm6ds3.py

from pyb import I2C
import time

import math
from lib.lib_lsm6ds3 import *

sensor = LSM6DS3(i2c, address=107, mode=PERFORMANCE_MODE_416HZ)

for i in range(10):
    ax, ay, az, gx, gy, gz = sensor.get_readings()
    print(ax, ay, az) #, gx, gy, gz, math.sqrt(ax**2 + ay**2 + az**2)*0.061)


for i in range(10):
    ax, ay, az, gx, gy, gz = sensor.get_readings()
    print(ax, ay, az, gx, gy, gz, math.sqrt(ax**2 + ay**2 + az**2)*0.061)

