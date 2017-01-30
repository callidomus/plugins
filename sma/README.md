# SMA

# Requirements

* SMA SunnyBoy 1.5 / 2.5 (other may work also)

# Configuration

## Plugin

Description of the attributes:

* __Wechselrichter__: IP or Hostname of the SunnyBoy
* __Benutzer__: select User or Installer
* __Passwort__: Password for the selected user
* __Abfrageintervall__: select polling interval

## Items

| Name                      | Type   | Unit |
|---------------------------|--------|------|
| Status                    | text   |      |
| Status Netzrelais         | text   |      |
| Status Anlagensteuerung   | text   |      |
| Status Gerätesteuerung    | text   |      |
| Eingang Leistung (W)      | number | W    |
| Eingang Spannung (V)      | number | V    |
| Eingang Strom (A)         | number | A    |
| Ausgang Leistung (W)      | number | W    |
| Ausgang Netzfrequenz (Hz) | number | Hz   |
| Ausgang Strom (A) - L1    | number | A    |
| Ausgang Strom (A) - L2    | number | A    |
| Ausgang Strom (A) - L3    | number | A    |
| Ausgang Spannung (V) - L1 | number | V    |
| Ausgang Spannung (V) - L2 | number | V    |
| Ausgang Spannung (V) - L3 | number | V    |
| Ausgang Leistung (W) - L1 | number | W    |
| Ausgang Leistung (W) - L2 | number | W    |
| Ausgang Leistung (W) - L3 | number | W    |
| Ertrag (Wh) - Gesamt      | number | Wh   |
| Ertrag (Wh) - Tag         | number | Wh   |
| Betriebszeit (h)          | number | h    |
| Einspeisezeit (h)         | number | h    |
