import time

# LSM303AGR - Magnetometer

ADDRESS_MAG      = const(0x1E)  # (0x3C >> 1) 
MAG_DEVICE_ID    = 0b01000000

MAG_RATE_10_HZ   = const(0x00)
MAG_RATE_20_HZ   = const(0x01)
MAG_RATE_50_HZ   = const(0x02)
MAG_RATE_100_HZ  = const(0x03)

# Magnetometer registers
OFFSET_X_REG_L    = 0x45
OFFSET_X_REG_H    = 0x46
OFFSET_Y_REG_L    = 0x47
OFFSET_Y_REG_H    = 0x48
OFFSET_Z_REG_L    = 0x49
OFFSET_Z_REG_H    = 0x4A
WHO_AM_I          = 0x4F
CFG_REG_A         = 0x60
CFG_REG_B         = 0x61
CFG_REG_C         = 0x62
INT_CRTL_REG      = 0x63
INT_SOURCE_REG    = 0x64
INT_THS_L_REG     = 0x65
STATUS_REG        = 0x67
OUTX_L_REG        = 0x68
OUTX_H_REG        = 0x69
OUTY_L_REG        = 0x6A
OUTY_H_REG        = 0x6B
OUTZ_L_REG        = 0x6C
OUTZ_H_REG        = 0x6D
MAG_SCALE         = 0.15 # 1.5 milligauss/LSB * 0.1 microtesla/milligauss


class LSM303AGR_MAG:
    '''
    Minimalna verzia 
    '''

    def __init__(self, i2c):
        self.i2c = i2c  #I2CDevice(i2c, _ADDRESS_MAG)
        self.addr = ADDRESS_MAG
        
        self.setreg(CFG_REG_A, 0x20)
        time.sleep(0.1) 
        
        self.device_id     = self.getreg(WHO_AM_I)

        if self.device_id != 0x40:
            raise AttributeError("Cannot find an LSM303AGR")
            
        self.setreg(CFG_REG_A, 0x8C)
        self.setreg(CFG_REG_B, 0x02)
        self.setreg(CFG_REG_C, 0x10)
        time.sleep(.02)

        
    def setreg(self, reg, data):
        self.i2c.mem_write(data, self.addr, reg)
    
        
    def getreg(self, reg):
        data = bytearray(1)
        self.i2c.mem_read(data, self.addr, reg)
        return data[0]
        
        
    def raw_x(self):
        x = (self.getreg(OUTX_H_REG)*256) +  self.getreg(OUTX_L_REG)
        if(x & 0x8000) > 0:
            x = (x & 0x7FFF) - 32768
        return x
        
        
    def raw_y(self):
        y = (self.getreg(OUTY_H_REG)*256) +  self.getreg(OUTY_L_REG)
        if(y & 0x8000) > 0:
            y = (y & 0x7FFF) - 32768
        return y
        
        
    def raw_z(self):
        z =  (self.getreg(OUTZ_H_REG)*256) +  self.getreg(OUTZ_L_REG)
        if(z & 0x8000) > 0:
            z = (z & 0x7FFF) - 32768
        return z
        

    def magnetic(self):
        """The processed magnetometer sensor values.
        A 3-tuple of X, Y, Z axis values in microteslas that are signed floats.
        """
        
        return (self.raw_x() * MAG_SCALE, self.raw_y() * MAG_SCALE, self.raw_z() * MAG_SCALE)
    
