import json
import os

STATE_FILE = "trinity_runtime/state.json"

SYSTEM_TOKEN = "TRINITY_SYSTEM_UI"

AUDIO_PRESETS = {
    "music": 70,
    "game": 85,
    "movie": 60,
    "call": 50
}

DEFAULT_STATE = {
    "power_profile": "balanced",
    "brightness": 50,
    "volume": 70,
    "last_volume": 70,
    "muted": False,
    "audio_profile": "music"
}


def _ensure_state():
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    if not os.path.isfile(STATE_FILE):
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_STATE, f, indent=2)


def get_state():
    _ensure_state()
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def set_state(key, value):
    state = get_state()
    state[key] = value
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def apply_audio_profile(profile):
    if profile not in AUDIO_PRESETS:
        raise ValueError("Invalid audio profile")

    volume = AUDIO_PRESETS[profile]
    state = get_state()

    state["audio_profile"] = profile
    state["volume"] = volume
    state["last_volume"] = volume
    state["muted"] = False

    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

    return state

