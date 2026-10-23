# Praxissemester: System-Update des 3D-Industriedruckers 3Dgence INDUSTRY F421

In diesem Repository ist die technische und wirtschaftliche Machbarkeit eines System-Updates (Hardware & Software) für den 3D-Industriedrucker **3Dgence INDUSTRY F421** dokumentiert. Im Rahmen des Praxissemesters bei der **Airbus DS Airborne Solutions GmbH** wurde die Migration auf moderne Open-Source-Komponenten untersucht.

---

## Dokumentation & Berichte

Die offiziellen Berichte und Ausarbeitungen stehen im PDF-Format zur Verfügung:
* [Zwischenbericht (PDF)](report/.output/Zwischenbericht_Mirco_Ick_5312533.pdf)
* [Abschlussbericht (PDF)](report/.output/prx_final_report.pdf)

---

## Repository-Struktur

Das Repository gliedert sich in folgende Hauptkomponenten:

* **[`doku/`](doku/)** – Ergänzende Projektdokumentationen und Datenblätter.
* **[`kicad/`](kicad/)** – Platinenlayouts und Schaltpläne (z. B. Adapter-PCB für die Mainboard-Integration).
* **[`klipper/`](klipper/)** – Konfigurationsdateien, Makros und Firmware-Anpassungen für Klipper.
* **[`python/`](python/)** – Skripte zur Sensor- und Hardware-Ansteuerung.
* **[`print_data/`](print_data/)** – Testdrucke, Slicer-Profile und druckspezifische Daten.
* **[`report/`](report/)** – Quarto-Quellcode (`.qmd`) und Build-Artefakte der Berichte.

---

## 🛠️ Systemdaten & Key Facts

* **Hersteller:** 3Dgence
* **Modell:** INDUSTRY F421
* **Kernziele:** Evaluierung neuer Steuerungs-Hardware (u. a. Mainboard- und Sensor-Integration), Firmware-Umstellung auf Klipper sowie Analyse der technischen und wirtschaftlichen Realisierbarkeit.