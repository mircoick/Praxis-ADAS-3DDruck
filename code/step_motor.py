from time import *
import lgpio
import numpy as np
from typing import Literal
from pydantic import Field, BaseModel
import matplotlib.pyplot as plt
import pybresenham
from pygcode import Line
import pandas as pd

class MotorDriverConf(BaseModel):
    '''
    Mit dieser Klasse werden die Stepper-Motoren über ihre Einstellmöglichkeiten konfiguriert.
    Die Werte der Parameter können seperat eingesehen werden.
    '''

    PIN_ENA_EN1: int = Field(ge = 0, le = 27, default= 18)
    '''Der Enable Pin über dem auch die Pulsweitermodulation erfolgt von Motor 1.'''
    PIN_IN1_EN1: int = Field(ge = 0, le = 27, default= 22)
    '''Bei Aktivierung Vorwärtslauf Motor 1.'''
    PIN_IN2_EN1: int = Field(ge = 0, le = 27, default= 23)
    '''Bei Aktivierung Rückwärtslauf Motor 1.'''
    
    PIN_ENA_EN2: int = Field(ge = 0, le = 27, default= 19)
    '''Der Enable Pin über dem auch die Pulsweitermodulation erfolgt von Motor 2.'''
    PIN_IN1_EN2: int = Field(ge = 0, le = 27, default= 17)
    '''Bei Aktivierung Vorwärtslauf Motor 2.'''
    PIN_IN2_EN2: int = Field(ge = 0, le = 27, default= 27)
    '''Bei Aktivierung Rückwärtslauf Motor 2.'''


