from trinity.core.registry import list_installed_apps


def render():
    apps = list_installed_apps()

    print("=== TrinityOS Control Center ===\n")

    if not apps:
        print("Nenhum app instalado.")
        return

    for app in apps:
        print(f"• {app['name']}")
        print(f"  ID: {app['id']}")
        print(f"  Versão: {app['version']}")
        print()


if __name__ == "__main__":
    render()
from trinity.services.power.src.trinity_power import (
    set_power_profile,
    get_power_profile
)


def power_menu():
    print("\n=== Power Profiles ===")
    print("1) performance")
    print("2) balanced")
    print("3) battery")

    choice = input("Escolha o perfil: ").strip()
    mapping = {"1": "performance", "2": "balanced", "3": "battery"}

    if choice in mapping:
        profile = mapping[choice]
        state = set_power_profile(profile)
        print(f"Perfil aplicado: {state['power_profile']}")
    else:
        print("Opção inválida")


if __name__ == "__main__":
    render()
    power_menu()
