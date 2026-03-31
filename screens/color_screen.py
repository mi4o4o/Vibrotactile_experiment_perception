from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QScrollArea, QSizePolicy
)
from PyQt6.QtCore import Qt
import random

from screens.color_tile import ColorTile
from utils.colors import COLOR_SHADES_11


class ColorRatingScreen(QWidget):
    """
    Displays matrix of colour tiles grouped by hue.
    Row order is reshuffled on every trial.
    """
    
    def __init__(self, on_complete):
        
        super().__init__()
        self.on_complete = on_complete

        self.tiles = {}
        self.rows = {}
        self.selected_tile = None
        self.selected_hue = None
        self.selected_index = None
        
        self.scroll = None
        self.color_grid_layout = None

        self._build_ui()

    def _build_ui(self):
        main = QVBoxLayout()
        main.setAlignment(Qt.AlignmentFlag.AlignTop)
        main.setSpacing(20)
        main.setContentsMargins(40, 35, 40, 35)

        self.trial_label = QLabel("Trial 1 of X")
        self.trial_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.trial_label.setStyleSheet("""
            font-size: 20px; 
            font-weight: 600; 
            color: #000000;
        """)
        main.addWidget(self.trial_label)

        q = QLabel("Choose the colour that best matches the vibration you just felt")
        q.setAlignment(Qt.AlignmentFlag.AlignCenter)
        q.setStyleSheet("""
            font-size: 16px; 
            color: #333333; 
            margin-bottom: 8px;
        """)
        q.setWordWrap(True)
        main.addWidget(q)
        
        main.addSpacing(12)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self._build_color_grid()

        main.addWidget(self.scroll, stretch=1)

        main.addSpacing(20)

        preview_container = QWidget()
        preview_container.setStyleSheet("background-color: transparent;")
        preview_layout = QVBoxLayout(preview_container)
        preview_layout.setSpacing(12)
        preview_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        preview_layout.setContentsMargins(0, 0, 0, 0)
        
        # Large square that fills with the selected colour so the participant can confirm their choice
        self.preview_square = QFrame()
        self.preview_square.setFixedSize(160, 160)
        self.preview_square.setVisible(False)
        self.preview_square.setStyleSheet("")
        preview_layout.addWidget(self.preview_square, alignment=Qt.AlignmentFlag.AlignCenter)

        self.selected_label = QLabel("No colour selected")
        self.selected_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.selected_label.setStyleSheet("""
            font-size: 15px; 
            color: #666666; 
            font-weight: 500;
            background-color: transparent;
        """)
        preview_layout.addWidget(self.selected_label)
        
        main.addWidget(preview_container)

        main.addSpacing(18)

        # Continue is disabled until the participant actually selects something
        self.continue_btn = QPushButton("Continue")
        self.continue_btn.setEnabled(False)
        self.continue_btn.setFixedWidth(240)
        self.continue_btn.setFixedHeight(48)
        # Uses global button styling from theming.py
        self.continue_btn.clicked.connect(self._submit)
        main.addWidget(self.continue_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(main)

    def _build_color_grid(self):
        """
        Builds the colour grid from scratch with a shuffled row order.
        Called once on init and again at the start of every new trial.
        """
        content = QWidget()
        content.setStyleSheet("background-color: #f8f8f8;")
        
        self.color_grid_layout = QVBoxLayout(content)
        self.color_grid_layout.setSpacing(12)
        self.color_grid_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.color_grid_layout.setContentsMargins(0, 0, 0, 0)

        hue_names = list(COLOR_SHADES_11.keys())
        random.shuffle(hue_names)

        self.tiles.clear()
        self.rows.clear()

        for hue in hue_names:
            shades = COLOR_SHADES_11[hue]
            
            row_container = QWidget()
            row_container.setStyleSheet("background-color: transparent;")
            row_container_layout = QHBoxLayout(row_container)
            row_container_layout.setContentsMargins(0, 0, 0, 0)
            row_container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            row_frame = QFrame()
            row_frame.setStyleSheet("background-color: transparent;")
            row_frame.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            row_layout = QHBoxLayout(row_frame)
            row_layout.setSpacing(0)
            row_layout.setContentsMargins(0, 0, 0, 0)
            
            row_tiles = []

            for idx, hex_code in enumerate(shades):
                tile = ColorTile(hue, idx, hex_code)
                tile.clicked.connect(self._tile_clicked)

                self.tiles[(hue, idx)] = tile
                row_tiles.append(tile)
                row_layout.addWidget(tile, 0, Qt.AlignmentFlag.AlignLeft)

            self.rows[hue] = row_tiles
            row_container_layout.addWidget(row_frame)
            self.color_grid_layout.addWidget(row_container)

        self.scroll.setWidget(content)

    def _tile_clicked(self, hue, idx, hex_code):
        # Deselect the previous tile before selecting the new one
        if self.selected_tile:
            self.selected_tile.set_selected(False)

        tile = self.tiles[(hue, idx)]
        tile.set_selected(True)
        self.selected_tile = tile

        self.selected_hue = hue
        self.selected_index = idx

        # Update the preview and unlock the continue button
        self.preview_square.setVisible(True)
        self.preview_square.setStyleSheet(
            f"""
            background-color: {hex_code}; 
            border: 1px solid rgba(0,0,0,0.15);
            """
        )
        self.selected_label.setText("Selected colour")
        self.continue_btn.setEnabled(True)

    def set_trial_info(self, trial, total):
        """Reset the screen for a new trial - clears selection and reshuffles the colour rows."""
        self.trial_label.setText(f"Trial {trial} of {total}")

        if self.selected_tile:
            self.selected_tile.set_selected(False)

        self.selected_tile = None
        self.selected_hue = None
        self.selected_index = None

        self.preview_square.setVisible(False)
        self.selected_label.setText("No colour selected")
        self.continue_btn.setEnabled(False)

        self._build_color_grid()

    def _submit(self):
        if self.selected_hue is not None:
            self.on_complete(self.selected_hue, self.selected_index)