class MotorDriver():
    '''
    Diese Klasse wird verwendet um die Stepper-Motoren zu initialisieren und sie anzusprechen.
    '''
    def __init__(self, config: MotorDriverConf):
        '''Initialisierung der Klasse'''
        self.params = config
        self.h = lgpio.gpiochip_open(0)
        self.motors = {
            "motor1": {
                "en": self.params.PIN_ENA_EN1,
                "in1": self.params.PIN_IN1_EN1,
                "in2": self.params.PIN_IN2_EN1
            },
            "motor2": {
                "en": self.params.PIN_ENA_EN2,
                "in1": self.params.PIN_IN1_EN2,
                "in2": self.params.PIN_IN2_EN2
            }
        }

        for motor_name, pins in self.motors.items():
            lgpio.gpio_claim_output(self.h, pins["en"])
            lgpio.gpio_claim_output(self.h, pins["in1"])
            lgpio.gpio_claim_output(self.h, pins["in2"])
            
        for motor_name, pins in self.motors.items():
            lgpio.gpio_write(self.h, pins["en"],0)
            lgpio.gpio_write(self.h, pins["in1"],0)
            lgpio.gpio_write(self.h, pins["in2"],0)

    def read_gcode(self, filepath:str):
        rows = []
        with open("data/overhang test.gcode") as f:
            for text in f:
                line = Line(text)

                row = {}

                if line.block.gcodes:
                    row["cmd"] = str(line.block.gcodes[0])

                for word in line.block.words:
                    row[word.letter] = word.value

                rows.append(row)

        self.df = pd.DataFrame(rows)

    def set_direction(self, direction: str, motor: str):
        """Setzt die Drehrichtung des wählbaren Motors."""
        if motor not in self.motors:
            print(f"Fehler: {motor} existiert nicht.")
            return
        
        pins = self.motors[motor]

        if direction == "forward":
            lgpio.gpio_write(self.h, pins["in1"], 1)
            lgpio.gpio_write(self.h, pins["in2"], 0)
        elif direction == "backward":
            lgpio.gpio_write(self.h, pins["in1"], 0)
            lgpio.gpio_write(self.h, pins["in2"], 1)
        elif direction == "stop":
            lgpio.gpio_write(self.h, pins["in1"], 0)
            lgpio.gpio_write(self.h, pins["in2"], 0)

    def stop(self):
        for motor_name in self.motors.items():
            self.set_direction("stop",motor_name)
        
    def pwm_test(self):
        '''Hier können eigene Werte eingegeben werden. Bei einer Eingabe für die Laufrichtung des Motors wird die Schleife abgebrochen.'''
        direction = input("forward/ backward:	")
        motor = input("motor1/ motor2:	")
        speed = .1
        pins = self.motors[motor]
        while speed > 0:
            speed = int(input("Bitte die Geschwindigkeit in Prozent angeben: "))
            self.set_direction(direction,motor)
            lgpio.tx_pwm(self.h,pins["en"],1000,speed)
        print("Stop")
        self.set_direction("stop",motor)

    def start_pos(self,x0,y0,sec):
        print("\nInitialisierung X (Startposition x=0):")
        if x0 > 0:
            for i in range(0,x0):
                self.step_impulse("forward",.5,"motor1")
                sleep(sec)
                print(f"i motor1 vorwärts",i+1,x0)
            self.x_old = x0
            
        elif x0 < 0:
            for i in range(0,x0,-1):
                self.step_impulse("backward",.5,"motor1")
                sleep(sec)
                print("i motor1 Rückwärts",i-1,x0)
            self.x_old = x0
        
        else:
            self.x_old = x0
        print(f"\nEnde Initialisierung x = {self.x_old,self.y_old}\n")
            
        print("Initialisierung Y (Startposition y=0):")
        if y0 > 0:
            for i in range(0,y0):
                self.step_impulse("forward",.5,"motor2")
                sleep(sec)
                print("i motor2 vorwärts",i+1,y0)
            self.y_old = y0
            
        elif y0 < 0:
            for i in range(0,y0,-1):
                self.step_impulse("backward",.5,"motor2")
                sleep(sec)
                print("i motor2 Rückwärts",i-1,y0)
            self.y_old = y0
        else:
            self.y_old = y0
            
        print(f"\nEnde Initialisierung y = {self.x_old,self.y_old}\n")
        
    def step_impulse(self, direction:str,impulse: int,motor:str):
        '''Ein Step Impulse der mit der Zeitangabe gesteuert werden kann.'''
        if motor not in self.motors:
            print(f"Fehler: {motor} existiert nicht.")
            return
        
        self.set_direction(direction,motor)
        
        pins = self.motors[motor]
        lgpio.tx_pwm(self.h,pins["en"],1000,100)
        sleep(impulse/1e6)
        lgpio.tx_pwm(self.h,pins["en"],1000,0)
        
    def step_double_impulse(self,dir1,dir2,impulse):
        '''Ein DoppelterStep Impulse der mit der Zeitangabe gesteuert werden kann.'''
        self.set_direction(dir1,"motor1")
        self.set_direction(dir2,"motor2")
        
        p1 = self.motors["motor1"]
        p2 = self.motors["motor2"]
        
        lgpio.tx_pwm(self.h,p1["en"],1000,100)
        lgpio.tx_pwm(self.h,p2["en"],1000,100)
        
        sleep(impulse/1e6)
        
        lgpio.tx_pwm(self.h,p1["en"],1000,0)
        lgpio.tx_pwm(self.h,p2["en"],1000,0)
        
    def bresenham_step(self,x0:int,y0:int,x1:int,y1:int,sec):
        steps = list(pybresenham.line(x0,y0,x1,y1))
        print(steps)
        self.x_old = None
        self.y_old = None
        s=0
        self.start_pos(x0,y0,sec)
        for x,y in steps:
            
            dir1 = None
            dir2 = None
            
            if x > self.x_old:
                dir1 = "forward"
            elif x < self.x_old:
                dir1 = "backward"
            if y > self.y_old:
                dir2 = "forward"
            elif y < self.y_old:
                dir2 = "backward"
                
            if dir1 and dir2:
                self.step_double_impulse(dir1,dir2,.5)
                self.x_old = x
                self.y_old = y
                print("Doppelschritt x/y ",dir1,dir2,self.x_old,self.y_old)
            elif dir1:
                self.step_impulse(dir1,.5,"motor1")
                self.x_old = x
                print("Einzelschritt x ",dir1,self.x_old,self.y_old)
            elif dir2:
                self.step_impulse(dir2,.5,"motor2")
                self.y_old = y
                print("Einzelschritt y ",dir2,self.x_old,self.y_old)        

            print(f"\nNächster Gesamtschritt {x,y}\t{steps[s]}")
            s=s+1
            
        print("\nENDE")
        
        