from time import *
import lgpio
import numpy as np
from typing import Literal
from pydantic import Field, BaseModel
import matplotlib.pyplot as plt

class step_motor_conf(BaseModel):
    '''
    Mit dieser Klasse werden die Stepper-Motoren über ihre Einstellmöglichkeiten konfiguriert.
    Die Werte der Parameter können seperat eingesehen werden.
    '''

    PIN_ENA: int = Field(ge = 0, le = 26, default= 18)
    '''Der Enable Pin über dem auch die Pulsweitermodulation erfolgt.'''
    PIN_IN1: int = Field(ge = 0, le = 26, default= 22)
    '''Bei Aktivierung Vorwärtslauf.'''
    PIN_IN2: int = Field(ge = 0, le = 26, default= 23)
    '''Bei Aktivierung Rückwärtslauf.'''


class MotorDriver():
    '''
    Diese Klasse wird verwendet um die Stepper-Motoren zu initialisieren und sie anzusprechen.
    '''
    def __init__(self, config: step_motor_conf):
        '''Initialisierung der Klasse'''
        self.params = config
        self.h = lgpio.gpiochip_open(0)

        lgpio.gpio_claim_output(self.h, self.params.PIN_IN1)
        lgpio.gpio_claim_output(self.h, self.params.PIN_IN2)
        lgpio.gpio_claim_output(self.h, self.params.PIN_ENA)

    def set_direction(self, direction: str):
        """Setzt die Drehrichtung des Motors."""
        if direction == "forward":
            lgpio.gpio_write(self.h, self.params.PIN_IN1, 1)
            lgpio.gpio_write(self.h, self.params.PIN_IN2, 0)
        elif direction == "backward":
            lgpio.gpio_write(self.h, self.params.PIN_IN1, 0)
            lgpio.gpio_write(self.h, self.params.PIN_IN2, 1)
        elif direction == "stop":
            lgpio.gpio_write(self.h, self.params.PIN_IN1, 0)
            lgpio.gpio_write(self.h, self.params.PIN_IN2, 0)

    def auto_test(self):
        print("Start Autotest")

        self.set_direction("forward")

        for speed in range(100,-1,-1):
            lgpio.tx_pwm(self.h,self.params.PIN_ENA,1000,speed)
            print(f"Vorwärtslauf bei {speed}% der Geschwindigkeit")
            sleep(.5)

        sleep(.5)
        self.set_direction("stop")
        sleep(1)

        self.set_direction("backward")

        speed = 20

        for r in range(6):
            lgpio.tx_pwm(self.h,self.params.PIN_ENA,1000,speed*r)
            print(f"Rückwärtslauf bei {speed*r}% der Geschwindkeit")
            sleep(1)

        self.set_direction("stop")
        print("Ende Autotest")

    def self_test(self):
        '''Hier können eigene Werte eingegeben werden. Bei einer Eingabe für die Laufrichtung des Motors wird die Schleife abgebrochen.'''
        direction = input("forward/ backward?	")
        speed = .1
        while speed > 0:
            speed = int(input("Bitte die Geschwindigkeit in Prozent angeben: "))
            self.set_direction(direction)
            lgpio.tx_pwm(self.h,self.params.PIN_ENA,1000,speed)
        print("Stop")
        self.set_direction("stop")