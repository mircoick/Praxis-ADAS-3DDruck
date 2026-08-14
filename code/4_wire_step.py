import lgpio
from time import *

def motor(engine,NC, direction="left", steps:int=1):
    step_sequence = [
                [1, 1, 0, 0],
                [0, 1, 1, 0],
                [0, 0, 1, 1],
                [1, 0, 0, 1]
            ]
    if direction == "right":
        step_sequence = step_sequence[::-1]
        if steps > 255:
            print("To many steps!")
            return
    print(f"Driving {direction}")
    for _ in range(steps):
        for step in step_sequence:
            for pin, state in zip(engine, step):
                if lgpio.gpio_read(h, NC) == 0 and direction is not "right":
                    print("Endposition!")
                    return
                lgpio.gpio_write(h, pin, state)        
            sleep(.005)



# GPIO-Pins für die Spulen (A+, B+, A-, B-)
engine = [4, 27, 17, 22]

# Pins des Endschalters
NO = 24
NC = 25

h = lgpio.gpiochip_open(0)

for pin in engine + [NO]:
    lgpio.gpio_claim_output(h, pin)

try:
    print("Starte Test!\n")
    start_time = time()
    lgpio.gpio_write(h, NO, 1)
    motor(engine,NC,"right",20)


finally:
    for pin in engine + [NO]:
        lgpio.gpio_write(h, pin, 0)
    lgpio.gpiochip_close(h)
    print("\nTest ended.")
