#!/usr/bin/env bash
# Neuen Core-Stand von xiaomi_miio übernehmen: aktualisiert den Branch
# `upstream` auf den HA-Tag und führt ihn in `main` zusammen.
#
#   tools/core_update.sh 2026.11.0
#
# Danach: Konflikte lösen, pyproject.toml (pytest-homeassistant-custom-component
# passend zum Tag) anpassen, `uv run pytest`, Version im Manifest erhöhen.
set -euo pipefail

TAG="${1:?HA-Version angeben, z. B. 2026.11.0}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

cd "$ROOT"
if [[ -n "$(git status --porcelain)" ]]; then
    echo "Arbeitsverzeichnis nicht sauber, erst committen." >&2
    exit 1
fi

git clone -q --depth 1 --branch "$TAG" --filter=blob:none --sparse \
    https://github.com/home-assistant/core.git "$TMP/core"
git -C "$TMP/core" sparse-checkout set \
    homeassistant/components/xiaomi_miio tests/components/xiaomi_miio

# Übersetzungen gibt es nur im gebauten Paket, nicht im Quellcode
uv pip download --quiet --no-deps --dest "$TMP/wheel" "homeassistant==$TAG" 2>/dev/null \
    || pip download --quiet --no-deps --dest "$TMP/wheel" "homeassistant==$TAG"
unzip -q "$TMP"/wheel/homeassistant-*.whl \
    'homeassistant/components/xiaomi_miio/translations/*' -d "$TMP/wheel"

git checkout -q upstream
rm -rf custom_components/xiaomi_miio tests/components/xiaomi_miio
cp -R "$TMP/core/homeassistant/components/xiaomi_miio" custom_components/
cp -R "$TMP/wheel/homeassistant/components/xiaomi_miio/translations" \
    custom_components/xiaomi_miio/
cp -R "$TMP/core/tests/components/xiaomi_miio" tests/components/
echo "$TAG" > CORE_VERSION
git add -A
git commit -q -m "Core xiaomi_miio $TAG unverändert übernommen" || echo "Keine Änderungen im Core."
git checkout -q main
git merge --no-edit upstream || echo "Konflikte lösen, dann committen."
