import cv2
import time
import logging
import os

from datetime import datetime

from dotenv import load_dotenv

from config import (
    CAMERA_INDEX,
    RECORD_ON_MOTION,
    SNAPSHOT_ON_MOTION,
    PLAY_SOUND_ALERT,
    MOTION_COOLDOWN,
    SHOW_FPS,
    FRAME_WIDTH,
    FRAME_HEIGHT
)

from utils.detector import MotionDetector
from utils.recorder import VideoRecorder

from alerts.sound_alert import play_alert
from alerts.email_alert import send_email_alert


load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("motion_log.txt"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def draw_status(frame, status, fps=None):

    color = (0, 0, 255) if status == "MOTION DETECTED" else (0, 255, 0)

    cv2.putText(
        frame,
        status,
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        color,
        2
    )

    if fps and SHOW_FPS:

        cv2.putText(
            frame,
            f"FPS: {fps:.1f}",
            (10, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 0),
            1
        )

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cv2.putText(
        frame,
        timestamp,
        (frame.shape[1] - 220, frame.shape[0] - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (200, 200, 200),
        1
    )

    return frame


def main():

    logger.info("Starting motion detector...")

    cap = cv2.VideoCapture(CAMERA_INDEX)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    if not cap.isOpened():

        logger.error("Could not open webcam.")
        return

    detector = MotionDetector()

    recorder = VideoRecorder()

    last_motion_time = 0
    last_sound_time = 0

    snapshot_taken = False

    prev_time = time.time()

    logger.info("Press Q to quit")

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        curr_time = time.time()

        fps = 1 / (curr_time - prev_time + 1e-9)

        prev_time = curr_time

        processed_frame, motion_detected, contours = detector.detect(frame)

        if motion_detected:

            status = "MOTION DETECTED"

            last_motion_time = curr_time

            logger.info("Motion detected!")

            if PLAY_SOUND_ALERT and (
                curr_time - last_sound_time > 5
            ):

                play_alert()

                last_sound_time = curr_time

            if SNAPSHOT_ON_MOTION and not snapshot_taken:

                snapshot_path = VideoRecorder.save_snapshot(
                    processed_frame
                )

                snapshot_taken = True

                send_email_alert(
                    snapshot_path=snapshot_path,
                    sender_email=os.getenv("SENDER_EMAIL"),
                    receiver_email=os.getenv("RECEIVER_EMAIL"),
                    app_password=os.getenv("GMAIL_APP_PASSWORD")
                )

            if RECORD_ON_MOTION and not recorder.is_recording:

                recorder.start_recording(processed_frame)

        else:

            status = "Monitoring..."

            snapshot_taken = False

            if recorder.is_recording:

                time_since_motion = (
                    curr_time - last_motion_time
                )

                if time_since_motion > MOTION_COOLDOWN:

                    recorder.stop_recording()

        if recorder.is_recording:

            recorder.write_frame(processed_frame)

        display_frame = draw_status(
            processed_frame,
            status,
            fps
        )

        cv2.imshow(
            "Motion Detector",
            display_frame
        )

        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break

        elif key == ord('r'):

            detector.update_background(frame)

            logger.info("Background reset")

        elif key == ord('s'):

            VideoRecorder.save_snapshot(processed_frame)

    recorder.stop_recording()

    cap.release()

    cv2.destroyAllWindows()

    logger.info("Motion detector stopped")


if __name__ == "__main__":
    main()