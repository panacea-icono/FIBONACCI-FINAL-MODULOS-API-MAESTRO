#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Conector Hugging Face: lista y descarga tus modelos, datasets y Spaces.

Uso rápido:
  - Exporta tu token o colócalo en .env (HF_TOKEN o HUGGINGFACE_TOKEN)
  - Listar todo:    python3 scripts/hf_connect.py list
  - Listar modelos: python3 scripts/hf_connect.py list --type model
  - Descargar:      python3 scripts/hf_connect.py download --type model --id org/nombre

Descargas por defecto en:
  external/hf/models/ORG__NOMBRE
  external/hf/datasets/ORG__NOMBRE
  external/hf/spaces/ORG__NOMBRE
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path


def _load_env_token() -> str:
    # Carga token de entorno; intenta leer .env si existe (sin dependencias)
    token = os.getenv("HUGGINGFACE_TOKEN") or os.getenv("HF_TOKEN") or ""
    if token:
        return token
    # carga básica desde .env si no está exportado
    env_path = Path(".env")
    if env_path.exists():
        try:
            for line in env_path.read_text(encoding="utf-8").splitlines():
                if line.strip().startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                k = k.strip()
                v = v.strip().strip('"').strip("'")
                if k in ("HUGGINGFACE_TOKEN", "HF_TOKEN") and v:
                    return v
        except Exception:
            pass
    return ""


def _api():
    try:
        from huggingface_hub import HfApi
    except Exception as e:
        print("Install dependency: pip install huggingface_hub", file=sys.stderr)
        raise SystemExit(e)
    return HfApi()


def whoami(token: str) -> str:
    api = _api()
    try:
        info = api.whoami(token=token)
        return info.get("name") or ""
    except Exception:
        return ""


def list_assets(kind: str | None, author: str | None, token: str):
    api = _api()
    kinds = [kind] if kind else ["model", "dataset", "space"]
    results = {}
    for k in kinds:
        try:
            if k == "model":
                items = list(api.list_models(author=author, token=token))
            elif k == "dataset":
                items = list(api.list_datasets(author=author, token=token))
            elif k == "space":
                # list_spaces may not exist on very old versions
                items = list(api.list_spaces(author=author, token=token))  # type: ignore[attr-defined]
            else:
                items = []
        except Exception as e:
            print(f"[WARN] No se pudieron listar {k}s: {e}")
            items = []
        results[k] = [getattr(i, "id", str(i)) for i in items]
    return results


def sanitize_repo_id(repo_id: str) -> str:
    return repo_id.replace("/", "__")


def download_asset(kind: str, repo_id: str, dest_root: Path, token: str) -> Path:
    try:
        from huggingface_hub import snapshot_download
    except Exception as e:
        print("Install dependency: pip install huggingface_hub", file=sys.stderr)
        raise SystemExit(e)

    kind_map = {
        "model": ("models", "model"),
        "dataset": ("datasets", "dataset"),
        "space": ("spaces", "space"),
    }
    if kind not in kind_map:
        raise SystemExit(f"Tipo no soportado: {kind}")

    subdir, repo_type = kind_map[kind]
    dest_dir = dest_root / subdir / sanitize_repo_id(repo_id)
    dest_dir.mkdir(parents=True, exist_ok=True)

    local_dir = snapshot_download(
        repo_id=repo_id,
        repo_type=repo_type,  # type: ignore[arg-type]
        local_dir=dest_dir,
        token=token,
        local_dir_use_symlinks=False,
    )
    return Path(local_dir)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Conectar a Hugging Face (modelos/datasets/spaces)")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_list = sub.add_parser("list", help="Listar activos del usuario")
    p_list.add_argument("--type", choices=["model", "dataset", "space"], help="Tipo a listar")
    p_list.add_argument("--author", help="Usuario/organización (por defecto: el token actual)")

    p_dl = sub.add_parser("download", help="Descargar un activo")
    p_dl.add_argument("--type", required=True, choices=["model", "dataset", "space"], help="Tipo de repo")
    p_dl.add_argument("--id", required=True, help="ID del repo, ej. org/nombre")
    p_dl.add_argument("--dest", default="external/hf", help="Directorio raíz de descarga")

    args = parser.parse_args(argv)

    token = _load_env_token()
    if not token:
        print("[ERROR] Necesitas configurar HF_TOKEN o HUGGINGFACE_TOKEN en tu entorno o .env", file=sys.stderr)
        return 2

    if args.cmd == "list":
        author = args.author or whoami(token) or None
        res = list_assets(args.type, author, token)
        print("Autor:", author or "(desconocido)")
        for k, ids in res.items():
            print(f"\n{k.upper()}S ({len(ids)}):")
            for rid in ids:
                print(" -", rid)
        return 0

    if args.cmd == "download":
        dest_root = Path(args.dest)
        dest_root.mkdir(parents=True, exist_ok=True)
        local = download_asset(args.type, args.id, dest_root, token)
        print(f"Descargado en: {local}")
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

