from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QComboBox,
    QPushButton, QMessageBox
)

from data.demographics import DemographicsData


class DemographicsScreen(QWidget):
    def __init__(self, on_complete):
        super().__init__()
        self.on_complete = on_complete
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)

        title = QLabel("Vibrotactile Perception Study")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
        layout.addWidget(title)

        subtitle = QLabel("Please provide the following information to begin")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("font-size: 14px; color: #555;")
        layout.addWidget(subtitle)

        # Participant ID
        id_label = QLabel("Participant ID")
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("Enter participant ID")
        self.id_input.setFixedWidth(260)

        # Age — ComboBox with actual ages
        age_label = QLabel("Age")
        self.age_combo = QComboBox()
        self.age_combo.addItem("Select...")

        for age in range(18, 91):  # ages 18–90
            self.age_combo.addItem(str(age))

        self.age_combo.setFixedWidth(260)

        # Gender
        gender_label = QLabel("Gender")
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Select...","Male", "Female", "Other", "Prefer not to say"])
        self.gender_combo.setFixedWidth(260)

        # Continue button
        continue_btn = QPushButton("Begin experiment")
        continue_btn.setFixedWidth(260)
        continue_btn.setStyleSheet("padding: 10px; font-size: 16px;")
        continue_btn.clicked.connect(self.handle_continue)

        # Add widgets
        for w in [
            id_label, self.id_input,
            age_label, self.age_combo,
            gender_label, self.gender_combo,
            continue_btn
        ]:
            w.setMaximumWidth(260)
            layout.addWidget(w, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def handle_continue(self):
        pid = self.id_input.text().strip()
        age_text = self.age_combo.currentText()
        gender = self.gender_combo.currentText()

        # Validate
        if not pid or age_text == "Select...":
            QMessageBox.warning(
                self, "Missing information",
                "Please enter a participant ID and select your age."
            )
            return

        age = int(age_text)

        demo = DemographicsData(participant_id=pid, age=age, gender=gender)
        self.on_complete(demo)
