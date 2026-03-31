import os
os.environ["QT_MAC_WANTS_LAYER"] = "1"
os.environ["QT_QUICK_BACKEND"] = "software"
os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"

from PyQt6.QtWidgets import QApplication, QWidget
import sys

app = QApplication(sys.argv)

win = QWidget()
win.setStyleSheet("background: white;")
win.setWindowTitle("Test Window")
win.setFixedSize(900, 600)
win.show()

sys.exit(app.exec())
