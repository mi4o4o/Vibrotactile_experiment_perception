from PyQt6.QtWidgets import QApplication
from PyQt6.QtSvgWidgets import QSvgWidget

app = QApplication([])
w = QSvgWidget("assets/shapes/svg/kiki-bouba-1.svg")
w.show()
app.exec()
