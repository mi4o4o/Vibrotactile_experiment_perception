def set_light_theme(app):
    app.setStyleSheet("""
        QWidget {
            background-color: #f8f8f8;  /* Off-white background for entire app */
            color: black;
            font-size: 14px;
        }
        
        QMainWindow {
            background-color: #f8f8f8;  /* Ensure main window has off-white background */
        }
        
        QStackedWidget {
            background-color: #f8f8f8;  /* Ensure stacked widget has off-white background */
        }

        /* --- BUTTONS --- */
        QPushButton {
            background-color: #d9d9d9;      /* neutral grey */
            color: black;
            border: 1px solid #b5b5b5;
            border-radius: 6px;
            padding: 8px;
        }
        QPushButton:hover {
            background-color: #cfcfcf;      /* slightly darker grey */
            border-color: #b5b5b5;
        }
        QPushButton:pressed {
            background-color: #c4c4c4;
        }
        QPushButton:disabled {
            background-color: #e5e5e5;
            color: #888;
            border-color: #cccccc;
        }

        /* --- INPUT FIELDS --- */
        QLineEdit, QComboBox {
            background-color: white;
            border: 1px solid #bfbfbf;
            padding: 5px;
        }
        QLineEdit:focus, QComboBox:focus {
            border: 1px solid #888888;
        }

        /* --- SLIDER --- */
        QSlider::groove:horizontal {
            height: 6px;
            background: #cccccc;           /* grey track */
            border-radius: 3px;
        }
        QSlider::handle:horizontal {
            background: #888888;           /* grey handle */
            width: 18px;
            height: 18px;
            margin: -6px 0;
            border-radius: 9px;
        }
        QSlider::handle:horizontal:hover {
            background: #666666;
        }

        /* --- RADIO / CHECKED BUTTONS --- */
        QPushButton:checked {
            background-color: #888888;      /* dark neutral when selected */
            color: white;
            border: 1px solid #555555;
        }
        
        /* --- SCROLL AREAS --- */
        QScrollArea {
            background-color: #f8f8f8;
            border: none;
        }
    """)