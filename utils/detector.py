import cv2
from config import (
    BLUR_SIZE,
    THRESHOLD_VALUE,
    MIN_CONTOUR_AREA,
    DILATE_ITERATIONS
)


class MotionDetector:

    def __init__(self):
        self.background_frame = None

    def update_background(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.background_frame = cv2.GaussianBlur(gray, BLUR_SIZE, 0)

    def detect(self, frame):

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, BLUR_SIZE, 0)

        if self.background_frame is None:
            self.background_frame = blurred
            return frame, False, []

        frame_delta = cv2.absdiff(self.background_frame, blurred)

        _, thresh = cv2.threshold(
            frame_delta,
            THRESHOLD_VALUE,
            255,
            cv2.THRESH_BINARY
        )

        thresh = cv2.dilate(
            thresh,
            None,
            iterations=DILATE_ITERATIONS
        )

        contours, _ = cv2.findContours(
            thresh.copy(),
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        motion_detected = False

        motion_frame = frame.copy()

        for contour in contours:

            if cv2.contourArea(contour) < MIN_CONTOUR_AREA:
                continue

            motion_detected = True

            x, y, w, h = cv2.boundingRect(contour)

            cv2.rectangle(
                motion_frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

        self.background_frame = cv2.addWeighted(
            self.background_frame,
            0.95,
            blurred,
            0.05,
            0
        )

        return motion_frame, motion_detected, contours