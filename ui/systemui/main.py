import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QLabel, QPushButton, QSlider
)
from PySide6.QtCore import Qt

from trinity.ui.systemui.ipc_bridge import ipc_call


class TrinitySystemUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TrinityOS Control Center")
        self.setFixedSize(320, 480)

        layout = QVBoxLayout()

        title = QLabel("TrinityOS Next")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Volume
        layout.addWidget(QLabel("Volume"))
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.valueChanged.connect(self.set_volume)
        layout.addWidget(self.volume_slider)

        self.mute_btn = QPushButton("Mute")
        self.mute_btn.clicked.connect(self.toggle_mute)
        layout.addWidget(self.mute_btn)

        # Audio Profiles
        layout.addWidget(QLabel("Audio Profile"))
        for profile in ["music", "game", "movie", "call"]:
            btn = QPushButton(profile.capitalize())
            btn.clicked.connect(
                lambda _, p=profile: self.set_audio_profile(p)
            )
            layout.addWidget(btn)

        self.setLayout(layout)
        self.refresh_state()

    def refresh_state(self):
        state = ipc_call({"action": "get_state"})
        self.volume_slider.setValue(state.get("volume", 70))

    def set_volume(self, value):
        ipc_call({"action": "set", "key": "volume", "value": value})

    def toggle_mute(self):
        ipc_call({"action": "mute"})
        self.refresh_state()

    def set_audio_profile(self, profile):
        ipc_call({"action": "audio_profile", "profile": profile})
        self.refresh_state()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = TrinitySystemUI()
    ui.show()
    sys.exit(app.exec())
