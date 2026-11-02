# Roadmap

Nur Offenes. Erledigtes steht im `CHANGELOG.md`.

## Test am Gerät (Roborock S5)

- [ ] `get_room_mapping` liefert `[]`, obwohl die Karte gespeichert und segmentiert ist (`lab_status` 1, `get_segment_status` [1], 2026-11-02). Klären: Meldet der S5 Räume erst, wenn sie in der Xiaomi-App benannt sind? Sonst Segment-IDs ab 16 mit `segment_clean` ausprobieren
- [ ] Wie heißen die Räume in `get_room_mapping`: Klarname oder Cloud-ID? Davon hängt ab, ob die Namen im Zuordnungsdialog lesbar sind
- [ ] In HA installieren (HACS, benutzerdefiniertes Repository), Neustart nur nach OK, Räume den Bereichen zuordnen, `vacuum.clean_area` testen
- [ ] Reparaturmeldung bei geänderter Karte im echten Betrieb prüfen

## Core-PR

- [ ] Abfrage von `get_room_mapping` bei jeder Aktualisierung: zu häufig? Alternative: nur beim Start und nach jeder Reinigung
- [ ] Entscheiden, ob ein Modell ohne benannte Räume trotzdem `CLEAN_AREA` bekommen soll
- [ ] Tests in `test_vacuum.py` einordnen (hier getrennt in `test_vacuum_segments.py`), Snapshot-Tests prüfen
- [ ] PR an home-assistant/core, Codeowner von `xiaomi_miio` vorher fragen (Issue oder Discussion)
