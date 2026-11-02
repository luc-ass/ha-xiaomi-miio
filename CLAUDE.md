# HA Xiaomi Miio (Reinigen nach Bereich)

Kopie der Core-Integration `xiaomi_miio` (Home Assistant, Anzeigename „Xiaomi Home“) mit einer kleinen Erweiterung: **Reinigen nach Bereich** (`vacuum.clean_area`) für Roborock-Sauger, die nur über die Xiaomi-App laufen. Anlass ist Lucas' Roborock S5 („Saugroboter OG“, `vacuum.sauger_og_schlafzimmer`). Die Custom-Integration überschreibt die eingebaute mit gleichem Domain-Namen, Einrichtung und Entities bleiben.

Ziel: die Erweiterung später als Pull Request im Core einreichen. Deshalb bleibt der Unterschied zum Core so klein wie möglich.

Sprache: Doku, Commits und Rückfragen auf Deutsch. Code, Kommentare, Tests und `README.md` auf Englisch (Core-Stil).

## Dokumente

| Datei | Inhalt |
| --- | --- |
| `CHANGELOG.md` | Versionen dieser Integration, neueste oben |
| `ROADMAP.md` | Offene Aufgaben (Test am Gerät, PR) |
| `README.md` | Installation und Unterschiede zum Core (englisch, für HACS) |
| `CORE_VERSION` | HA-Version, aus der der Core-Code stammt |

Änderungen in HA (Installation, Neustart, Bereichszuordnung) stehen im `CHANGELOG.md` von `~/Projects/ha-organisation` mit Verweis auf die Version hier. Dort gelten auch die Freigaben (HA neu starten nur nach OK).

## Branches

- `upstream`: Core-Code unverändert, je HA-Version ein Commit (`tools/core_update.sh <tag>`). Enthält auch `translations/` aus dem HA-Paket, weil Custom-Integrationen `strings.json` nicht lesen.
- `main`: `upstream` plus Erweiterung. `git diff upstream -- custom_components` zeigt genau, was ein PR enthielte.

Core-Dateien nur dort ändern, wo die Erweiterung es braucht. Keine Formatierung oder Aufräumarbeiten in Core-Code, sonst wird der Diff unlesbar.

## Erweiterung

- `config_flow.py`, `const.py`, `strings.json`, `translations/`: Option `rooms` für Sauger (`{"16": "Schlafzimmer"}`), Ersatz für Modelle ohne Raumliste wie den S5
- `__init__.py`: Der Vacuum-Coordinator liest `get_room_mapping`, `VacuumCoordinatorData.rooms` ist `None`, wenn das Gerät es nicht kann.
- `vacuum.py`: `VacuumEntityFeature.CLEAN_AREA`, sobald Räume gemeldet werden, danach bleibt es gesetzt. `async_get_segments` fragt frisch ab, `async_clean_segments` nutzt `segment_clean`, `_async_check_segments_changed` legt die Reparaturmeldung an.
- Manifest: `version` und `issue_tracker` (Pflicht für Custom-Integrationen).

## Tests

```
uv sync
uv run pytest          # Core-Tests unverändert plus test_vacuum_segments.py
uv run ruff check custom_components tests conftest.py
```

`conftest.py` leitet `homeassistant.components.xiaomi_miio` auf die Custom-Kopie um, `tests/common.py` und `tests/typing.py` ersetzen die Hilfen aus dem Core. So bleiben die Core-Tests unverändert und neue Tests lassen sich 1:1 in einen PR übernehmen. `pytest-homeassistant-custom-component` muss zur HA-Version in `CORE_VERSION` passen. Ruff prüft nur Fehler und Importe mit den isort-Regeln des Core, damit der Core-Code ohne Änderungen durchgeht.

## Gerät

`uv run tools/raumliste.py` liest Modell, Firmware, Kartenspeicher und Raumliste (nur lesend). Zugangsdaten `S5_HOST` und `S5_TOKEN` aus `.env` hier oder aus `../ha-organisation/.env`. Den Token nie ausgeben oder in Dateien schreiben.

Befehle, die den Sauger bewegen (`segment_clean`, `app_segment_clean`), hat Lucas für Tests freigegeben (2026-11-02).

### Befunde am S5 (Firmware 3.5.8, 2026-11-02)

- `get_room_mapping` liefert `[]`, Räume lassen sich in der Xiaomi-App nicht benennen. Kein lokaler Befehl liefert die Segmente, sie stehen nur in der Cloud-Karte
- `segment_clean` nimmt jede ID von 1 bis 31 an (40 lehnt er ab: „data for segment is invalid“). Bei einer ID ohne Raum fährt er nach etwa 5–15 s von selbst zurück, Fläche 0
- Segmente aus der automatischen Aufteilung haben IDs ab 1, von Hand abgetrennte ab 16. OG: 2 Arbeitszimmer, 3 Badezimmer, 4 Kinderzimmer, 5 Schlafzimmer, 16 Treppe (gesperrt), 17 Flur OG
- Probefahrten am schnellsten so: Claude schickt ihn los, Lucas sagt den Raum und holt ihn in der App zurück
- `goto` (und neue Ziele allgemein) nimmt der S5 während einer Fahrt oder Reinigung nicht an, vorher `stop`. Die Position gibt er lokal nicht heraus (kein `get_*pos*`), die Station liegt bei etwa x 25500, y 25500 (mm). Abfalleimer OG: x 21300, y 24200 (`script.sauger_og_abfalleimer` in HA)
