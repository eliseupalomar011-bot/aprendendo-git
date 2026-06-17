import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from trinity.core.state import (
    get_state,
    set_state,
    apply_audio_profile,
    SYSTEM_TOKEN
)
from trinity.services.power.src.trinity_power import (
    set_power_profile,
    get_power_profile
)

HOST = "localhost"
PORT = 8765


def is_authorized(handler):
    token = handler.headers.get("X-Trinity-Token")
    return token == SYSTEM_TOKEN


class TrinityAPI(BaseHTTPRequestHandler):

    def _send(self, data, code=200):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, X-Trinity-Token")
        self.end_headers()

    def do_GET(self):
        state = get_state()

        if self.path == "/power":
            self._send({"profile": get_power_profile()})

        elif self.path == "/brightness":
            self._send({"value": state.get("brightness", 50)})

        elif self.path == "/volume":
            self._send({
                "value": state.get("volume", 70),
                "muted": state.get("muted", False)
            })

        elif self.path == "/audio/profile":
            self._send({"profile": state.get("audio_profile", "music")})

        else:
            self._send({"error": "Not found"}, 404)

    def do_POST(self):
        if not is_authorized(self):
            self._send({"error": "Permission denied"}, 403)
            return

        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length)) if length else {}
        state = get_state()

        if self.path == "/power":
            try:
                new_state = set_power_profile(body.get("profile"))
                self._send(new_state)
            except Exception as e:
                self._send({"error": str(e)}, 400)

        elif self.path == "/brightness":
            value = max(0, min(100, int(body.get("value", 50))))
            set_state("brightness", value)
            self._send({"value": value})

        elif self.path == "/volume":
            value = max(0, min(100, int(body.get("value", 70))))
            set_state("volume", value)
            set_state("muted", value == 0)
            self._send({"value": value})

        elif self.path == "/mute":
            if state.get("muted"):
                restore = state.get("last_volume", 70)
                set_state("volume", restore)
                set_state("muted", False)
                self._send({"muted": False, "volume": restore})
            else:
                set_state("last_volume", state.get("volume", 70))
                set_state("volume", 0)
                set_state("muted", True)
                self._send({"muted": True, "volume": 0})

        elif self.path == "/audio/profile":
            try:
                new_state = apply_audio_profile(body.get("profile"))
                self._send(new_state)
            except Exception as e:
                self._send({"error": str(e)}, 400)

        else:
            self._send({"error": "Not found"}, 404)


def run():
    print(f"TrinityAPI running at http://{HOST}:{PORT}")
    HTTPServer((HOST, PORT), TrinityAPI).serve_forever()


if __name__ == "__main__":
    run()
