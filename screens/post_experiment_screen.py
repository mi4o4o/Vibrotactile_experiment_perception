from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QRadioButton, QButtonGroup, QScrollArea, QFrame
)
from PyQt6.QtCore import Qt


class PostExperimentScreen(QWidget):
    """
    Optional questionnaire shown at the end of the session.
    Collects qualitative feedback to help contextualize the quantitative results.
    """
    
    def __init__(self, on_complete):
        super().__init__()
        self.on_complete = on_complete
        self._build_ui()
    
    def _build_ui(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none; 
                background-color: white;
            }
            QScrollBar:vertical {
                background: #f0f0f0;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #c0c0c0;
                border-radius: 6px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background: #a0a0a0;
            }
        """)
        
        container = QWidget()
        container.setStyleSheet("background-color: white;")
        main = QVBoxLayout(container)
        main.setSpacing(35)
        main.setContentsMargins(70, 50, 70, 50)
        
        title = QLabel("Post-Experiment Questions")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 30px; 
            font-weight: bold; 
            color: #2c3e50;
        """)
        main.addWidget(title)
        
        subtitle = QLabel("Please take a moment to share your experience with the experiment")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("""
            font-size: 17px; 
            color: #7f8c8d;
            margin-bottom: 10px;
        """)
        subtitle.setWordWrap(True)
        main.addWidget(subtitle)
        
        main.addSpacing(20)
        
        # Q1: Overall difficulty rating (5-point scale) + optional free text
        q1_container = self._create_question_container()
        q1_layout = QVBoxLayout(q1_container)
        q1_layout.setSpacing(18)
        
        q1_label = QLabel(
            "<b>1.</b> How easy or difficult was it to choose a visual stimulus "
            "(colour, shape, or combined option) that matched the vibrotactile pattern?"
        )
        q1_label.setWordWrap(True)
        q1_label.setStyleSheet("font-size: 17px; color: #2c3e50; line-height: 1.5;")
        q1_layout.addWidget(q1_label)
        
        scale_layout = QVBoxLayout()
        scale_layout.setSpacing(12)
        
        self.difficulty_group = QButtonGroup(self)
        difficulty_options = [
            "Very Easy",
            "Easy",
            "Neutral",
            "Difficult",
            "Very Difficult"
        ]
        
        for option in difficulty_options:
            radio = QRadioButton(option)
            radio.setStyleSheet("""
                QRadioButton {
                    font-size: 16px;
                    padding: 8px;
                    color: #2c3e50;
                    background-color: transparent;
                }
                QRadioButton::indicator {
                    width: 20px;
                    height: 20px;
                    border-radius: 10px;
                    border: 2px solid #888888;
                    background: white;
                }
                QRadioButton::indicator:checked {
                    background: #888888;
                    border: 2px solid #888888;
                }
                QRadioButton::indicator:hover {
                    border: 2px solid #666666;
                }
            """)
            self.difficulty_group.addButton(radio)
            scale_layout.addWidget(radio)
        
        q1_layout.addLayout(scale_layout)
        
        q1_text_label = QLabel("Additional comments (optional):")
        q1_text_label.setStyleSheet("font-size: 15px; color: #555; margin-top: 10px;")
        q1_layout.addWidget(q1_text_label)
        
        self.q1_text = QTextEdit()
        self.q1_text.setPlaceholderText("Describe your experience...")
        self.q1_text.setMaximumHeight(90)
        self.q1_text.setStyleSheet("""
            QTextEdit {
                font-size: 15px;
                padding: 10px;
                border: 2px solid #ddd;
                border-radius: 8px;
                background: white;
            }
            QTextEdit:focus {
                border: 2px solid #888888;
            }
        """)
        q1_layout.addWidget(self.q1_text)
        
        main.addWidget(q1_container)
        
        # Q2: Which trials felt easier or more intuitive
        q2_container = self._create_question_container()
        q2_layout = QVBoxLayout(q2_container)
        q2_layout.setSpacing(18)
        
        q2_label = QLabel(
            "<b>2.</b> Did some trials feel easier or more intuitive than others? "
            "If yes, which ones and why?"
        )
        q2_label.setWordWrap(True)
        q2_label.setStyleSheet("font-size: 17px; color: #2c3e50; line-height: 1.5;")
        q2_layout.addWidget(q2_label)
        
        self.q2_text = QTextEdit()
        self.q2_text.setPlaceholderText(
            "For example: 'The color trials felt easier because...' or "
            "'Some shape patterns were more obvious...'"
        )
        self.q2_text.setMinimumHeight(130)
        self.q2_text.setStyleSheet("""
            QTextEdit {
                font-size: 15px;
                padding: 10px;
                border: 2px solid #ddd;
                border-radius: 8px;
                background: white;
            }
            QTextEdit:focus {
                border: 2px solid #888888;
            }
        """)
        q2_layout.addWidget(self.q2_text)
        
        main.addWidget(q2_container)
        
        # Q3: Open-ended comments about anything else they noticed
        q3_container = self._create_question_container()
        q3_layout = QVBoxLayout(q3_container)
        q3_layout.setSpacing(18)
        
        q3_label = QLabel(
            "<b>3.</b> Do you have any additional comments, suggestions, or observations "
            "about the experiment? This can include anything about the interface, "
            "the vibrotactile patterns, the decision process, or anything else you found notable."
        )
        q3_label.setWordWrap(True)
        q3_label.setStyleSheet("font-size: 17px; color: #2c3e50; line-height: 1.5;")
        q3_layout.addWidget(q3_label)
        
        self.q3_text = QTextEdit()
        self.q3_text.setPlaceholderText(
            "Share any thoughts about the experiment, interface design, "
            "vibration patterns, or anything else..."
        )
        self.q3_text.setMinimumHeight(130)
        self.q3_text.setStyleSheet("""
            QTextEdit {
                font-size: 15px;
                padding: 10px;
                border: 2px solid #ddd;
                border-radius: 8px;
                background: white;
            }
            QTextEdit:focus {
                border: 2px solid #888888;
            }
        """)
        q3_layout.addWidget(self.q3_text)
        
        main.addWidget(q3_container)
        
        main.addSpacing(25)
        
        note = QLabel(
            " "
        )
        note.setAlignment(Qt.AlignmentFlag.AlignCenter)
        note.setStyleSheet("""
            font-size: 14px; 
            color: #7f8c8d;
            font-style: italic;
        """)
        note.setWordWrap(True)
        main.addWidget(note)
        
        main.addSpacing(15)
        
        submit_btn = QPushButton("Submit and Continue")
        submit_btn.setFixedWidth(300)
        submit_btn.setFixedHeight(55)
        submit_btn.setStyleSheet("""
            QPushButton {
                font-size: 18px;
                font-weight: bold;
                padding: 15px;
            }
        """)
        submit_btn.clicked.connect(self._handle_submit)
        main.addWidget(submit_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        main.addSpacing(30)
        
        scroll.setWidget(container)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(scroll)
    
    def _create_question_container(self):
        """Returns a styled card frame to wrap each question in."""
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background-color: #fafbfc;
                border-radius: 12px;
                padding: 25px;
                border: 1px solid #e1e4e8;
            }
        """)
        return container
    
    def _handle_submit(self):
        """Collect all responses into a dictionary and pass them to the callback."""
        difficulty = None
        selected_button = self.difficulty_group.checkedButton()
        if selected_button:
            difficulty = selected_button.text()
        
        q1_additional = self.q1_text.toPlainText().strip()
        q2_response = self.q2_text.toPlainText().strip()
        q3_response = self.q3_text.toPlainText().strip()
        
        responses = {
            'difficulty_rating': difficulty,
            'difficulty_additional': q1_additional,
            'easier_trials': q2_response,
            'additional_comments': q3_response
        }
        
        self.on_complete(responses)
    
    def reset(self):
        """Clear all fields so the screen is ready for a new participant."""
        selected = self.difficulty_group.checkedButton()
        if selected:
            self.difficulty_group.setExclusive(False)
            selected.setChecked(False)
            self.difficulty_group.setExclusive(True)
        
        self.q1_text.clear()
        self.q2_text.clear()
        self.q3_text.clear()