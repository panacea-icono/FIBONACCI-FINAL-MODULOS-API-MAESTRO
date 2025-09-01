PANAS Multichain – Integración con PANAS-TOKEN y panas-token.M

Resumen
- Este repos integra los repositorios PANAS-TOKEN y panas-token.M dentro de `panas_multichain` usando `git subtree`, preservando historia.

Script de integración
- Ejecuta el script para clonar `panas_multichain` y sumar ambos repos:

```
./scripts/merge_panas_repos.sh
```

Parámetros opcionales (variables de entorno)
- `PANAS_MULTICHAIN_URL`: URL del repo destino (por defecto GitHub oficial).
- `PANAS_TOKEN_URL`: URL de PANAS-TOKEN.
- `PANAS_TOKEN_M_URL`: URL de panas-token.M.
- `DEST_DIR`: carpeta de checkout (`panas_multichain`).
- `DEST_BRANCH`: rama de trabajo (`merge/panas-tokens`).
- `PREFIX_A`: prefijo destino para PANAS-TOKEN (`integrations/PANAS-TOKEN`).
- `PREFIX_B`: prefijo destino para panas-token.M (`integrations/panas-token.M`).
- `SQUASH`: `1` para squash de historia; `0` para historia completa (recomendado).

Ejemplos
```
# Historia completa en prefijos por defecto
./scripts/merge_panas_repos.sh

# Squash de historia y prefijos personalizados
SQUASH=1 PREFIX_A=modules/PANAS-TOKEN PREFIX_B=modules/panas-token.M ./scripts/merge_panas_repos.sh
```

Notas
- `git subtree` evita dependencias de submodules y permite trabajar sobre el contenido integrado directamente.
- Si deseas sincronizar cambios futuros, puedes usar `git subtree pull` con los mismos parámetros para cada prefijo.

Workflows de GitHub Actions
- `.github/workflows/subtree-sync.yml`
  - Sincroniza periódicamente (o manual) los upstreams:
    - `panacea-icono/PANAS-TOKEN` → `integrations/PANAS-TOKEN`
    - `panacea-icono/panas-token.M` → `integrations/panas-token.M`
  - Dispara manualmente desde “Actions → Subtree Sync” (opción `squash`).
  - Abre PR automático con los cambios.

- `.github/workflows/subtree-add.yml`
  - Agrega un nuevo repo como subtree vía `workflow_dispatch`.
  - Inputs: `repo_url`, `prefix`, `branch` (opcional), `squash` (opcional).
  - Crea una rama y PR con la importación.

Permisos
- Ambos workflows usan `GITHUB_TOKEN` con permisos `contents: write` y `pull-requests: write`.
- Si la rama `main` está protegida, los PRs se pueden mergear con revisión.
