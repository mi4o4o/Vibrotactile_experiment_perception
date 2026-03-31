from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFrame
from PyQt6.QtCore import Qt


class PracticeCompleteScreen(QWidget):
    """
    Transition screen shown after practice trials finish.
    Tells the participant the main round is about to begin.
    """
    
    def __init__(self, on_complete):
        super().__init__()
        self.on_complete = on_complete
        self._build_ui()
    
    def _build_ui(self):
        main = QVBoxLayout()
        main.setSpacing(0)
        main.setContentsMargins(80, 50, 80, 50)
        
        # Stored as an attribute so set_round_info can update the text
        self.title = QLabel("Practice Complete")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("""
            font-size: 32px; 
            font-weight: bold; 
            color: #2c3e50;
        """)
        main.addWidget(self.title)
        
        main.addSpacing(30)
        
        message_frame = QFrame()
        message_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-radius: 12px;
                padding: 30px;
            }
        """)
        
        message_layout = QVBoxLayout(message_frame)
        message_layout.setSpacing(20)
        message_layout.setContentsMargins(40, 30, 40, 30)
        
        # Stored as an attribute so set_round_info can update the text
        self.message_text = QLabel(
            "Great! You've completed the practice trials.<br><br>"
            "You should now be familiar with:<br>"
            "• How the vibrotactile patterns feel<br>"
            "• How to select answer option<br>"
            "• The overall flow of each trial<br><br>"
            "<b>The main experiment will now begin.</b><br><br>"
            "Remember: there are no right or wrong answers. "
            ""
        )
        self.message_text.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.message_text.setStyleSheet("""
            font-size: 18px; 
            color: #2c3e50;
            line-height: 1.6;
        """)
        self.message_text.setWordWrap(True)
        message_layout.addWidget(self.message_text)
        
        main.addWidget(message_frame)
        
        main.addSpacing(40)
        
        ready_label = QLabel("When you're ready, click the button below to begin the main round")
        ready_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ready_label.setStyleSheet("""
            font-size: 16px; 
            color: #7f8c8d;
            font-style: italic;
        """)
        main.addWidget(ready_label)
        
        main.addSpacing(20)
        
        begin_btn = QPushButton("Begin Main Round")
        begin_btn.setFixedWidth(300)
        begin_btn.setFixedHeight(55)
        begin_btn.setStyleSheet("""
            QPushButton {
                font-size: 18px;
                font-weight: bold;
                padding: 15px;
            }
        """)
        begin_btn.clicked.connect(self.on_complete)
        main.addWidget(begin_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.setLayout(main)
    
    def set_round_info(self, round_name: str):
        """
        Update the title and message to match the round that just finished.
        Called before showing this screen so the text is always round-specific.
        """
        self.title.setText(f"{round_name} Practice Complete")
        
        if round_name == "Colour":
            task_description = "• How to select colours and brightness levels"
        elif round_name == "Shape":
            task_description = "• How to select shapes using the slider"
        elif round_name == "Combined":
            task_description = "• How to select both colours and shapes together"
        else:
            task_description = "• How to select your answer"
        
        self.message_text.setText(
            f"Great! You've completed the {round_name.lower()} practice trials.<br><br>"
            "You should now be familiar with:<br>"
            "• How the vibrotactile patterns feel<br>"
            f"{task_description}<br>"
            "• The overall flow of each trial<br><br>"
            f"<b>The main {round_name.lower()} round will now begin.</b><br><br>"
            "Remember: there are no right or wrong answers."
        )