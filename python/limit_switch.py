import lgpio
from time import *

"""
Gelb    =   NC
Schwarz =   Ground
Rot     =   NO
"""

NC = 24
NO = 25

count = 0
h = lgpio.gpiochip_open(0)

lgpio.gpio_claim_output(h, NC)
lgpio.gpio_claim_input(h, NO, lgpio.SET_PULL_UP)

lgpio.gpio_write(h,NC,1)

try:
    while True:
        print(f"Iteration: {count}\t|\tWert am Ausgang {lgpio.gpio_read(h,NO)}")
        sleep(.5)
        count += 1

finally: 
    lgpio.gpio_write(h,NC,0)
    lgpio.gpiochip_close(h)