from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QScrollArea, QSizePolicy, QSlider
)
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QPainter
from PyQt6.QtSvg import QSvgRenderer
import os
import random

from screens.color_tile import ColorTile
from utils.colors import COLOR_SHADES_11


class ColorableSvgWidget(QWidget):
    """
    SVG widget that can be filled with any colour dynamically.
    Used in the combined round to show the selected shape filled with the selected colour.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.renderer = None
        self.svg_content = ""
        self.current_color = None  # None = outline only, no fill
        self.setMinimumSize(550, 550)
        
    def load_svg(self, filepath):
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                self.svg_content = f.read()
            self._update_renderer()
        else:
            self.renderer = None
            self.update()
    
    def set_fill_color(self, hex_color):
        """Change the fill colour and trigger a redraw."""
        self.current_color = hex_color
        self._update_renderer()
    
    def _update_renderer(self):
        """Inject the current fill colour into the SVG source and reload the renderer."""
        if not self.svg_content:
            return
        
        modified_svg = self.svg_content
        
        if self.current_color:
            modified_svg = modified_svg.replace('fill: none;', f'fill: {self.current_color};')
            modified_svg = modified_svg.replace('fill="none"', f'fill="{self.current_color}"')
        
        self.renderer = QSvgRenderer(modified_svg.encode('utf-8'))
        self.update()
    
    def paintEvent(self, event):
        """Scale and center the SVG within the widget bounds."""
        if not self.renderer or not self.renderer.isValid():
            return
            
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        svg_size = self.renderer.defaultSize()
        if svg_size.width() == 0 or svg_size.height() == 0:
            return
        
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


class CombinedRatingScreen(QWidget):
    """
    The combined round screen where participants select both a colour and a shape.
    Laid out as two panels side by side — colour grid on the left, shape slider on the right.
    The shape fills with the selected colour in real time so participants can see the combination.
    """
    
    def __init__(self, on_complete):
        super().__init__()
        self.on_complete = on_complete
        
        self.shape_folder = "assets/shapes/svg"
        self.num_shapes = 20
        
        self.tiles = {}
        self.selected_tile = None
        self.selected_hue = None
        self.selected_index = None
        
        # Keeps a reference to the colour grid so it can be torn down and rebuilt each trial
        self.colors_container = None
        
        self._build_ui()

    def _build_ui(self):
        main = QVBoxLayout()
        main.setSpacing(0)
        main.setContentsMargins(40, 35, 40, 25)

        self.trial_label = QLabel("Trial 1 of X")
        self.trial_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.trial_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #2c3e50;")
        main.addWidget(self.trial_label)

        q = QLabel("Choose the shape and colour that best match the vibration you just felt")
        q.setAlignment(Qt.AlignmentFlag.AlignCenter)
        q.setStyleSheet("font-size: 18px; color: #555;")
        q.setWordWrap(True)
        main.addWidget(q)

        main.addSpacing(55)
        
        content = QHBoxLayout()
        content.setSpacing(80)
        content.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Left panel: colour selection
        self.left_panel = QVBoxLayout()
        self.left_panel.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        
        color_label = QLabel("Colour")
        color_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        color_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50;")
        self.left_panel.addWidget(color_label)
        
        self.left_panel.addSpacing(15)
        
        self._build_color_grid()
        
        self.left_panel.addStretch()
        
        # Right panel: shape selection
        right_panel = QVBoxLayout()
        right_panel.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        
        shape_label = QLabel("Shape")
        shape_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        shape_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50;")
        right_panel.addWidget(shape_label)
        
        right_panel.addSpacing(15)
        
        self.shape_preview = ColorableSvgWidget()
        self.shape_preview.setFixedSize(550, 550)
        right_panel.addWidget(self.shape_preview, alignment=Qt.AlignmentFlag.AlignCenter)
        
        right_panel.addSpacing(15)
        
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(1, 20)
        self.slider.setValue(10)
        self.slider.setFixedWidth(550)
        self.slider.setFixedHeight(30)
        self.slider.valueChanged.connect(self._update_shape)
        
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
        
        right_panel.addWidget(self.slider, alignment=Qt.AlignmentFlag.AlignCenter)
        
        slider_desc = QLabel("Move the slider to select a shape")
        slider_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        slider_desc.setStyleSheet("font-size: 14px; color: #666;")
        right_panel.addWidget(slider_desc)
        
        right_panel.addStretch()
        
        content.addLayout(self.left_panel)
        content.addLayout(right_panel)
        
        main.addLayout(content)
        
        main.addSpacing(25)

        # Continue is disabled until the participant selects a colour
        self.continue_btn = QPushButton("Continue")
        self.continue_btn.setEnabled(False)
        self.continue_btn.setFixedWidth(280)
        self.continue_btn.setFixedHeight(50)
        self.continue_btn.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                font-weight: bold;
                padding: 12px;
            }
        """)
        self.continue_btn.clicked.connect(self._submit)
        main.addWidget(self.continue_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.setLayout(main)
        
        self.update_shape_preview(10)
    
    def _build_color_grid(self):
        """
        Rebuilds the colour grid with a freshly shuffled row order.
        The old grid is destroyed first to avoid leftover widgets piling up.
        The new grid is inserted at index 1, right below the "Colour" label.
        """
        if self.colors_container:
            self.left_panel.removeWidget(self.colors_container)
            self.colors_container.deleteLater()
        
        self.colors_container = QWidget()
        colors_layout = QVBoxLayout(self.colors_container)
        colors_layout.setSpacing(12)
        colors_layout.setContentsMargins(0, 0, 0, 0)
        colors_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        
        hue_names = list(COLOR_SHADES_11.keys())
        random.shuffle(hue_names)
        
        self.tiles.clear()
        
        for hue in hue_names:
            shades = COLOR_SHADES_11[hue]
            
            row_container = QWidget()
            row_container_layout = QHBoxLayout(row_container)
            row_container_layout.setContentsMargins(0, 0, 0, 0)
            row_container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            row_frame = QFrame()
            row_frame.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            row_layout = QHBoxLayout(row_frame)
            row_layout.setSpacing(0)
            row_layout.setContentsMargins(0, 0, 0, 0)
            
            for idx, hex_code in enumerate(shades):
                tile = ColorTile(hue, idx, hex_code)
                tile.clicked.connect(self._tile_clicked)
                self.tiles[(hue, idx)] = tile
                row_layout.addWidget(tile, 0, Qt.AlignmentFlag.AlignLeft)
            
            row_container_layout.addWidget(row_frame)
            colors_layout.addWidget(row_container)
        
        self.left_panel.insertWidget(1, self.colors_container)
    
    def _update_shape(self, value):
        self.update_shape_preview(value)
    
    def update_shape_preview(self, slider_value):
        """Load the SVG for the current slider position and reapply the selected colour if any."""
        idx = max(1, min(self.num_shapes, slider_value))
        filename = f"kiki-bouba-{idx} copy.svg"
        path = os.path.join(self.shape_folder, filename)
        self.shape_preview.load_svg(path)
        
        # Keep the shape filled with the current colour when sliding
        if self.selected_hue is not None:
            tile = self.tiles[(self.selected_hue, self.selected_index)]
            self.shape_preview.set_fill_color(tile.hex_code)
    
    def _tile_clicked(self, hue, idx, hex_code):
        if self.selected_tile:
            self.selected_tile.set_selected(False)
        
        tile = self.tiles[(hue, idx)]
        tile.set_selected(True)
        self.selected_tile = tile
        
        self.selected_hue = hue
        self.selected_index = idx
        
        # Fill the shape preview with the chosen colour immediately
        self.shape_preview.set_fill_color(hex_code)
        
        self.continue_btn.setEnabled(True)
    
    def set_trial_info(self, trial, total):
        """Reset the screen for a new trial — clears selections, resets the slider, and reshuffles the colour rows."""
        self.trial_label.setText(f"Trial {trial} of {total}")
        
        if self.selected_tile:
            self.selected_tile.set_selected(False)
        
        self.selected_tile = None
        self.selected_hue = None
        self.selected_index = None
        
        # Return slider to the middle of the range
        self.slider.setValue(10)
        self.shape_preview.set_fill_color(None)

        self.continue_btn.setEnabled(False)
        
        self._build_color_grid()
    
    def _submit(self):
        if self.selected_hue is not None:
            self.on_complete(self.slider.value(), self.selected_hue, self.selected_index)