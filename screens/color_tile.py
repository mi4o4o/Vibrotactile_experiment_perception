# screens/color_tile.py
from PyQt6.QtWidgets import QFrame, QSizePolicy
from PyQt6.QtCore import Qt, pyqtSignal


class ColorTile(QFrame):
    """A single clickable colour square in the colour grid."""

    clicked = pyqtSignal(str, int, str)

    def __init__(self, hue, index, hex_code, parent=None):
        super().__init__(parent)
        self.hue = hue
        self.index = index
        self.hex_code = hex_code

        self.tile_width = 60
        self.tile_height = 60
        self.is_selected = False

        self.setFixedSize(self.tile_width, self.tile_height)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setMouseTracking(False)

        self._apply_style(selected=False)

        # Small white dot that appears in the center when this tile is selected
        self.dot = QFrame(self)
        self.dot.setFixedSize(16, 16)
        self.dot.hide()
        self.dot.setStyleSheet(
            "background-color: white; border-radius: 8px; border: 2px solid rgba(0,0,0,0.4);"
        )
        self.dot.move(
            (self.tile_width - 16) // 2,
            (self.tile_height - 16) // 2
        )

    def _apply_style(self, selected=False):
        # Add a subtle border when selected so the choice is clear without being distracting
        border = "2px solid rgba(0,0,0,0.3)" if selected else "none"

        self.setStyleSheet(
            f"""
            ColorTile {{
                background-color: {self.hex_code};
                border: {border};
                margin: 0px;
                padding: 0px;
            }}
            """
        )

    def mousePressEvent(self, event):
        self.clicked.emit(self.hue, self.index, self.hex_code)
        super().mousePressEvent(event)

    def set_selected(self, selected: bool):
        self.is_selected = selected
        self._apply_style(selected)

        if selected:
            self.dot.show()
        else:
            self.dot.hide()