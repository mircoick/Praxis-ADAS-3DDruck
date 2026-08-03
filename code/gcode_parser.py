from gcodeparser import GcodeParser

with open("data/overhang test.gcode", "r") as datei:
    gcode_inhalt = datei.read()

parsed_lines = GcodeParser(gcode_inhalt).lines
for line in parsed_lines:
    if line.command:
        print(f"Befehl: {line.command}, Parameter: {line.params}")
