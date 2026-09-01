import board, digitalio, adafruit_max31865, time, csv
from datetime import datetime, timedelta

"""
VCC = 3.3V
GND = GND
CLK = GPIO12
SDI = GPIO10
SDO = GPIO9
CS  = GPIO5
"""

spi = board.SPI()
cs = digitalio.DigitalInOut(board.D5)  # Chip select
sensor = adafruit_max31865.MAX31865(spi, cs, rtd_nominal=100.0, ref_resistor=428.25, wires=3)
sensor.clear_faults()

filename = "temp_data.csv"

print(f"Datenaufnahme von Temperaturdaten mit PT100\n")
h = int(input("Stunden: ") or 0)
m = int(input("Minuten: ") or 0)
s = int(input("Sekunden: ") or 0)

secs = 3600 * h + 60 * m + s

with open(filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp", "Temperature_C", "Resistance_Ohm"])

    end_time = (datetime.now() + timedelta(seconds=secs))
    while datetime.now() < end_time:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        temp = sensor.temperature
        res = sensor.resistance

        print(f"[{timestamp}] Temp: {temp:0.3f} °C | Res: {res:0.3f} Ohm")
        writer.writerow([timestamp, f"{temp:.3f}", f"{res:.3f}"])
        file.flush()

        time.sleep(1)

print("\nAufnahme beendet!")