from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QPushButton
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QPainter
from PyQt6.QtSvg import QSvgRenderer
import os

class CenteredSvgWidget(QWidget):
    """Renders an SVG file centered and scaled within the widget bounds."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.renderer = None
        self.setMinimumSize(550, 550)
        
    def load_svg(self, filepath):
        if os.path.exists(filepath):
            self.renderer = QSvgRenderer(filepath)
            self.update()
        else:
            self.renderer = None
            self.update()
    
    def paintEvent(self, event):
        if not self.renderer or not self.renderer.isValid():
            return
            
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        svg_size = self.renderer.defaultSize()
        if svg_size.width() == 0 or svg_size.height() == 0:
            return
        
        # Scale to fit while maintaining aspect ratio
        widget_rect = self.rect()
        scale_w = widget_rect.width() / svg_size.width()
        scale_h = widget_rect.height() / svg_size.height()
        scale = min(scale_w, scale_h) * 0.9
        
        scaled_width = svg_size.width() * scale
        scaled_height = svg_size.height() * scale
        x = (widget_rect.width() - scaled_width) / 2
        y = (widget_rect.height() - scaled_height) / 2
        
        target_rect = QRectF(x, y, scaled_width, scaled_height)
        self.renderer.render(painter, target_rect)


class ShapeRatingScreen(QWidget):
    def __init__(self, on_complete, on_play_vibration):
        super().__init__()
        self.shape_folder = "assets/shapes/svg"
        self.num_shapes = 20
        self.on_complete = on_complete
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(25)
        layout.setContentsMargins(40, 35, 40, 35)

        self.trial_label = QLabel("Trial 1 of 20")
        self.trial_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.trial_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(self.trial_label)

        question_label = QLabel("Choose the shape that best matches the vibration you just felt")
        question_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        question_label.setStyleSheet("font-size: 18px; color: #555;")
        question_label.setWordWrap(True)
        layout.addWidget(question_label)

        layout.addSpacing(15)

        self.shape_preview = CenteredSvgWidget()
        self.shape_preview.setFixedSize(550, 550)
        layout.addWidget(self.shape_preview, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addSpacing(20)

        slider_label = QLabel("Move the slider to select the shape")
        slider_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        slider_label.setStyleSheet("font-size: 16px; color: #666;")
        layout.addWidget(slider_label)

        layout.addSpacing(10)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(1, 20)
        self.slider.setValue(10)
        self.slider.setTickInterval(1)
        self.slider.setSingleStep(1)
        self.slider.setPageStep(1)
        self.slider.setFixedWidth(550)
        self.slider.setFixedHeight(30)
        self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider.valueChanged.connect(self._update_slider)
        
        self.slider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 8px;
                background: #cccccc;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #888888;
                width: 24px;
                height: 24px;
                margin: -8px 0;
                border-radius: 12px;
            }
            QSlider::handle:horizontal:hover {
                background: #666666;
            }
        """)
        
        layout.addWidget(self.slider, alignment=Qt.AlignmentFlag.AlignCenter)

        # Empty label row kept for layout spacing consistency
        range_container = QWidget()
        range_layout = QVBoxLayout(range_container)
        range_layout.setContentsMargins(0, 0, 0, 0)
        range_layout.setSpacing(5)
        
        labels_row = QWidget()
        labels_layout = QVBoxLayout(labels_row)
        labels_layout.setContentsMargins(0, 0, 0, 0)
        labels_layout.setSpacing(0)
        
        range_label = QLabel("")
        range_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        range_label.setStyleSheet("font-size: 14px; color: #888; font-style: italic;")
        labels_layout.addWidget(range_label)
        
        range_layout.addWidget(labels_row)
        range_container.setFixedWidth(550)
        layout.addWidget(range_container, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addSpacing(20)

        continue_btn = QPushButton("Continue")
        continue_btn.setFixedWidth(280)
        continue_btn.setFixedHeight(50)
        continue_btn.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                font-weight: bold;
                padding: 12px;
            }
        """)
        continue_btn.clicked.connect(self.handle_continue)
        layout.addWidget(continue_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

        self.update_shape_preview(self.slider.value())

    def set_trial_info(self, trial, total):
        self.trial_label.setText(f"Trial {trial} of {total}")
        # Reset to the middle of the range for each new trial
        self.slider.setValue(10)

    def _update_slider(self, value):
        self.update_shape_preview(value)

    def update_shape_preview(self, slider_value):
        """Load the SVG corresponding to the current slider position."""
        idx = max(1, min(self.num_shapes, slider_value))
        filename = f"kiki-bouba-{idx} copy.svg"
        path = os.path.join(self.shape_folder, filename)
        self.shape_preview.load_svg(path)

    def handle_continue(self):
        self.on_complete(self.slider.value())