from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea
from PyQt6.QtCore import Qt


class InstructionsScreen(QWidget):
    def __init__(self, on_complete):
        super().__init__()
        self.on_complete = on_complete
        self._build_ui()

    def _build_ui(self):
        main = QVBoxLayout()
        main.setSpacing(0)
        main.setContentsMargins(60, 20, 60, 20)

        # Title
        title = QLabel("Study Instructions")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 30px; 
            font-weight: bold; 
            color: #000000;
        """)
        main.addWidget(title)
        
        main.addSpacing(5)
        
        # Subtitle
        subtitle = QLabel("Please read the following information carefully")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("""
            font-size: 22px; 
            color: #7f8c8d;
        """)
        main.addWidget(subtitle)

        main.addSpacing(20)

        # Scrollable content area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("""
            QScrollArea {
                border: 1px solid #e0e0e0;
                background-color: white;
            }
        """)

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(0)
        content_layout.setContentsMargins(40, 20, 40, 20)

        # Instructions text
        instructions = [
            ("Welcome", 
             "Thank you for participating in this vibrotactile perception study. This experiment explores how people associate tactile sensations with visual properties like colour and shape."),
            
            ("What You'll Do", 
             "You will wear a haptic vest that delivers vibration patterns to your torso. After feeling each pattern, you will select colours and shapes that best match your perception of the vibration."),
            
            ("Study Structure", 
             "The study consists of three rounds:\n\n"
             "Round 1 (Colour): You will feel vibrotactile patterns. For each one, select the colour and brightness level that best matches the sensation.\n\n"
             "Round 2 (Shape): You will feel vibrotactile patterns. For each one, select the shape (from angular to rounded) that best matches the sensation.\n\n"
             "Round 3 (Combined): You will feel vibrotactile patterns. For each one, select both a colour and a shape that match your experience."),
            
            ("Practice Trials", 
             "Before the main experiment begins, you will complete 5 practice trials to familiarize yourself with the vibrations and response interface. These practice responses will not be analyzed."),
            
            ("Breaks", 
             "Short 3-minute breaks will be offered between rounds to help you stay comfortable and focused."),
            
            ("Your Task", 
             "There are no right or wrong answers. We are interested in your personal, intuitive associations between what you feel and what you see. Please respond based on your immediate impression."),
            
            ("Duration", 
             "The entire session will take approximately 45-60 minutes, including breaks."),
            
            ("Important Information", 
             "Please inform the researcher immediately if you feel any discomfort. You may withdraw from the study at any time without penalty. All your responses are anonymous and will be kept confidential."),
        ]

        for heading, text in instructions:
            # Section heading
            heading_label = QLabel(heading)
            heading_label.setStyleSheet("""
                font-size: 24px; 
                font-weight: bold; 
                color: #000000;
            """)
            heading_label.setWordWrap(True)
            content_layout.addWidget(heading_label)
            
            content_layout.addSpacing(3)  # Minimal gap between header and description

            # Section text
            text_label = QLabel(text)
            text_label.setStyleSheet("""
                font-size: 22px; 
                color: #555555; 
                line-height: 1.5;
            """)
            text_label.setWordWrap(True)
            content_layout.addWidget(text_label)
            
            content_layout.addSpacing(15)  # Larger gap between sections

        scroll.setWidget(content)
        main.addWidget(scroll, stretch=1)

        main.addSpacing(15)

        # Confirmation text
        confirm_label = QLabel(
            "By clicking 'Begin', you confirm that you have read and understood these instructions."
        )
        confirm_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        confirm_label.setStyleSheet("""
            font-size: 21px; 
            color: #888888; 
            font-style: italic;
        """)
        confirm_label.setWordWrap(True)
        main.addWidget(confirm_label)

        main.addSpacing(12)

        # Begin button
        begin_btn = QPushButton("Begin Practice Trials")
        begin_btn.setFixedWidth(240)
        begin_btn.setStyleSheet("""
            QPushButton {
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
            }
        """)
        begin_btn.clicked.connect(self.on_complete)
        main.addWidget(begin_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(main)