import board, digitalio, adafruit_max31865, time, csv
from datetime import datetime

spi = board.SPI()
cs = digitalio.DigitalInOut(board.D5)  # Chip select
sensor = adafruit_max31865.MAX31865(spi, cs, rtd_nominal=100.0, ref_resistor=428.0, wires=3)
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

    for _ in range(secs):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        temp = sensor.temperature
        res = sensor.resistance

        print(f"[{timestamp}] Temp: {temp:0.3f} °C | Res: {res:0.3f} Ohm")
        writer.writerow([timestamp, f"{temp:.3f}", f"{res:.3f}"])
        file.flush()

        time.sleep(1)
