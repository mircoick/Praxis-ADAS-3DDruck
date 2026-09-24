from . import bus

SLOT_ADDRS = {
    'unten_rechts': 0x6c,
    'unten_links':  0x6d,
    'oben_rechts':  0x6e,
    'oben_links':   0x6f,
}

class FilamentControl:
    def __init__(self, config):
        self.printer = config.get_printer()
        self.name = config.get_name()

        # I2C Hauptplatine (0x6a)
        self.i2c_main = bus.MCU_I2C_from_config(config, default_addr=0x6a)

        # Status-Variablen
        self.temp_innenraum = 0.0
        self.temp_heater = 0.0
        self.heating_pwm = 0
        self.slot_status = {
            'unten_rechts': {'detected': False, 'raw': 0x00},
            'unten_links':  {'detected': False, 'raw': 0x00},
            'oben_rechts':  {'detected': False, 'raw': 0x00},
            'oben_links':   {'detected': False, 'raw': 0x00},
        }

        # I2C Filament-Platinen initialisieren
        self.slots = {}
        for sname, addr in SLOT_ADDRS.items():
            self.slots[sname] = bus.MCU_I2C_from_config(config, default_addr=addr)

        # G-Code Commands registrieren
        gcode = self.printer.lookup_object('gcode')
        gcode.register_command("SET_FILAMENT_HEATING_PWM", self.cmd_SET_HEATING_PWM)
        gcode.register_command("SET_FILAMENT_MOTOR", self.cmd_SET_MOTOR)
        gcode.register_command("I2C_SCAN_FILAMENT", self.cmd_I2C_SCAN_FILAMENT)
        gcode.register_command("QUERY_FILAMENT_CONTROL", self.cmd_QUERY_FILAMENT_CONTROL)

        # Timer-Event registrieren
        self.printer.register_event_handler("klippy:connect", self._handle_connect)

    def _handle_connect(self):
        reactor = self.printer.get_reactor()
        reactor.register_timer(self._sample_sensor, reactor.monotonic() + 1.0)

    def _sample_sensor(self, eventtime):
        # 1. Hauptplatine: Innenraum-Temp (0x04) & Heizung-Temp (0x0E)
        try:
            res_in = self.i2c_main.i2c_write_read([0x04], 1)
            if res_in:
                self.temp_innenraum = float(res_in[0])

            res_ht = self.i2c_main.i2c_write_read([0x0e], 1)
            if res_ht:
                self.temp_heater = float(res_ht[0])
        except Exception:
            pass

        # 2. Filament-Platinen: Filamenterkennung (Register 0x03)
        for sname, dev in self.slots.items():
            try:
                res_fil = dev.i2c_write_read([0x03], 1)
                if res_fil:
                    val = res_fil[0]
                    self.slot_status[sname]['raw'] = val
                    self.slot_status[sname]['detected'] = (val == 0x03)
            except Exception:
                self.slot_status[sname]['detected'] = False

        return eventtime + 1.0

    def cmd_SET_HEATING_PWM(self, gcmd):
        val = gcmd.get_int('VALUE', minval=0, maxval=255)
        self.i2c_main.i2c_write([0x05, val])
        self.heating_pwm = val
        gcmd.respond_info(f"Filament Heizung PWM auf {val} gesetzt.")

    def cmd_SET_MOTOR(self, gcmd):
        slot = gcmd.get('SLOT')
        cmd = gcmd.get_int('CMD', 0x00)
        if slot in self.slots:
            self.slots[slot].i2c_write([0x0a, cmd])
            gcmd.respond_info(f"Slot {slot} Motor Command: {cmd}")
        else:
            gcmd.respond_info(f"Unbekannter Slot. Optionen: {list(self.slots.keys())}")

    def cmd_I2C_SCAN_FILAMENT(self, gcmd):
        gcmd.respond_info("--- Starte I2C Bus Status-Check ---")
        
        # Hauptplatine prüfen
        try:
            res = self.i2c_main.i2c_write_read([0x04], 1)
            gcmd.respond_info("Hauptplatine (0x6a): ONLINE")
        except Exception:
            gcmd.respond_info("Hauptplatine (0x6a): OFFLINE / FEHLER")

        # Slots prüfen
        for sname, dev in self.slots.items():
            addr_hex = f"0x{SLOT_ADDRS[sname]:02x}"
            try:
                res = dev.i2c_write_read([0x03], 1)
                gcmd.respond_info(f"Slot {sname} ({addr_hex}): ONLINE")
            except Exception:
                gcmd.respond_info(f"Slot {sname} ({addr_hex}): OFFLINE / FEHLER")

    def cmd_QUERY_FILAMENT_CONTROL(self, gcmd):
        msg = ["--- Filament Control Status ---"]
        msg.append(f"Innenraum Temp: {self.temp_innenraum:.1f} °C")
        msg.append(f"Heizung/Lüfter Temp: {self.temp_heater:.1f} °C")
        msg.append(f"Heizung PWM: {self.heating_pwm}/255")
        msg.append("Slots:")
        for sname, sdata in self.slot_status.items():
            state = "Filament erkannt" if sdata['detected'] else "Leer / Nicht erkannt"
            msg.append(f"  - {sname}: {state} (Raw: 0x{sdata['raw']:02x})")
        gcmd.respond_info("\n".join(msg))

    def get_status(self, eventtime):
        return {
            'temperature': round(self.temp_innenraum, 2),
            'temp_heater': round(self.temp_heater, 2),
            'heating_pwm': self.heating_pwm,
            'unten_rechts_detected': self.slot_status['unten_rechts']['detected'],
            'unten_links_detected': self.slot_status['unten_links']['detected'],
            'oben_rechts_detected': self.slot_status['oben_rechts']['detected'],
            'oben_links_detected': self.slot_status['oben_links']['detected'],
        }

def load_config(config):
    return FilamentControl(config)