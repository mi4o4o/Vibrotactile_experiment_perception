from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QTimer


class PatternPlaybackScreen(QWidget):
    def __init__(self, on_finished, play_vibration):
        super().__init__()
        self.on_finished = on_finished
        self.play_vibration = play_vibration
        self.current_pattern = None
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label = QLabel("Playing vibrotactile pattern…")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("font-size: 50px; font-weight: bold;")

        layout.addWidget(self.label)
        self.setLayout(layout)

    def set_trial_info(self, trial, total):
        self.label.setText(f"Playing vibrotactile pattern…\nTrial {trial} of {total}")

    def set_pattern(self, pattern):
        self.current_pattern = pattern

    def start(self):
        if self.current_pattern:
            from utils.haptics import play_haptic_pattern
            play_haptic_pattern(
                event_name=self.current_pattern.event_name,
                intensity=self.current_pattern.intensity,
                duration=self.current_pattern.duration
            )
            print(f"Playing pattern: {self.current_pattern}")
        else:
            print("WARNING: No pattern set, using legacy vibration")
            self.play_vibration()

        QTimer.singleShot(3500, self.on_finished)