import sqlite3
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QTimeEdit, QPushButton, QMessageBox
from PyQt5.QtCore import QTime
from styles import apply_event_dialog_stylesheet  # Assuming you have this in your styles module


class EventDialog(QDialog):
    def __init__(self, date, parent = None, title="", time_str="00:00"):
        super().__init__(parent)
        try:
            self.date = date.toString("yyyy-MM-dd")
        except:
            self.date = date
            
        self.setWindowTitle(f"Event for {self.date}")
        
        # setting the dialog gui size
        self.setFixedSize(500, 150)
        
        layout = QVBoxLayout()
        
        # Input title
        self.title_input = QLineEdit(self)
        self.title_input.setPlaceholderText("Enter title")
        self.title_input.setText(title)  # Set existing title if provided
        
        # Input time
        self.time_input = QTimeEdit(self)
        self.time_input.setDisplayFormat("HH:mm")
        self.time_input.setTime(QTime.fromString(time_str, "HH:mm"))
        
        # Input Submit 
        self.submit_button = QPushButton("Submit", self)
        
        layout.addWidget(self.title_input)
        layout.addWidget(self.time_input)
        layout.addWidget(self.submit_button)
        self.setLayout(layout)
        
        apply_event_dialog_stylesheet(self)
        
        # Button action
        self.submit_button.clicked.connect(self.submit)

        
    def submit(self):
        title = self.title_input.text()
        time = self.time_input.time().toString("HH:mm")
        
        if title:
            conn = sqlite3.connect('events.db')
            cursor = conn.cursor()

            # Check if the event already exists
            cursor.execute('''
                SELECT * FROM events WHERE date = ? AND time = ?
            ''', (self.date, time))
            
            existing_event = cursor.fetchone()
            
            if existing_event:
                # If event exists, prompt the user
                reply = QMessageBox.question(self, 'Event Exists',
                                            f'{time} event "{existing_event[3]}" already exists. Do you want to replace it?',
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

                if reply == QMessageBox.Yes:
                    # Update the existing event in the database
                    cursor.execute('''
                        UPDATE events SET title = ? WHERE date = ? AND time = ?
                    ''', (title, self.date, time))
                    conn.commit()
                    
                    # Update the event in the parent window (MainWindow)
                    self.parent().update_event(self.date, time, title)

            else:
                # Insert the new event into the database
                cursor.execute('''
                    INSERT INTO events (date, time, title) VALUES (?, ?, ?)
                ''', (self.date, time, title))
                conn.commit()

                # Insert: Call the parent to add the event to the list
                self.parent().add_event(self.date, time, title)
                
            conn.close()
            self.accept()  # Close the dialog
               
class URLInputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Enter YouTube URL")
        self.setFixedSize(400, 150)

        layout = QVBoxLayout()

        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("Enter YouTube URL...")

        self.submit_button = QPushButton("Play Song", self)

        layout.addWidget(self.url_input)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

        apply_event_dialog_stylesheet(self)
        
        # Connect the button click to accept the dialog (submit the input)
        self.submit_button.clicked.connect(self.accept)
