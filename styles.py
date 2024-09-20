def apply_event_dialog_stylesheet(dialog):
    dialog.setStyleSheet("""
        QDialog {
            background-color: #E3F2FD;  /* Light blue background */
            border-radius: 10px;  /* Rounded corners for the dialog */
        }
        QLineEdit {
            font-size: 14px;
            padding: 5px;
            border: 2px solid #64B5F6;  /* Light blue border */
            border-radius: 5px;  /* Rounded corners */
            background-color: #FFFFFF;  /* White background */
        }
        QTimeEdit {
            font-size: 14px;
            padding: 5px;
            border: 2px solid #64B5F6;  /* Light blue border */
            border-radius: 5px;  /* Rounded corners */
            background-color: #FFFFFF;  /* White background */
        }
        QPushButton {
            background-color: #64B5F6;  /* Light blue button background */
            color: white;
            font-size: 14px;
            padding: 8px 16px;
            border-radius: 8px;  /* Rounded corners for the button */
            border: 1px solid #1E88E5;  /* Darker blue border */
        }
        QPushButton:hover {
            background-color: #42A5F5;  /* Darker blue when hovered */
        }
        QPushButton:pressed {
            background-color: #1E88E5;  /* Even darker blue when pressed */
        }
    """)

def apply_edit_delete_stylesheet(dialog_edit_delete):
    dialog_edit_delete.setStyleSheet("""
        QDialog {
            background-color: #E3F2FD;  /* Light blue background */
            border-radius: 10px;  /* Rounded corners */
        }
        QPushButton {
            background-color: #64B5F6;  /* Light blue button background */
            color: white;
            font-size: 14px;
            padding: 8px 16px;
            border-radius: 8px;  /* Rounded corners for the button */
            border: 1px solid #1E88E5;  /* Darker blue border */
        }
        QPushButton:hover {
            background-color: #42A5F5;  /* Slightly darker blue when hovered */
        }
        QPushButton:pressed {
            background-color: #1E88E5;  /* Even darker blue when pressed */
        }
        QPushButton#delete_button {
            background-color: #E57373;  /* Red button for delete */
            border: 1px solid #D32F2F;  /* Dark red border for delete */
        }
        QPushButton#delete_button:hover {
            background-color: #EF5350;  /* Darker red when hovered */
        }
        QPushButton#delete_button:pressed {
            background-color: #D32F2F;  /* Even darker red when pressed */
        }
    """)

def apply_slider_stylesheet(slider):
    slider.song_slider.setStyleSheet("""
        QSlider::groove:horizontal {
            border: 1px solid #999999;
            height: 8px;  /* Height of the track */
            background: #B3E5FC;  /* Light blue track color */
            border-radius: 4px;  /* Rounded corners */
        }
        QSlider::handle:horizontal {
            background: #64B5F6;  /* Handle color */
            border: 1px solid #0288D1;  /* Border color of the handle */
            width: 15px;  /* Width of the handle */
            height: 15px;  /* Height of the handle */
            border-radius: 7px;  /* Rounded handle */
            margin: -4px 0;  /* Adjust the handle position */
        }
    """)
    
def apply_stylesheet(base):
    # Apply a global stylesheet
    base.setStyleSheet("""
        QMainWindow {
            background-color: #E0F7FA;  /* Light cyan background */
        }
        QCalendarWidget QAbstractItemView:enabled {
            background-color: #F9F9F9;
            selection-background-color: #DDEEFF;
            selection-color: black;
            border: 1px solid #0288D1;  /* Darker blue border */
            font-size: 14px;
        }
        QCalendarWidget QToolButton {
            color: #333333;
            font-size: 14px;
        }
        QListWidget {
            font-size: 14px;
            background-color: #FAFAFA;
            border: 1px solid #CCCCCC;
            border-radius: 10px;
        }
        QListWidget::item {
            padding: 5px;
            border-bottom: 1px solid #81D4FA;
        }
        QListWidget::item:hover {
            background-color: #B3E5FC;
        }
        QListWidget::item:selected {
            background-color: #DDEEFF;
            color: #000000;
        }
        QPushButton {
            background-color: #64B5F6;  /* Light blue button background */
            color: white;
            font-size: 14px;
            padding: 8px 16px;
            border-radius: 8px;  /* Rounded corners for the button */
            border: 1px solid #1E88E5;  /* Darker blue border */
        }
        QPushButton:hover {
            background-color: #42A5F5;  /* Slightly darker blue when hovered */
        }
        QPushButton:pressed {
            background-color: #1E88E5;  /* Even darker blue when pressed */
        }
    """)