import json
import os
import zipfile
from datetime import datetime
from typing import Dict, Any


class InstallError(Exception):
    pass


def ensure_dir(p: str) -> None:
    os.makedirs(p, exist_ok=True)


def install_otn(otn_path: str, runtime_root: str = "trinity_runtime") -> Dict[str, Any]:
    """
    Instala um .otn em um runtime local (simulação v0).
    """
    if not os.path.isfile(otn_path):
        raise InstallError(f"Arquivo não encontrado: {otn_path}")

    ensure_dir(runtime_root)
    apps_root = os.path.join(runtime_root, "apps")
    reg_root = os.path.join(runtime_root, "registry")
    ensure_dir(apps_root)
    ensure_dir(reg_root)

    with zipfile.ZipFile(otn_path, "r") as z:
        # lê manifest
        try:
            with z.open("otn-manifest.json") as f:
                data = json.loads(f.read().decode("utf-8"))
        except KeyError:
            raise InstallError("Pacote .otn sem otn-manifest.json")

        try:
            pkg = data["package"]
            pkg_id = pkg["id"]
            name = pkg.get("name", pkg_id)
            version = pkg["version"]
            pkg_type = pkg.get("type", "unknown")
            target = pkg.get("target", "openharmony")
        except KeyError as e:
            raise InstallError(f"Manifest inválido, campo ausente: {e}")

        # diretorios de instalação
        target_dir = os.path.join(apps_root, pkg_id, version)
        staging_dir = target_dir + ".staging"

        # limpa staging anterior
        if os.path.exists(staging_dir):
            import shutil
            shutil.rmtree(staging_dir, ignore_errors=True)

        ensure_dir(staging_dir)

        # extrai tudo de payload/ para staging
        has_payload = False
        for name_in_zip in z.namelist():
            if name_in_zip.startswith("payload/") and not name_in_zip.endswith("/"):
                has_payload = True
                rel_path = name_in_zip[len("payload/"):]
                out_path = os.path.join(staging_dir, rel_path)
                ensure_dir(os.path.dirname(out_path))
                with z.open(name_in_zip) as src, open(out_path, "wb") as dst:
                    dst.write(src.read())

        if not has_payload:
            raise InstallError("Pacote inválido: não há arquivos em payload/")

        # promove staging -> target
        import shutil
        if os.path.exists(target_dir):
            shutil.rmtree(target_dir, ignore_errors=True)
        ensure_dir(os.path.dirname(target_dir))
        os.rename(staging_dir, target_dir)

        # grava registro
        record = {
            "id": pkg_id,
            "name": name,
            "version": version,
            "type": pkg_type,
            "target": target,
            "installed_at": datetime.utcnow().isoformat() + "Z",
            "install_path": target_dir.replace("\\", "/"),
            "source": os.path.basename(otn_path),
        }

        with open(os.path.join(reg_root, f"{pkg_id}.json"), "w", encoding="utf-8") as f:
            json.dump(record, f, ensure_ascii=False, indent=2)

        return record
