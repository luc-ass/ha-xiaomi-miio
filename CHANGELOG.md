# Changelog

Versionen dieser Integration, neueste oben. Installation und Änderungen in HA stehen in `ha-organisation/CHANGELOG.md`.

## 0.1.0 (unveröffentlicht)

Basis: Core `xiaomi_miio` aus HA 2026.10.4.

- Reinigen nach Bereich (`CLEAN_AREA`) für Roborock-Sauger mit Raumaufteilung: Raumliste aus `get_room_mapping`, Reinigung über `segment_clean`, Reparaturmeldung bei geänderten Räumen
- Tests: Core-Tests laufen unverändert gegen die Kopie, dazu `test_vacuum_segments.py` (63 Tests)
