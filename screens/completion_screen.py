from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout


class CompletionScreen(QWidget):
    def __init__(self, on_save, on_restart):
        super().__init__()
        self.on_save = on_save
        self.on_restart = on_restart
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)

        self.title = QLabel("Experiment complete")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("font-size: 22px; font-weight: bold;")
        layout.addWidget(self.title)

        self.info_label = QLabel("Thank you for participating!")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.info_label)

        self.details_label = QLabel("")
        self.details_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.details_label)

        row = QHBoxLayout()

        restart_btn = QPushButton("Start new session")
        restart_btn.clicked.connect(self.on_restart)
        row.addWidget(restart_btn)

        layout.addLayout(row)
        self.setLayout(layout)

    def set_summary(self, participant_id, n_trials):
        self.details_label.setText(f"Participant ID: {participant_id}")
