import asyncio
from datetime import datetime
import threading
import time
import python_weather
from RPLCD.i2c import CharLCD

# Globale Variable für die Wetterdaten
weather_data = {"temp": "--", "description": "Lade..."}

wetter_ort = "Bremen" 

async def fetch_weather():
    """Holt alle 10 Minuten die aktuellen Wetterdaten für Bremen."""
    global weather_data
    while True:
        try:
            async with python_weather.Client(
                unit=python_weather.METRIC
            ) as client:
                weather = await client.get(wetter_ort)
                weather_data["temp"] = f"{weather.temperature}°C"
                weather_data["description"] = weather.description[
                    :16
                ]  # Auf 16 Zeichen begrenzen
        except Exception as e:
            weather_data["description"] = "Fehler"
        await asyncio.sleep(600)  # Alle 10 Minuten aktualisieren


def start_asyncio_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(fetch_weather())


# Initialisiere die Displays
lcd1 = CharLCD(
    i2c_expander="PCF8574",
    address=0x27,
    port=3,
    cols=16,
    rows=2,
    charmap="A00",
)

lcd2 = CharLCD(
    i2c_expander="PCF8574",
    address=0x21,
    port=3,
    cols=16,
    rows=2,
    charmap="A00",
)

# Custom Characters
heart = (
    0b00000,
    0b01010,
    0b11111,
    0b11111,
    0b01110,
    0b00100,
    0b00000,
    0b00000,
)

smiley = (
    0b00000,
    0b01010,
    0b00000,
    0b00100,
    0b10001,
    0b01110,
    0b00000,
    0b00000,
)

lcd1.create_char(0, heart)
lcd1.create_char(1, smiley)

# Steuer-Flag für die Threads
running = True


def update_lcd1():
    """Aktualisiert Datum und Uhrzeit auf lcd1."""
    lcd1.cursor_pos = (0, 0)
    lcd1.write_string(chr(0))
    lcd1.cursor_pos = (1, 0)
    lcd1.write_string(chr(1))

    while running:
        now = datetime.now()

        lcd1.cursor_pos = (0, 3)
        lcd1.write_string(now.strftime("%d.%m.%Y"))

        lcd1.cursor_pos = (1, 3)
        lcd1.write_string(now.strftime("%H:%M:%S"))

        time.sleep(1)


# Event-Loop für Wetter-Updates in einem eigenen Thread starten
weather_loop = asyncio.new_event_loop()
thread_weather = threading.Thread(target=start_asyncio_loop, args=(weather_loop,), daemon=True)
thread_weather.start()

# Thread für LCD1 starten
thread_lcd1 = threading.Thread(target=update_lcd1, daemon=True)
thread_lcd1.start()

try:
    while True:
        # 1. Wetterdaten auf LCD2 anzeigen
        lcd2.clear()
        lcd2.cursor_pos = (0, 0)
        lcd2.write_string(f"{wetter_ort}: {weather_data['temp']}")
        lcd2.cursor_pos = (1, 0)
        lcd2.write_string(weather_data["description"])
        time.sleep(4)

except KeyboardInterrupt:
    print("\nProgramm beendet.")

finally:
    running = False
    time.sleep(0.2)

    # Displays säubern und Hintergrundbeleuchtung ausschalten
    lcd1.clear()
    lcd1.backlight_enabled = False
    lcd2.clear()
    lcd2.backlight_enabled = False