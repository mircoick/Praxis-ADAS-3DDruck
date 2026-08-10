import lgpio
from time import sleep

IN1, IN2, IN3, IN4 = 17, 27, 23, 24
EN = 4

step_sequence = [
    [1, 0, 0, 0],  # IN1
    [0, 0, 1, 0],  # IN3
    [0, 1, 0, 0],  # IN2
    [0, 0, 0, 1]   # IN4
]

# Die 4 Polungskombinationen
combinations = {
    "Variante A (Standard)": [17, 27, 23, 24],
    "Variante B (Spule A gedreht)": [27, 17, 23, 24],
    "Variante C (Spule B gedreht)": [17, 27, 24, 23],
    "Variante D (Beide gedreht)": [27, 17, 24, 23]
}

h = lgpio.gpiochip_open(0)

for pin in [17, 27, 23, 24, EN]:
    lgpio.gpio_claim_output(h, pin)
lgpio.gpio_write(h, EN, 1)

try:
    for name, engine in combinations.items():
        print(f"\nTeste: {name}")
        for _ in range(20):
            for step in step_sequence:
                for i in range(4):
                    lgpio.gpio_write(h, engine[i], step[i])
                sleep(0.03)
        sleep(0.5)

finally:
    for pin in [17, 27, 23, 24, EN]:
        lgpio.gpio_write(h, pin, 0)
    lgpio.gpiochip_close(h)
    print("\nTest beendet.")
