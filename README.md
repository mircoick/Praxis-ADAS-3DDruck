# Praxissemester: Machbarkeitsanalyse zum System-Update eines 3D-Industriedruckers

In diesem Repository ist die technische und wirtschaftliche Machbarkeit eines System-Updates (Hardware & Software) für den 3D-Industriedrucker **3Dgence INDUSTRY F421** dokumentiert. Im Rahmen des Praxissemesters bei der **Airbus DS Airborne Solutions GmbH** wurde die Migration auf moderne Open-Source-Komponenten untersucht.

---

## Dokumentation & Berichte

Die offiziellen Berichte und Ausarbeitungen stehen im PDF-Format zur Verfügung:
* [Zwischenbericht (PDF)](report/.output/Zwischenbericht_Mirco_Ick_5312533.pdf)
* [Abschlussbericht (PDF)](report/.output/prx_final_report.pdf)

---

## Repository-Struktur

Das Repository gliedert sich in folgende Hauptkomponenten:

- **[`doku/`](doku/)** - Ergänzende Projektdokumentationen.
- **[`info/`](info/)**    -    Datenblätter und Firmeninfos.
- **[`kicad/`](kicad/)**  -    Idee einer Adapterplatine mit Schaltplänen.
- **[`klipper/`](klipper/)**  -  Konfigurationsdateien, Makros und Firmware-Anpassungen für Klipper.
- **[`print_data/`](print_data/)**  -  Testdrucke, Slicer-Profile und druckspezifische Daten.
- **[`python/`](python/)**  -  Skripte zur isolierten Sensor- und Hardware-Ansteuerung.
- **[`report/`](report/)**  -  Quarto-Quellcode (`.qmd`) und Build-Artefakte der Berichte.

---

## 🛠️ Systemdaten & Key Facts

* **Hersteller:** 3Dgence
* **Modell:** INDUSTRY F421
* **Kernziele:** Evaluierung neuer Steuerungs-Hardware (u. a. Mainboard- und Sensor-Integration), Firmware-Umstellung auf Klipper sowie Analyse der technischen und wirtschaftlichen Realisierbarkeit.
