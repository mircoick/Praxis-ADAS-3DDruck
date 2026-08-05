from time import *
from lgpio import *
import numpy as np
from typing import Literal
from pydantic import Field, BaseModel
import matplotlib.pyplot as plt

class step_motor():
    def __init__(self):
        pass

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
        self.h = gpiochip_open(0)

        self.gpio_claim_output(self.h, self.params.PIN_IN1)
        self.gpio_claim_output(self.h, self.params.PIN_IN2)
        self.gpio_claim_output(self.h, self.params.PIN_ENA)

    def set_direction(self, direction: str):
        """Setzt die Drehrichtung des Motors."""
        if direction == "forward":
            gpio_write(self.h, self.params.PIN_IN1, 1)
            gpio_write(self.h, self.params.PIN_IN2, 0)
        elif direction == "backward":
            gpio_write(self.h, self.params.PIN_IN1, 0)
            gpio_write(self.h, self.params.PIN_IN2, 1)
        elif direction == "stop" or direction == None:
            gpio_write(self.h, self.params.PIN_IN1, 0)
            gpio_write(self.h, self.params.PIN_IN2, 0)

    def auto_test(self):
        print("Start Autotest")

        self.set_direction("forwart")

        for speed in range(100,-1,-1):
            tx_pwm(self.h,self.PIN_ENA,1000,speed)
            print(f"Vorwärtslauf bei {speed}% der Geschwindigkeit")
            sleep(.5)

        sleep(.5)
        self.set_direction()
        sleep(1)

        self.set_direction("backward")

        speed = 20

        for r in range(6):
            tx_pwm(self.h,self.PIN_ENA,1000,speed*r)
            print(f"Rückwärtslauf bei {speed*r}% der Geschwindkeit")
            sleep(1)

        self.set_direction("stop")
        print("Ende Autotest")

    def self_test(self, direction: str, speed: int):
        '''Hier können eigene Werte eingegeben werden. Bei einer Eingabe für die Laufrichtung des Motors wird die Schleife abgebrochen.'''
        direction = 1
        while direction != None:
            direction = input("Bitte die Laufrichtung angeben")
            speed = input("Bitte die Geschwindigkeit in Prozent angeben")
            self.set_direction(direction)
            tx_pwm(self.h,self.PIN_ENA,1000,speed)      

        self.set_direction("stop")