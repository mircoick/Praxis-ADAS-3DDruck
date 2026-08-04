from time import *
from lgpio import *

PIN_ENA = 18
PIN_IN1 = 22
PIN_IN2 = 23

h = gpiochip_open(0)



gpio_claim_output(h, PIN_IN1)
gpio_claim_output(h, PIN_IN2)
gpio_claim_output(h, PIN_ENA)

gpio_write(h, PIN_IN1, 1)
gpio_write(h, PIN_IN2, 0)


if input()==1:
    while True:
        tx_pwm(h,PIN_ENA,1000,int(input()))

else:
    print("Start")
    for speed in range(100,-1,-1):
        tx_pwm(h,PIN_ENA,1000,speed)
        print(f"Vorwärts: {speed}")
        sleep(.5)

    sleep(.5)
    gpio_write(h, PIN_IN1, 0)
    gpio_write(h, PIN_IN2, 0)
    sleep(1)

    gpio_write(h, PIN_IN1, 0)
    gpio_write(h, PIN_IN2, 1)

    speed = 20

    for r in range(6):
        tx_pwm(h,PIN_ENA,1000,speed*r)
        print(f"Rückwärts: {speed*r}")
        sleep(1)

    gpio_write(h, PIN_IN1, 0)
    gpio_write(h, PIN_IN2, 0)
    
    print("Ende")
