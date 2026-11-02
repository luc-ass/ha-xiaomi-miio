# Changelog

Versionen dieser Integration, neueste oben. Installation und Änderungen in HA stehen in `ha-organisation/CHANGELOG.md`.

## 0.2.0 (2026-11-02, in HA installiert)

- Räume von Hand in den Optionen eintragen (`16: Schlafzimmer`, eine Zeile je Raum), für Sauger, die keine Räume melden (Roborock S5). Meldet das Gerät Räume, haben diese Vorrang
- Tests für Options-Dialog und eingetragene Räume (68 Tests)
- Am S5 getestet: `vacuum.clean_area` mit Flur OG fährt in den Flur

## 0.1.0

Basis: Core `xiaomi_miio` aus HA 2026.10.4.

- Reinigen nach Bereich (`CLEAN_AREA`) für Roborock-Sauger mit Raumaufteilung: Raumliste aus `get_room_mapping`, Reinigung über `segment_clean`, Reparaturmeldung bei geänderten Räumen
- Tests: Core-Tests laufen unverändert gegen die Kopie, dazu `test_vacuum_segments.py` (63 Tests)
