from trinity.core.state import set_state, get_state

PROFILES = ["performance", "balanced", "battery"]


def set_power_profile(profile: str):
    if profile not in PROFILES:
        raise ValueError(f"Perfil inválido: {profile}")

    set_state("power_profile", profile)
    return get_state()


def get_power_profile():
    return get_state().get("power_profile", "balanced")
