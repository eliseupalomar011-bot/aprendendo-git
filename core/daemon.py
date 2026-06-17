from trinity.core.ipc import start_ipc
from trinity.core.state import (
    get_state,
    set_state,
    apply_audio_profile
)


def handle_request(req):
    action = req.get("action")

    if action == "get_state":
        return get_state()

    elif action == "set":
        key = req.get("key")
        value = req.get("value")
        set_state(key, value)
        return get_state()

    elif action == "audio_profile":
        return apply_audio_profile(req.get("profile"))

    elif action == "mute":
        state = get_state()
        if state.get("muted"):
            set_state("volume", state.get("last_volume", 70))
            set_state("muted", False)
        else:
            set_state("last_volume", state.get("volume", 70))
            set_state("volume", 0)
            set_state("muted", True)
        return get_state()

    return {"error": "Unknown action"}


if __name__ == "__main__":
    print("🧠 TrinityCore daemon started")
    start_ipc(handle_request)

