import csv
import time
from datetime import datetime
from smbus2 import SMBus

I2C_BUS = 1
ADDRESSES = [0x6a,0x6c, 0x6d, 0x6e, 0x6f]  # Beispielhafte Adressen
#ADDRESSES = [0x6a]
NUM_REGISTERS = 16
TEST_VALUES = [0x00, 0x55, 0xAA, 0xFF]
CSV_FILENAME = "i2c_log.csv"


def monitor_i2c():
  cache = {}
  with SMBus(I2C_BUS) as bus:
    for addr in ADDRESSES:
      try:
        cache[addr] = [
            bus.read_byte_data(addr, reg) for reg in range(NUM_REGISTERS)
        ]
      except OSError:
        cache[addr] = None

    print(
        f"I2C-Registerüberwachung gestartet. Schreibe in {CSV_FILENAME} (Abbruch"
        " mit Strg+C)...\n"
    )

    with open(CSV_FILENAME, mode="w", newline="") as f:
      writer = csv.writer(f)
      writer.writerow(
          ["timestamp", "address", "register", "old_value", "new_value"]
      )

      while True:
        timestamp = datetime.now()
        for addr in ADDRESSES:
          if cache[addr] is None:
            continue
          for reg in range(NUM_REGISTERS):
            try:
              val = bus.read_byte_data(addr, reg)
              old_val = cache[addr][reg]
              if val != old_val:
                print(
                    f"[CHANGE] 0x{addr:02x} | Reg 0x{reg:02x}: 0x{old_val:02x}"
                    f" -> 0x{val:02x}"
                )
                writer.writerow(
                    [timestamp, f"0x{addr:02x}", f"0x{reg:02x}", old_val, val]
                )
                f.flush()
                cache[addr][reg] = val
            except OSError:
              pass
        time.sleep(0.1)


def test_all_registers(addresses, num_registers, test_values, delay_between=0.01):
    """
    Testet für jedes Register systematisch, ob es beschreibbar ist.
    Schreibt Testwerte, prüft auf Änderung und stellt am Ende den Ursprungswert wieder her.
    """
    writable_registers = []

    print("=== Starte automatisierten Register-Schreibtest ===")
    print(f"Test-Adressen: {[hex(a) for a in addresses]}")
    print(f"Register-Bereich: 0x00 bis {hex(num_registers - 1)}")
    print(f"Test-Muster: {[hex(v) for v in test_values]}\n")

    with SMBus(I2C_BUS) as bus:
        for addr in addresses:
            print(f"--- Prüfe Adresse 0x{addr:02x} ---")
            for reg in range(num_registers):
                try:
                    # 1. Ursprünglichen Wert sichern
                    original_val = bus.read_byte_data(addr, reg)
                    is_writable = False
                    successful_val = None

                    # 2. Verschiedene Testwerte durchprobieren
                    for target_val in test_values:
                        # Überspringen, falls der Testwert zufällig dem aktuellen Wert entspricht
                        if target_val == original_val:
                            continue

                        bus.write_byte_data(addr, reg, target_val)
                        time.sleep(delay_between)
                        read_back = bus.read_byte_data(addr, reg)

                        # Wenn sich der Wert tatsächlich auf den Zielwert geändert hat
                        if read_back == target_val:
                            is_writable = True
                            successful_val = read_back
                            break

                    # 3. Ursprungswert wiederherstellen
                    bus.write_byte_data(addr, reg, original_val)
                    time.sleep(delay_between)

                    # 4. Auswertung ausgeben
                    if is_writable:
                        print(f"Addr 0x{addr:02x} | Reg 0x{reg:02x}: BESCHREIBBAR (Alt=0x{original_val:02x} -> Test=0x{successful_val:02x})")
                        writable_registers.append((addr, reg))
                    else:
                        print(f"Addr 0x{addr:02x} | Reg 0x{reg:02x}: Read-Only / Schreibgeschützt (Wert bleibt 0x{original_val:02x})")

                except OSError as e:
                    print(f"Addr 0x{addr:02x} | Reg 0x{reg:02x}: Zugriffsfehler ({e})")

            print()

    print("=== Test beendet ===")
    print(f"Gefundene beschreibbare Register ({len(writable_registers)}):")
    for a, r in writable_registers:
        print(f"  - Addr: 0x{a:02x}, Reg: 0x{r:02x}")


if __name__ == "__main__":
    #test_all_registers(ADDRESSES, NUM_REGISTERS, TEST_VALUES)
    monitor_i2c()