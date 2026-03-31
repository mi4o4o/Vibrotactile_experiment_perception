from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFrame
from PyQt6.QtCore import Qt


class RoundInstructionScreen(QWidget):
    """
    Instruction screen shown before each round.
    Displays round-specific instructions and examples.
    """
    
    def __init__(self, on_complete):
        super().__init__()
        self.on_complete = on_complete
        self._build_ui()
    
    def _build_ui(self):
        main = QVBoxLayout()
        main.setSpacing(0)
        main.setContentsMargins(80, 50, 80, 50)
        
        # Round title
        self.title = QLabel("Round 1: Colour")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("""
            font-size: 32px; 
            font-weight: bold; 
            color: #2c3e50;
        """)
        main.addWidget(self.title)
        
        main.addSpacing(30)
        
        # Instructions container with background
        instructions_frame = QFrame()
        instructions_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-radius: 12px;
                padding: 30px;
            }
        """)
        
        instructions_layout = QVBoxLayout(instructions_frame)
        instructions_layout.setSpacing(20)
        instructions_layout.setContentsMargins(40, 30, 40, 30)
        
        # Main instruction text
        self.instruction_text = QLabel()
        self.instruction_text.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.instruction_text.setStyleSheet("""
            font-size: 18px; 
            color: #2c3e50;
            line-height: 1.6;
        """)
        self.instruction_text.setWordWrap(True)
        instructions_layout.addWidget(self.instruction_text)
        
        main.addWidget(instructions_frame)
        
        main.addSpacing(40)
        
        # Ready message
        ready_label = QLabel("When you're ready, click the button below to begin")
        ready_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ready_label.setStyleSheet("""
            font-size: 16px; 
            color: #7f8c8d;
            font-style: italic;
        """)
        main.addWidget(ready_label)
        
        main.addSpacing(20)
        
        # Begin button
        self.begin_btn = QPushButton("Begin Round")
        self.begin_btn.setFixedWidth(300)
        self.begin_btn.setFixedHeight(55)
        self.begin_btn.setStyleSheet("""
            QPushButton {
                font-size: 18px;
                font-weight: bold;
                padding: 15px;
            }
        """)
        self.begin_btn.clicked.connect(self.on_complete)
        main.addWidget(self.begin_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.setLayout(main)
    
    def set_round_info(self, round_name: str, instructions: str):
        """
        Update the screen with round-specific information.
        
        Args:
            round_name: Name of the round (e.g., "Round 1: Colour")
            instructions: Detailed instruction text for this round
        """
        self.title.setText(round_name)
        self.instruction_text.setText(instructions)


# Predefined instructions for each round
COLOR_ROUND_INSTRUCTIONS = """<b>In this round, you will:</b><br><br>

- Feel a vibrotactile pattern through the vest<br>
- Select the colour that you think best matches what you felt<br>
- There are no right or wrong answers, trust your intuition<br><br>

<b>How it works:</b><br><br>

1. You will feel a vibration pattern<br>
2. Choose a colour from the palette by clicking on any shade<br>
3. The selected colour will appear in the preview box<br>
4. Click "Continue" to move to the next trial<br><br>

<b>Practice Trials:</b><br><br>

Before the main round begins, you will complete <b>4 practice trials</b> to familiarize yourself with the vibrations and interface. These responses will not be included in the final data.<br><br>

After the practice trials, the main round will begin with <b>30 trials</b>."""

SHAPE_ROUND_INSTRUCTIONS = """<b>In this round, you will:</b><br><br>

- Feel a vibrotactile pattern through the vest<br>
- Select the shape that best matches what you felt<br>
- Use the slider to choose from angular to round shapes<br><br>

<b>How it works:</b><br><br>

1. You will feel a vibration pattern<br>
2. Move the slider to select a shape from the range<br>
3. The shape preview will update as you move the slider<br>
4. Click "Continue" to move to the next trial<br><br>

<b>Practice Trials:</b><br><br>

Before the main round begins, you will complete <b>4 practice trials</b> to familiarize yourself with the different vibration patterns and the shape selection interface. These responses will not be included in the final data.<br><br>

After the practice trials, the main round will begin with <b>18 trials</b>."""

COMBINED_ROUND_INSTRUCTIONS = """<b>In this round, you will:</b><br><br>

- Feel a vibrotactile pattern through the vest<br>
- Select both a <b>colour and shape</b> that best match what you felt<br>
- The shape will fill with your selected colour as a preview<br><br>
- Please choose the shape–color combination that best matches the vibration as one whole impression, not as two separate choices.<br><br>

<b>How it works:</b><br><br>

1. You will feel a vibration pattern<br>
2. Choose a colour by clicking on any shade from the palette<br>
3. Move the slider to select a shape<br>
4. The shape will display filled with your chosen colour<br>
5. You can adjust both selections before continuing<br>
6. Click "Continue" to move to the next trial<br><br>

<b>Practice Trials:</b><br><br>

Before the main round begins, you will complete <b>4 practice trials</b> to familiarize yourself with selecting both colour and shape together. These responses will not be included in the final data.<br><br>

After the practice trials, the main round will begin with <b>54 trials</b>."""