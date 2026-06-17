import json
import os

REGISTRY_ROOT = "trinity_runtime/registry"


def list_installed_apps():
    apps = []

    if not os.path.isdir(REGISTRY_ROOT):
        return apps

    for fname in os.listdir(REGISTRY_ROOT):
        if not fname.endswith(".json"):
            continue

        path = os.path.join(REGISTRY_ROOT, fname)
        try:
            with open(path, "r", encoding="utf-8") as f:
                apps.append(json.load(f))
        except Exception as e:
            print(f"Aviso: erro ao ler {fname}: {e}")

    return apps
