# for database
import sqlite3
from database import init_db

# for dialog
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QCalendarWidget, QDialog, QVBoxLayout, QLineEdit, QTimeEdit, QPushButton, QListWidget, QWidget, QMessageBox, QSlider, QLabel, QHBoxLayout
from PyQt5.QtCore import QDate, QTime, QTimer, QUrl, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import yt_dlp

from styles import apply_slider_stylesheet, apply_stylesheet, apply_edit_delete_stylesheet
from event_dialog import EventDialog, URLInputDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create Calendar Widget
        self.calendar = QCalendarWidget(self)
        self.calendar.setGridVisible(True)
        self.calendar.clicked.connect(self.date_clicked)
        self.calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)

        # Create Event List Widget (scrollable)
        self.event_list = QListWidget(self)
        self.event_list.itemDoubleClicked.connect(self.event_double_clicked)

        self.setWindowTitle(f"Event Manager-TCK")
        self.setWindowIcon(QIcon("./images/event.png"))
        self.setFixedSize(300, 500)
        
        # Create QLabel for the song name (scrolling)
        self.song_label = QLabel("Now Playing: No Song", self)
        self.song_label.setAlignment(Qt.AlignCenter)
        
        # Create a QPushButton to input a YouTube URL and play the song
        self.url_button = QPushButton("Play from URL", self)
        self.url_button.clicked.connect(self.open_url_input_dialog)
        
        # Marquee settings
        self.marquee_text = "Now Playing: No Song"
        self.marquee_index = 0
        self.marquee_timer = QTimer(self)
        self.marquee_timer.timeout.connect(self.scroll_text)
        self.marquee_timer.start(200)  # Adjust the speed (lower value = faster)

        # Create a QSlider to show song progress
        self.song_slider = QSlider(Qt.Horizontal, self)
        self.song_slider.setRange(0, 100)
        self.song_slider.setEnabled(False)
        self.song_slider.sliderMoved.connect(self.set_position)
        apply_slider_stylesheet(self)

        # Create a QSlider for volume control
        self.volume_slider = QSlider(Qt.Horizontal, self)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)  # Set default volume to 50%
        self.volume_slider.sliderMoved.connect(self.set_volume)
        
        # Create QLabel for volume indicator
        self.volume_label = QLabel("Volume: 50", self)
        
        # Set up the media player
        self.player = QMediaPlayer(self)
        self.player.setVolume(50)  # Set initial volume to 50%
        
        # Timer to update the progress bar
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_position)
        self.timer.start(1000)  # Update every second
        
        # Set up a QTimer to check for upcoming events every minute
        self.event_check_timer = QTimer(self)
        self.event_check_timer.timeout.connect(self.check_upcoming_events)
        self.event_check_timer.start(60000)  # 1000 ms = 1 sec

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.calendar)
        layout.addWidget(self.song_label)  # Song title goes here
        layout.addWidget(self.song_slider)  # Progress bar below song title
        
        # Horizontal layout for volume control
        volume_layout = QHBoxLayout()
        volume_layout.addWidget(self.url_button)
        volume_layout.addWidget(self.volume_label)
        volume_layout.addWidget(self.volume_slider)
        layout.addLayout(volume_layout)

        layout.addWidget(self.event_list)
        
        container = self.centralWidget()
        
        if not container:
            container = QWidget()
            self.setCentralWidget(container)
        container.setLayout(layout)

        apply_stylesheet(self)
        
        # Load event
        self.load_events()
        
        # Stream and play audio from a YouTube link
        self.stream_and_play_youtube("https://www.youtube.com/watch?v=zIMUVTbRmek")
    
    def open_url_input_dialog(self):
        # Open the dialog to input a YouTube URL
        dialog = URLInputDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            youtube_url = dialog.url_input.text()
            if youtube_url:
                self.stream_and_play_youtube(youtube_url)
        
    def set_song_title(self, title):
        # Set the song label to display the current stream title and start marquee.
        self.marquee_text = f"Now Playing: {title}" + " " * 10  # Add some space to the end for smoother scrolling
        self.marquee_index = 0  # Reset the scroll position

    def scroll_text(self):
        # Scroll the song title from right to left.
        display_text = self.marquee_text[self.marquee_index:] + self.marquee_text[:self.marquee_index]
        # print(display_text)
        self.song_label.setText(display_text)
        self.marquee_index += 1

        # Wrap around when the index reaches the end of the text
        if self.marquee_index > len(self.marquee_text):
            self.marquee_index = 0
    
    def stream_and_play_youtube(self, youtube_url):
        # Stream and play audio directly from a YouTube link.
        ydl_opts = {
            'format': 'bestaudio/best',  # Best available audio format
            'noplaylist': True  # Don't download entire playlists
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=False)
            audio_url = info_dict['url']  # Get the direct audio stream URL
            self.load_stream(audio_url, info_dict['title'])

    def load_stream(self, stream_url, title):
        # Loads a stream URL and starts playing it.
        url = QUrl(stream_url)
        self.player.setMedia(QMediaContent(url))
        self.player.play()
        
        # Set the song label
        self.set_song_title(title)
        
        # Set media status change handler to restart music when it finishes
        self.player.mediaStatusChanged.connect(self.check_for_restart)
     
    def set_position(self, position):
        # Set the media player position based on slider movement.
        self.player.setPosition(position)

    def update_position(self):
        # Updates the song slider as the song plays.
        if self.player.duration() > 0:
            self.song_slider.setMaximum(self.player.duration())
            self.song_slider.setValue(self.player.position()) 
    
    def set_volume(self, value):
        # Adjust the volume based on the slider.
        self.player.setVolume(value)
        self.volume_label.setText(f"Volume: {value}")
     
    def check_for_restart(self, status):
        # Restarts the song when it reaches the end.
        if status == QMediaPlayer.EndOfMedia:
            self.player.play()
    
    def check_upcoming_events(self):
        # Check for upcoming events and show notifications.
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        
        # Load events from the database
        conn = sqlite3.connect('events.db')
        cursor = conn.cursor()
        cursor.execute("SELECT date, time, title FROM events")
        events = cursor.fetchall()

        # Track which events to delete
        events_to_delete = []

        # Check for each event if it is within 30, 5, or 1 minute of the current time
        for event in events:
            date_str, time_str, title = event
            event_date = QDate.fromString(date_str, "yyyy-MM-dd")
            event_time = QTime.fromString(time_str, "HH:mm")
            
            if event_date == current_date:
                # Calculate time difference in minutes
                time_diff = current_time.secsTo(event_time) // 60
                
                # Check if the event is happening soon (within 30, 5, or 1 minute)
                if 5 < time_diff <= 30:
                    self.show_notification(f"Event '{title}' is happening in 30 minutes!")
                elif 1 < time_diff <= 5:
                    self.show_notification(f"Event '{title}' is happening in 5 minutes!")
                elif 0 < time_diff <= 1:
                    self.show_notification(f"Event '{title}' is happening in 1 minute!")
                elif time_diff < 0:
                # Event is in the past, mark it for deletion
                    events_to_delete.append((date_str, time_str, title))
                    
        for date_str, time_str, title in events_to_delete:
            cursor.execute('''
                DELETE FROM events WHERE date = ? AND time = ? AND title = ?
            ''', (date_str, time_str, title))
            self.remove_event_from_list(date_str, time_str, title)

        # Commit the changes to the database
        conn.commit()
        conn.close()
        
    def remove_event_from_list(self, date, time, title):
        # Remove an event from the QListWidget based on date, time, and title.
        for index in range(self.event_list.count()):
            item_text = self.event_list.item(index).text()
            if item_text.startswith(f"{date} {time} {title}"):
                self.event_list.takeItem(index)
                break
        
    def show_notification(self, message):
        # Display a message box with the notification.
        QMessageBox.information(self, "Upcoming Event", message)
        
    def date_clicked(self):
        selected_date = self.calendar.selectedDate()
        
        # today
        today = QDate.currentDate()
        
        if selected_date < today:
            QMessageBox.warning(self, "Invalid Date", "you cannot select a date before today !!!!!")
        else:
            self.open_event_dialog(selected_date)

    def open_event_dialog(self, date):
        dialog = EventDialog(date, self)
        dialog.exec_()

    def event_double_clicked(self, item):
        # pre-processing 
        event_text = item.text()  # "2024-09-14 10:00: Meeting"
        date_str, time_str, title = event_text.split(' ', 2)
        
        # Create dialog with edit and delete buttons
        self.edit_delete_event_dialog(date_str, time_str, title, item)
    
    def edit_delete_event_dialog(self, date, time, title, item):
        # delete dialog
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Edit or Delete Event for {date}")
        dialog.setFixedSize(500, 100)
        
        layout = QVBoxLayout()
        
        # Edit button
        edit_button = QPushButton("Edit")
        edit_button.clicked.connect(lambda: self.edit_event(date, time, title, dialog, item))

        # Delete button
        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(lambda: self.delete_event(date, time, title, dialog, item))

        layout.addWidget(edit_button)
        layout.addWidget(delete_button)
        
        dialog.setLayout(layout)
        
        # Apply the custom stylesheet
        apply_edit_delete_stylesheet(dialog)
        
        dialog.exec_()
    
    def edit_event(self, date, time, title, dialog, item):
        # Open the edit event dialog
        dialog.close()
        edit_dialog = EventDialog(date, self, title=title, time_str=time)
        edit_dialog.exec_()

    def delete_event(self, date, time, title, dialog, item):
        # Delete the selected event from the database and update the UI
        # but why cannot be applied permanently ???? 
        conn = sqlite3.connect('events.db')
        cursor = conn.cursor()
        
        # Delete from database
        cursor.execute('''
            DELETE FROM events WHERE date = ? AND time = ? AND title = ?
        ''', (date, time, title))
        
        conn.commit()
        conn.close()

        # Remove item from list
        row = self.event_list.row(item)
        self.event_list.takeItem(row)

        # Close dialog
        dialog.accept()
    
    def add_event(self, date, time, title):
        event_str = f"{date} {time} {title}"
        self.event_list.addItem(event_str)
        
        self.sort_event_list()

    def sort_event_list(self):
        # Extract all items from the QListWidget into a list
        event_items = []
        for index in range(self.event_list.count()):
            # append all of the values in event_list
            event_items.append(self.event_list.item(index).text())

        # Sort the event_items by date (assuming the date is the first part in 'yyyy-MM-dd' format)
        event_items.sort(key=lambda event: QDate.fromString(event.split(' ')[0], "yyyy-MM-dd"))

        # Clear the QListWidget
        self.event_list.clear()

        # Add the sorted events back into the QListWidget
        for event in event_items:
            self.event_list.addItem(event)
    
    def update_event(self, date, time, title):
        # Update the visualization
        for index in range(self.event_list.count()):
            item_text = self.event_list.item(index).text()
            if item_text.startswith(f"{date} {time}"):
                self.event_list.item(index).setText(f"{date} {time} {title}")
                break

    def load_events(self):
        # Load all of the data
        conn = sqlite3.connect('events.db')
        cursor = conn.cursor()
        cursor.execute("SELECT date, time, title FROM events")
        events = cursor.fetchall()
        conn.close()

        # Sorting Ascending
        events.sort(key = lambda event: QDate.fromString(event[0], "yyyy-MM-dd"))
        
        for event in events:
            date, time, title = event
            event_str = f"{date} {time} {title}"
            self.event_list.addItem(event_str)

if __name__ == '__main__':
    # Initialize database
    init_db()

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    
    # Ensure the window stays on top
    window.setWindowFlags(window.windowFlags() | Qt.WindowStaysOnTopHint)
    window.show()  # Re-show the window after setting the flag
    sys.exit(app.exec_())
