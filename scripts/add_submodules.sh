#!/usr/bin/env bash
set -euo pipefail

# add_submodules.sh
# Agrega los submódulos definidos en modules.json y actualiza de forma recursiva.

ROOT_DIR="$(cd "${BASH_SOURCE[0]%/*}"/.. && pwd)"
cd "$ROOT_DIR"

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "[ERROR] Este script debe ejecutarse dentro de un repositorio git." >&2
  exit 1
fi

MODULES_FILE="modules.json"
if [[ ! -f "$MODULES_FILE" ]]; then
  echo "[ERROR] No se encontró $MODULES_FILE. Crea este archivo o restaura el repo." >&2
  exit 1
fi

add_module() {
  local path="$1"; shift
  local url="$1"; shift

  if [[ -d "$path" ]] && [[ -d "$path/.git" ]]; then
    # Si ya es un repo, asumir que el submódulo fue agregado previamente
    if git submodule status -- "$path" >/dev/null 2>&1; then
      echo "[SKIP] Ya es submódulo: $path"
      return 0
    else
      echo "[WARN] Directorio git existente en $path pero no como submódulo. Omite." >&2
      return 0
    fi
  fi

  echo "[ADD] $path -> $url"
  git submodule add "$url" "$path" || {
    echo "[WARN] Falló agregar $path desde $url (¿repo privado/inexistente?)." >&2
    return 0
  }
}

# Recorre modules.json y agrega submódulos
python3 - "$MODULES_FILE" <<'PY' | while read -r path url; do
import json, sys
from pathlib import Path

mods = json.load(open(sys.argv[1]))
for name, spec in mods.items():
    path = spec.get("path", name)
    url = spec.get("repo")
    if not url:
        continue
    print(path, url)
PY
  mkdir -p "$(dirname "$path")"
  add_module "$path" "$url"
done

echo "[INFO] Inicializando/actualizando submódulos..."
git submodule update --init --recursive

echo "[DONE] Submódulos procesados."
