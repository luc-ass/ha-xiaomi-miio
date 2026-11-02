# /// script
# requires-python = ">=3.11,<3.14"
# dependencies = ["python-miio==0.5.12"]
# ///
"""Raumaufteilung eines Roborock-Saugers über miio lesen (nur lesend).

Zeigt Modell, Firmware, Kartenspeicher, Segmentstatus und get_room_mapping,
also genau das, was die Integration für CLEAN_AREA abfragt.

Zugangsdaten: S5_HOST und S5_TOKEN aus der Umgebung, sonst aus .env im Repo
oder aus ../ha-organisation/.env. Der Token wird nie ausgegeben.

    uv run tools/raumliste.py
"""

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENV_FILES = [ROOT / ".env", ROOT.parent / "ha-organisation" / ".env"]


def load_env() -> tuple[str, str]:
    for env_file in ENV_FILES:
        if not env_file.exists():
            continue
        for line in env_file.read_text().splitlines():
            if line.startswith("S5_") and "=" in line:
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip().strip('"'))
    if not os.environ.get("S5_HOST") or not os.environ.get("S5_TOKEN"):
        raise SystemExit("S5_HOST und S5_TOKEN fehlen (Umgebung oder .env)")
    return os.environ["S5_HOST"], os.environ["S5_TOKEN"]


def main() -> None:
    from miio import DeviceException, RoborockVacuum

    host, token = load_env()
    vacuum = RoborockVacuum(host, token)
    info = vacuum.info()
    print(f"Modell {info.model}, Firmware {info.firmware_version}")
    status = vacuum.send("get_status")[0]
    print(
        f"Zustand {status.get('state')}, Kartenspeicher (lab_status) "
        f"{status.get('lab_status')}, Karte vorhanden {status.get('map_present')}"
    )
    for command in ("get_segment_status", "get_room_mapping"):
        try:
            print(f"{command}: {vacuum.send(command)}")
        except DeviceException as ex:
            print(f"{command}: Fehler {ex}")


if __name__ == "__main__":
    main()
