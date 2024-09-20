# Alarm_APP

## Motivation
The main reason for creating this app is that we often record things on our calendar but tend to forget them when the time comes.   
To prevent this, we integreted the app with a database to record schedules and send notifications to users `30 minutes`, `5 minutes`, `1 minute` before the scheduled time. Additionally, to make task less monotonous, users can input the `Youtube` links to play the music while working.

## GUI
<img src = './gui.png' width = 250, height = 450></img>

## Features
+ Schedule insertion
+ Schdule editing
+ Schedule deletion
+ Automatic deletion of past schedules
+ Youtube music playback
+ Pinned to the top of the screen

## Description
```main.py``` : Display the main screen, excluding the `schedule insertion GUI` and the `Youtube music URL` input GUI.   
```event_dialog.py``` : A python file that creates a `schedule insertion GUI` and a `Youtube music URL` input GUI. (Refer to the image below)
