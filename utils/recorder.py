import cv2
import os

from datetime import datetime

from config import (
    RECORDING_FPS,
    RECORDING_CODEC,
    RECORDING_FORMAT
)


class VideoRecorder:

    def __init__(self):
        self.writer = None
        self.is_recording = False
        self.output_path = None

    def start_recording(
        self,
        frame,
        output_dir="output/recordings"
    ):

        if self.is_recording:
            return

        os.makedirs(output_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        self.output_path = os.path.join(
            output_dir,
            f"motion_{timestamp}{RECORDING_FORMAT}"
        )

        height, width = frame.shape[:2]

        fourcc = cv2.VideoWriter_fourcc(*RECORDING_CODEC)

        self.writer = cv2.VideoWriter(
            self.output_path,
            fourcc,
            RECORDING_FPS,
            (width, height)
        )

        self.is_recording = True

        print(f"[RECORDER] Recording started: {self.output_path}")

    def write_frame(self, frame):

        if self.is_recording and self.writer:
            self.writer.write(frame)

    def stop_recording(self):

        if self.is_recording and self.writer:

            self.writer.release()

            self.writer = None
            self.is_recording = False

            print(f"[RECORDER] Recording saved: {self.output_path}")

    @staticmethod
    def save_snapshot(
        frame,
        output_dir="output/snapshots"
    ):

        os.makedirs(output_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

        path = os.path.join(
            output_dir,
            f"snapshot_{timestamp}.jpg"
        )

        cv2.imwrite(path, frame)

        print(f"[SNAPSHOT] Saved: {path}")

        return path