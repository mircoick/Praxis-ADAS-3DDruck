import time
from smbus2 import SMBus
from math import cos, sin, sqrt

MAX30102_ADDR = 0x57

REG_INTR_STATUS_1 = 0x00
REG_INTR_STATUS_2 = 0x01
REG_INTR_ENABLE_1 = 0x02
REG_INTR_ENABLE_2 = 0x03
REG_FIFO_WR_PTR = 0x04
REG_OVF_COUNTER = 0x05
REG_FIFO_RD_PTR = 0x06
REG_FIFO_DATA = 0x07
REG_FIFO_CONFIG = 0x08
REG_MODE_CONFIG = 0x09
REG_SPO2_CONFIG = 0x0A
REG_LED1_PA = 0x0C
REG_LED2_PA = 0x0D

bus = SMBus(1)


def write_reg(reg, value):
    bus.write_byte_data(MAX30102_ADDR, reg, value)


def read_bytes(reg, nbytes):
    return bus.read_i2c_block_data(MAX30102_ADDR, reg, nbytes)


def max30102_init():
    write_reg(REG_MODE_CONFIG, 0x40)
    time.sleep(0.1)
    write_reg(REG_INTR_ENABLE_1, 0x40)
    write_reg(REG_INTR_ENABLE_2, 0x00)
    write_reg(REG_FIFO_WR_PTR, 0x00)
    write_reg(REG_OVF_COUNTER, 0x00)
    write_reg(REG_FIFO_RD_PTR, 0x00)
    write_reg(REG_FIFO_CONFIG, 0x0F)
    write_reg(REG_SPO2_CONFIG, 0x20)
    write_reg(REG_LED1_PA, 0x2F)
    write_reg(REG_LED2_PA, 0x2F)
    write_reg(REG_MODE_CONFIG, 0x03)
    print("MAX30102 initialized.")


def read_raw_sample():
    data = read_bytes(REG_FIFO_DATA, 6)
    red = (data[0] << 16 | data[1] << 8 | data[2]) & 0x000FFF
    ir = (data[3] << 16 | data[4] << 8 | data[5]) & 0x000FFF
    return red, ir


def ft(a, i):
    n = len(a)
    pi = 3.14
    re = 0.0
    im = 0.0
    for j in range(n):
        re = re + cos(2 * pi * i * j / n) * a[j]
        im = im + sin(2 * pi * i * j / n) * a[j]
    return sqrt(re**2 + im**2)


max30102_init()
time_sleep = 0.05
time_record = 10
dfr = 1 / time_record
ifmin = int(0.7 * time_record)
ifmax = int(3.4 * time_record)
t = 0.0
i = 0
a = []

while t < time_record:
    t = t + time_sleep
    a.append(0)
a.append(0)
t = 0.0

while True:
    read_bytes(REG_INTR_STATUS_1, 1)
    red, ir = read_raw_sample()
    t = t + time_sleep
    a[i] = ir
    i = i + 1

    if t > time_record:
        t = 0.0
        i = 0
        fmax = 0.0
        imax = 0
        for j in range(ifmin, ifmax):
            fr = ft(a, j)
            if fr > fmax:
                fmax = fr
                imax = j
        bps = dfr * imax
        bpm = 60 * bps
        print(bpm)
        time.sleep(1)

    time.sleep(time_sleep)