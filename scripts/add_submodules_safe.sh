#!/usr/bin/env bash
set -euo pipefail

# add_submodules_safe.sh
# Agrega los submódulos definidos en modules.json con validación previa de accesibilidad.

ROOT_DIR="$(cd "${BASH_SOURCE[0]%/*}"/.. && pwd)"
cd "$ROOT_DIR"

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "[ERROR] Este script debe ejecutarse dentro de un repositorio git." >&2
  exit 1
fi

MODULES_FILE="modules.json"
VERIFIED_FILE="modules_verified.json"

# Usar modules_verified.json si existe, sino usar modules.json
if [[ -f "$VERIFIED_FILE" ]]; then
  MODULES_FILE="$VERIFIED_FILE"
  echo "[INFO] Usando $VERIFIED_FILE (solo repositorios verificados)"
elif [[ -f "$MODULES_FILE" ]]; then
  echo "[INFO] Usando $MODULES_FILE (todos los repositorios)"
else
  echo "[ERROR] No se encontró $MODULES_FILE ni $VERIFIED_FILE." >&2
  exit 1
fi

check_repo_accessibility() {
  local url="$1"
  
  echo "[CHECK] Verificando accesibilidad de $url"
  
  # Usar curl para verificar si el repo es accesible
  local status
  status=$(curl -s -I "$url" | head -n1 | cut -d' ' -f2)
  
  case "$status" in
    200|301|302)
      echo "[OK] Repositorio accesible (HTTP $status)"
      return 0
      ;;
    404)
      echo "[ERROR] Repositorio no encontrado (HTTP 404)"
      return 1
      ;;
    403)
      echo "[ERROR] Repositorio privado o acceso denegado (HTTP 403)"
      return 1
      ;;
    *)
      echo "[WARN] Estado desconocido (HTTP $status), intentando de todas formas"
      return 0
      ;;
  esac
}

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

  # Verificar accesibilidad antes de intentar clonar
  if ! check_repo_accessibility "$url"; then
    echo "[SKIP] $path -> $url (repositorio no accesible)"
    return 0
  fi

  echo "[ADD] $path -> $url"
  if git submodule add "$url" "$path"; then
    echo "[SUCCESS] Submódulo agregado: $path"
  else
    echo "[ERROR] Falló agregar $path desde $url" >&2
    return 1
  fi
}

echo "[INFO] Procesando submódulos desde $MODULES_FILE"

# Recorre modules.json y agrega submódulos
python3 - "$MODULES_FILE" <<'PY' | while IFS=' ' read -r path url; do
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
  echo ""
  echo "=== Procesando módulo: $path ==="
  mkdir -p "$(dirname "$path")"
  add_module "$path" "$url" || {
    echo "[WARN] Error procesando $path, continuando con siguiente módulo"
  }
done

echo ""
echo "[INFO] Inicializando/actualizando submódulos..."
if git submodule update --init --recursive; then
  echo "[SUCCESS] Submódulos inicializados correctamente"
else
  echo "[WARN] Algunos submódulos pueden no haberse inicializado correctamente"
fi

echo ""
echo "[INFO] Listando submódulos agregados:"
git submodule status || echo "[WARN] No hay submódulos activos"

echo ""
echo "[DONE] Proceso de submódulos completado."