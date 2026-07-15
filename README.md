# Exam Cheating Detection System

A desktop application that monitors students during exams using a live
camera or recorded video, detecting suspicious behavior such as phone use
through real-time object detection and tracking.

## Features

- Real-time detection using YOLOv8
- Persistent student tracking with ByteTrack (each student keeps a stable ID)
- Automatic alerts when a phone is detected in a student's hand
- Screenshot capture for every alert
- SQLite database logging of all alerts
- Desktop notifications
- Dark-themed desktop interface built with CustomTkinter

## Requirements

- Python 3.10+
- A webcam (for live detection) or video files (for offline analysis)

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

- Click **Start Detection** to use the live camera
- Or click **Upload Video** first to analyze a recorded video, then **Start Detection**
- Click **Stop Detection** to end the session

## Project Structure

```
cheating_alert_system/
├── main.py                      # Application entry point and controller
├── requirements.txt
├── assets/
│   ├── models/                  # YOLO model weights
│   └── default_config.json
├── data/
│   ├── database/                 # SQLite database
│   ├── logs/                     # Application logs
│   └── screenshots/               # Alert screenshots
└── src/
    ├── config/settings.py        # App configuration manager
    ├── core/engine.py            # YOLO detection + ByteTrack tracking
    ├── behavior/analyzer.py      # Suspicious behavior rules
    ├── database_manager/db_manager.py
    ├── notification/notifier.py
    ├── utils/logger.py
    ├── utils/screenshot.py
    └── ui/main_window.py         # Desktop UI
```

## How It Works

1. Each frame from the camera or video is passed to the YOLO model, which
   detects people and objects (such as phones) and assigns each person a
   persistent tracking ID.
2. The behavior analyzer checks whether a detected phone overlaps with a
   student's hand region.
3. If suspicious behavior is detected, the system logs the event to the
   database, saves a screenshot, and sends a desktop notification.

## License

This project is for educational purposes.
