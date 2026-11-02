# Roadmap

Nur Offenes. Erledigtes steht im `CHANGELOG.md`.

## Test am Gerät (Roborock S5)

- [ ] Segment-IDs des OG durch Probefahrten zuordnen (`segment_clean`, ab 16) und in den Optionen eintragen. Befund 2026-11-02: `get_room_mapping` bleibt beim S5 leer, Räume lassen sich in der Xiaomi-App nicht benennen, auch sonst kein lokaler Befehl liefert die Segmente. Segment 16 existiert
- [ ] In HA installieren (HACS, benutzerdefiniertes Repository), Neustart nur nach OK, Räume den Bereichen zuordnen, `vacuum.clean_area` testen
- [ ] Reparaturmeldung bei geänderter Karte im echten Betrieb prüfen

## Core-PR

- [ ] Abfrage von `get_room_mapping` bei jeder Aktualisierung: zu häufig? Alternative: nur beim Start und nach jeder Reinigung
- [ ] Räume von Hand (Optionen) für den Core vertretbar? Alternative wäre die Cloud-Karte auszuwerten (RRMap), deutlich aufwendiger
- [ ] Tests in `test_vacuum.py` einordnen (hier getrennt in `test_vacuum_segments.py`), Snapshot-Tests prüfen
- [ ] PR an home-assistant/core, Codeowner von `xiaomi_miio` vorher fragen (Issue oder Discussion)
