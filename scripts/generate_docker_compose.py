#!/usr/bin/env python3
import json
from pathlib import Path

# Lee modules.json y genera docker-compose.yml para servicios que tengan Dockerfile

ROOT = Path(__file__).resolve().parent.parent
modules_file = ROOT / "modules.json"
compose_file = ROOT / "docker-compose.yml"

mods = json.loads(modules_file.read_text()) if modules_file.exists() else {}

services = {}
for name, spec in mods.items():
    path = spec.get("path", name)
    port = int(spec.get("port", 0))
    context = ROOT / path
    dockerfile = context / "Dockerfile"
    if dockerfile.exists():
        svc_name = name.replace("/", "_")
        services[svc_name] = {
            "build": {
                "context": path
            },
            "container_name": f"{svc_name}",
            "restart": "unless-stopped",
            "env_file": [".env"],
        }
        if port:
            services[svc_name]["ports"] = [f"{port}:{port}"]
    else:
        # No Dockerfile, omitir del compose
        pass

compose = {
    "version": "3.9",
    "services": services
}


def dump_yaml(obj, indent=0):
    sp = "  " * indent
    if isinstance(obj, dict):
        out = []
        for k, v in obj.items():
            if isinstance(v, (dict, list)):
                out.append(f"{sp}{k}:")
                out.append(dump_yaml(v, indent + 1))
            else:
                out.append(f"{sp}{k}: {v}")
        return "\n".join(out)
    elif isinstance(obj, list):
        out = []
        for item in obj:
            if isinstance(item, (dict, list)):
                out.append(f"{sp}-")
                out.append(dump_yaml(item, indent + 1))
            else:
                out.append(f"{sp}- {item}")
        return "\n".join(out)
    else:
        return f"{sp}{obj}"


compose_file.write_text(dump_yaml(compose) + "\n")
print(f"Generado {compose_file} con {len(services)} servicio(s).")
