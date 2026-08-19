import board
import digitalio
import adafruit_max31865
import time

spi = board.SPI()
cs = digitalio.DigitalInOut(board.D5)  # Chip select
sensor = adafruit_max31865.MAX31865(spi, cs, rtd_nominal=100.0, ref_resistor=428.0, wires=3)

# Den Fehlerstatus direkt ausgeben
fault = sensor.fault
print(f"Fault-Status (Rohdaten): {fault}")

# Um den Chip nach einem Fehler zurückzusetzen, falls er im Fehlerzustand hängt:
sensor.clear_faults()

while True:
    print(f"Temperature: {sensor.temperature:0.3f} C")
    print(f"Resistance: {sensor.resistance:0.3f} Ohm \n")
    time.sleep(1)
