# Motion Detector — Security Camera System

A real-time motion detection security camera built with Python and OpenCV.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green)

---

## Features

* Real-time motion detection
* Green bounding boxes around movement
* Automatic video recording
* Snapshot capture on motion
* Sound alert using Windows beep
* Email alerts with image attachment
* Motion logging system
* FPS display
* Timestamp overlay
* Configurable sensitivity settings

---

## How It Works

The application continuously reads frames from the webcam and compares them with a stored background frame.

### Detection Pipeline

1. Webcam captures video frames
2. Frames are converted to grayscale
3. Gaussian blur removes noise
4. Background subtraction detects pixel changes
5. Thresholding isolates moving regions
6. Contour detection finds moving objects
7. Bounding boxes are drawn around detected motion

---

## Technologies Used

* Python
* OpenCV
* NumPy
* SMTP Email
* dotenv

---


## Installation

### Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/motion-detector.git
cd motion-detector
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

#### Windows

```powershell
.\venv\Scripts\Activate.ps1
```

#### Mac/Linux

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configuration

Open `config.py` and modify settings such as:

* Motion sensitivity
* Recording settings
* FPS display
* Webcam index

Example:

```python
MIN_CONTOUR_AREA = 500
```

Increase value:

* less sensitive

Decrease value:

* more sensitive

---

## Email Alerts

Create a `.env` file in the project root:

```env
SENDER_EMAIL=your_email@gmail.com
RECEIVER_EMAIL=receiver@gmail.com
GMAIL_APP_PASSWORD=your_app_password
```

Important:

* Never upload `.env`
* Use Gmail App Passwords
* Enable 2-Step Verification in Google Account

---

## Run the Project

```bash
python main.py
```

---

## Controls

| Key | Action                 |
| --- | ---------------------- |
| Q   | Quit                   |
| R   | Reset background       |
| S   | Save snapshot manually |

---

## Output

Snapshots:

```txt
output/snapshots/
```

Recordings:

```txt
output/recordings/
```

Logs:

```txt
motion_log.txt
```

---

## Concepts Learned

* Computer Vision
* Frame Differencing
* Background Subtraction
* Contour Detection
* Video Processing
* Event-Based Recording
* Email Automation
* Modular Python Architecture

---

## Future Improvements

Possible upgrades:

* Face detection
* Person detection using AI
* Telegram alerts
* Cloud storage
* Mobile notifications
* Object tracking
* Gesture recognition

---

## License

MIT License
