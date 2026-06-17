import sys
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

try:
    from installer import install_otn
except:
    print("Erro: módulo installer não encontrado. Crie installer.py dentro de src/")
    sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print("TrinityInstaller v0")
        print("Uso: python cli.py <arquivo.otn>")
        sys.exit(1)

    otn_path = sys.argv[1]

    try:
        record = install_otn(otn_path)
        print("✔ Instalação concluída:")
        print(json.dumps(record, ensure_ascii=False, indent=2))
        sys.exit(0)
    except Exception as e:
        print("✖ Falha na instalação:")
        print(str(e))
        sys.exit(2)


if __name__ == "__main__":
    main()
