import lgpio
from time import *

"""
Gelb    =   Signalgeber
Schwarz =   Ground
Rot     =   Ausgang
"""

count = 0
h = lgpio.gpiochip_open(0)

rein = lgpio.gpio_claim_output(h, 4)
raus = lgpio.gpio_claim_input(h, 17, lgpio.SET_PULL_UP)

lgpio.gpio_write(h,4,1)

try:
    while True:
        print(f"Iteration: {count}\t|\tWert am Ausgang {lgpio.gpio_read(h,17)}")
        sleep(.5)
        count += 1

finally: 
    lgpio.gpio_write(h,4,0)
    lgpio.gpiochip_close(h)