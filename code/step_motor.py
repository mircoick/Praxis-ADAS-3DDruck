from time import *
import lgpio
import numpy as np
from typing import Literal
from pydantic import Field, BaseModel
import matplotlib.pyplot as plt
import pybresenham
from pygcode import Line
import pandas as pd
from itertools import zip_longest

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
        with open(filepath) as f:
            for text in f:
                line = Line(text)

                row = {}

                if line.block.gcodes:
                    row["cmd"] = str(line.block.gcodes[0])

                for word in line.block.words:
                    row[word.letter] = word.value

                rows.append(row)

        self.df = pd.DataFrame(rows)
        #self.df.fillna(method='ffill')
        #self.df.to_csv(filepath[:-5]+"csv")
        
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
        elif direction == "stop" or direction is None:
            lgpio.gpio_write(self.h, pins["in1"], 0)
            lgpio.gpio_write(self.h, pins["in2"], 0)

    def stop(self):
        for motor_name, pins in self.motors.items():
            self.set_direction("stop",motor_name)
        print("Stop")
            
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

    def start_pos(self,x0,y0,impulse):
        print(f"\nInitialisierung: x = 0, y = 0 => {x0,y0}")
        steps = list(pybresenham.line(0,0,x0,y0))
        x_int = 0
        y_int = 0
        for x,y in steps:
            
            dir1 = None
            dir2 = None
            
            if x > x_int:
                dir1 = "forward"
            elif x < x_int:
                dir1 = "backward"
            if y > y_int:
                dir2 = "forward"
            elif y < y_int:
                dir2 = "backward"
                
            if dir1 and dir2:
                self.step_double_impulse(dir1,dir2,impulse)
                x_int = x
                y_int = y
                #print(f"Doppellauf:\t- motor1 {dir1}\tx={abs(x_int)} x0={x0}\n\t\t- motor2 {dir2}\ty={abs(y_int)} y0={y0}")
            elif dir1:
                self.step_impulse(dir1,impulse,"motor1")
                x_int = x
                #print(f"Doppellauf:\t- motor1 {dir1}\tx={abs(x_int)} x0={x0}\n\t\t- motor2 aus \ty={y_int} y0={y0}")
            elif dir2:
                self.step_impulse(dir2,impulse,"motor2")
                y_int = y
                #print(f"Doppellauf:\t- motor1 aus\tx={x_int} x0={x0}\n\t\t- motor2 {dir2}\ty={abs(y_int)} y0={y0}")
                
        print(f"\nEnde Initialisierung {x_int,y_int}\n")

    def stop_pos(self,x0,y0,impulse):
        #print(f"\nEndbediungung: x = {x0}, y = {y0} => (0,0)")
        steps = list(pybresenham.line(x0,y0,0,0))
        x_int = x0
        y_int = y0
        for x,y in steps:
            
            dir1 = None
            dir2 = None
            
            if x > x_int:
                dir1 = "forward"
            elif x < x_int:
                dir1 = "backward"
            if y > y_int:
                dir2 = "forward"
            elif y < y_int:
                dir2 = "backward"
                
            if dir1 and dir2:
                self.step_double_impulse(dir1,dir2,impulse)
                x_int = x
                y_int = y
                #print(f"Doppellauf:\t- motor1 {dir1}\tx={abs(x_int)} x0={x0}\n\t\t- motor2 {dir2}\ty={abs(y_int)} y0={y0}")
            elif dir1:
                self.step_impulse(dir1,impulse,"motor1")
                x_int = x
                #print(f"Doppellauf:\t- motor1 {dir1}\tx={abs(x_int)} x0={x0}\n\t\t- motor2 aus \ty={y_int} y0={y0}")
            elif dir2:
                self.step_impulse(dir2,impulse,"motor2")
                y_int = y
                #print(f"Doppellauf:\t- motor1 aus\tx={x_int} x0={x0}\n\t\t- motor2 {dir2}\ty={abs(y_int)} y0={y0}")
                
        print(f"\nEnde Endbediungung {x_int,y_int}\n")


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
        
    def bresenham_step(self,x0:int,y0:int,x1:int,y1:int,impulse:int):
        #self.start_pos(x0,y0,impulse)
        steps = list(pybresenham.line(x0,y0,x1,y1))
        print(steps)
        self.x_old = x0
        self.y_old = y0
        s=0
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
                self.step_double_impulse(dir1,dir2,impulse)
                self.x_old = x
                self.y_old = y
                #print("Doppelschritt x/y ",dir1,dir2,self.x_old,self.y_old)
            elif dir1:
                self.step_impulse(dir1,impulse,"motor1")
                self.x_old = x
                #print("Einzelschritt x ",dir1,self.x_old,self.y_old)
            elif dir2:
                self.step_impulse(dir2,impulse,"motor2")
                self.y_old = y
                #print("Einzelschritt y ",dir2,self.x_old,self.y_old)        

            #print(f"\nGesamtschritt real: {x,y} | {steps[s]} :Vergleichswert aus Funktion")
            s=s+1
        
    def gcode_step(self, filepath: str, impulse: int = 1000):
            """Liest eine G-Code-Datei ein und führt die Bewegungen Schritt für Schritt aus."""
            self.read_gcode(filepath)
            
            coords_df = self.df[["X", "Y"]]*1e3
            coords_df = coords_df.fillna(value=0,limit=1).ffill()
            coords_df = coords_df.ffill()
            print(coords_df)

            if coords_df.empty:
                print("Keine gültigen X/Y-Koordinaten im G-Code gefunden.")
                return

            points = [(int(row["X"]), int(row["Y"])) for _, row in coords_df.iterrows()]
            current_x, current_y = 0, 0

            for next_x, next_y in points:
                print(f"\n--- Fahre von ({current_x}, {current_y}) nach ({next_x}, {next_y}) ---")
                self.bresenham_step(current_x, current_y, next_x, next_y, impulse)
                current_x, current_y = next_x, next_y

            self.stop_pos(current_x, current_y, impulse)