from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QKeyEvent


class BreakScreen(QWidget):
    """
    Break screen with 3-minute countdown timer.
    Hidden feature: Press 'S' key to skip the break.
    """
    
    def __init__(self, on_complete):
        super().__init__()
        self.on_complete = on_complete
        self.remaining_seconds = 120  # 3 minutes = 180 seconds
        
        self._build_ui()
        self._start_timer()
    
    def _build_ui(self):
        main = QVBoxLayout()
        main.setSpacing(0)
        main.setContentsMargins(60, 80, 60, 80)
        
        # Title
        self.title = QLabel("Break Time")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("""
            font-size: 28px; 
            font-weight: bold; 
            color: #2c3e50;
        """)
        main.addWidget(self.title)
        
        main.addSpacing(30)
        
        # Instructions
        instructions = QLabel(
            "Please take a short break to rest.\n"
            "The next round will begin automatically when the timer reaches zero."
        )
        instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)
        instructions.setStyleSheet("""
            font-size: 14px; 
            color: #555555;
            line-height: 1.6;
        """)
        instructions.setWordWrap(True)
        main.addWidget(instructions)
        
        main.addSpacing(50)
        
        # Countdown timer display
        self.timer_label = QLabel("2:00")
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_label.setStyleSheet("""
            font-size: 72px; 
            font-weight: bold; 
            color: #2c3e50;
            background-color: #f5f5f5;
            border: 2px solid #cccccc;
            border-radius: 20px;
            padding: 40px;
        """)
        main.addWidget(self.timer_label)
        
        main.addSpacing(50)
        
        # Hint text
        hint = QLabel("Feel free to stretch, look away from the screen or relax.")
        hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hint.setStyleSheet("""
            font-size: 13px; 
            color: #7f8c8d;
            font-style: italic;
        """)
        hint.setWordWrap(True)
        main.addWidget(hint)
        
        main.addStretch()
        
        self.setLayout(main)
    
    def _start_timer(self):
        """Start the countdown timer"""
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_timer)
        self.timer.start(1000)  # Update every second
    
    def _update_timer(self):
        """Update the countdown display"""
        self.remaining_seconds -= 1
        
        if self.remaining_seconds <= 0:
            self.timer.stop()
            self.on_complete()
        else:
            self._update_display()
    
    def _update_display(self):
        """Update the timer display with current remaining time"""
        minutes = self.remaining_seconds // 60
        seconds = self.remaining_seconds % 60
        self.timer_label.setText(f"{minutes}:{seconds:02d}")
    
    def keyPressEvent(self, event: QKeyEvent):
        """Hidden skip feature: Press 'S' to skip the break"""
        if event.key() == Qt.Key.Key_S:
            self.timer.stop()
            self.on_complete()
        else:
            super().keyPressEvent(event)