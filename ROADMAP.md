# Roadmap

Nur Offenes. Erledigtes steht im `CHANGELOG.md`.

## Test am Gerät (Roborock S5)

- [ ] Reparaturmeldung bei geänderter Karte im echten Betrieb prüfen (beim S5 greift sie nur für eingetragene Räume, er meldet selbst keine)
- [ ] GitHub-Release mit Versionsnummer anlegen, damit HACS Updates anzeigt (installiert ist bisher der Stand von `main`)

## Core-PR

- [ ] Abfrage von `get_room_mapping` bei jeder Aktualisierung: zu häufig? Alternative: nur beim Start und nach jeder Reinigung
- [ ] Räume von Hand (Optionen) für den Core vertretbar? Alternative wäre die Cloud-Karte auszuwerten (RRMap), deutlich aufwendiger
- [ ] Tests in `test_vacuum.py` einordnen (hier getrennt in `test_vacuum_segments.py`), Snapshot-Tests prüfen
- [ ] PR an home-assistant/core, Codeowner von `xiaomi_miio` vorher fragen (Issue oder Discussion)
